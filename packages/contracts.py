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

"""Contracts"""

import json
import os
from pathlib import Path

from constants import CONTRACTS
from web3 import Web3


class ContractManager:
    def __init__(self) -> None:
        """Initializer"""
        self.apis = {}
        self.contracts = {}

        # Load apis
        for chain_name in CONTRACTS.keys():
            self.apis[f"{chain_name}"] = Web3(
                Web3.HTTPProvider(os.getenv(f"{chain_name.upper()}_RPC"))
            )

        # Load contracts
        for chain_name, contract_group in CONTRACTS.items():
            self.contracts[chain_name] = {}
            for group_name, contracts in contract_group.items():
                self.contracts[chain_name][group_name] = {}
                for contract_name, contract_address in contracts.items():
                    with open(
                        Path("packages", "contracts", f"{contract_name}.json"), "r"
                    ) as abi_file:
                        abi = json.load(abi_file)
                        self.contracts[chain_name][group_name][
                            contract_name
                        ] = self.apis[chain_name].eth.contract(
                            address=Web3.to_checksum_address(contract_address), abi=abi
                        )
