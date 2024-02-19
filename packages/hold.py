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

from web3 import Web3
import os
from constants import VEOLAS, WVEOLAS
import json
from pathlib import Path


class veOLAS:
    """veOLAS"""

    def __init__(self) -> None:
        self.api = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC")))
        with open(Path("packages", "contracts", "veolas.json"), "r") as abi_file:
            abi = json.load(abi_file)
        self.veolas = self.api.eth.contract(address=Web3.to_checksum_address(VEOLAS), abi=abi)
        with open(Path("packages", "contracts", "wveolas.json"), "r") as abi_file:
            abi = json.load(abi_file)
        self.wveolas = self.api.eth.contract(address=Web3.to_checksum_address(WVEOLAS), abi=abi)

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


    def get(self, block):
        """Get voting power per holder"""
        holders = self._get_veolas_holders(block)
        return {
            address: self.wveolas.functions.getPastVotes(address, block).call() / 1e18 for address in holders
        }
