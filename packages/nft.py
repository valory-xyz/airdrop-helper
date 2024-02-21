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
import csv

from packages.constants import CONTRACTS


class NFT:
    """NFT"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        self.contract_manager = contract_manager
        self.contracts = contract_manager.contracts

    def get(self, csv_dump=False):
        """Get"""
        address_to_tokens = {}
        for chain_name, contract_group in CONTRACTS.items():
            if chain_name in self.contract_manager.skip_chains:
                print(
                    f"Warning: Missing {chain_name.upper()}_RPC. Skipping call to {chain_name} chain"
                )
                continue

            for contract_name in contract_group["registries"].keys():
                contract = self.contracts[chain_name]["registries"][contract_name]
                n_tokens = contract.functions.totalSupply().call()
                for token_id in range(1, n_tokens + 1):
                    owner_address = contract.functions.ownerOf(token_id).call()
                    if owner_address not in address_to_tokens:
                        address_to_tokens[owner_address] = {
                            chain: 0 for chain in CONTRACTS.keys()
                        }
                    address_to_tokens[owner_address][chain_name] += 1

        if csv_dump:
            self.dump(address_to_tokens)

        return address_to_tokens

    def dump(self, address_to_tokens):
        """Write to csv"""
        with open("nft_holders.csv", "w") as file:
            chains = list(self.contracts.keys())
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["address"] + [f"{chain}_nfts" for chain in chains])
            writer.writerows(
                [
                    [k] + [v[chain] for chain in chains]
                    for k, v in address_to_tokens.items()
                ]
            )
