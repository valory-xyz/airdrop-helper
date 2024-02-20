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

"""Bond"""


class Bonders:
    """Bonders"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        self.contract_manager = contract_manager
        if "ethereum" not in self.contract_manager.skip_chains:
            self.depository = contract_manager.contracts["ethereum"]["other"][
                "depository"
            ]

    def get(self, block=None, min_amount=None):
        """Get"""
        if "ethereum" in self.contract_manager.skip_chains:
            print("Warning: Missing ETHEREUM_RPC. Skipping call to Ethereum chain")
            return {}

        deposits = self.depository.events.CreateBond.create_filter(
            fromBlock="earliest",
            toBlock=block if block else "latest",
        ).get_all_entries()

        address_to_amount = {}
        for deposit in deposits:
            owner = deposit.args.owner
            address_to_amount[owner] = (
                address_to_amount.get(owner, 0) + deposit.args.amountOLAS / 1e18
            )

        return (
            {k: v for k, v in address_to_amount.items() if v >= min_amount}
            if min_amount
            else address_to_amount
        )
