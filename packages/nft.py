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

"""NFT"""
from constants import CONTRACTS


class NFT:

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        self.contracts = contract_manager.contracts

    def get(self):
        """Get"""
        address_to_tokens = {}
        for chain_name, contract_group in CONTRACTS.items():
            for contract_name in contract_group["registries"].keys():
                contract = self.contracts[chain_name]["registries"][contract_name]
                n_tokens = contract.functions.totalSupply().call()
                for token_id in range(1, n_tokens + 1):
                    owner_address = contract.functions.ownerOf(token_id).call()
                    if owner_address not in address_to_tokens:
                        address_to_tokens[owner_address] = {chain: 0 for chain in CONTRACTS.keys()}
                    address_to_tokens[owner_address][chain_name] += 1
        return address_to_tokens
