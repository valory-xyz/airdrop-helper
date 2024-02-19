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

from web3 import Web3
from constants import REGISTRIES
import json
from pathlib import Path
import os

class NFT:

    def __init__(self) -> None:
        self.api = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC")))
        with open(Path("packages", "contracts", "service_registry.json"), "r") as abi_file:
            abi = json.load(abi_file)
        self.service_registry = self.api.eth.contract(address=Web3.to_checksum_address(REGISTRIES["ETHEREUM"]["SERVICE"]), abi=abi)

    def get(self):
        """Get"""
        # Services
        n_services = self.service_registry.functions.totalSupply().call()

        token_id_to_owner = {
            token_id: self.service_registry.functions.ownerOf(token_id).call() for token_id in range(1, n_services + 1)
        }

        address_to_tokens = {}
        for address in token_id_to_owner.values():
            address_to_tokens[address] = address_to_tokens.get(address, 0) + 1

        return address_to_tokens

