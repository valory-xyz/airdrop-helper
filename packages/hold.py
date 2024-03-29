# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Hold"""

import csv


class veOLAS:
    """veOLAS"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        self.contract_manager = contract_manager
        if "ethereum" not in self.contract_manager.skip_chains:
            self.veolas = contract_manager.contracts["ethereum"]["other"]["veolas"]
            self.wveolas = contract_manager.contracts["ethereum"]["other"]["wveolas"]

    def _get_veolas_holders(self, block=None):
        """Get events"""
        deposits = self.veolas.events.Deposit.create_filter(
            fromBlock="earliest",
            toBlock=block if block else "latest",
        ).get_all_entries()

        withdraws = self.veolas.events.Withdraw.create_filter(
            fromBlock="earliest",
            toBlock=block if block else "latest",
        ).get_all_entries()

        addresses = set()
        for event in deposits + withdraws:
            addresses.add(event.address)
            addresses.add(event.args.account)  # TODO: do we need both?

        return list(addresses)

    def get(self, block, min_power=0, csv_dump=False):
        """Get voting power per holder"""
        if "ethereum" in self.contract_manager.skip_chains:
            print("Warning: Missing ETHEREUM_RPC. Skipping call to Ethereum chain")
            return {}

        if block == "latest":
            block = self.contract_manager.apis["ethereum"].eth.get_block("latest").number

        holders = self._get_veolas_holders(block)

        address_to_votes = {
            address: self.wveolas.functions.getPastVotes(address, block).call() / 1e18
            for address in holders
        }

        address_to_votes = {k: v for k, v in address_to_votes.items() if v >= min_power}

        if csv_dump:
            self.dump(address_to_votes)

        return address_to_votes

    def dump(self, address_to_votes):
        """Write to csv"""
        with open("veolas_power.csv", "w") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["address", "veolas_power"])
            writer.writerows(list(address_to_votes.items()))
