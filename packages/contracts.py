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

from eth_abi.exceptions import InsufficientDataBytes
from web3 import Web3

from packages.constants import CONTRACTS


MAX_BLOCKS = 5000


class ContractManager:
    """ContractManager"""

    def __init__(self) -> None:
        """Initializer"""
        self.apis = {}
        self.contracts = {}

        # Load apis
        missing_rpcs = {}
        for chain_name in CONTRACTS.keys():
            # Skip Solana for now
            if chain_name in ["solana"]:
                continue

            rpc_var_name = f"{chain_name.upper()}_RPC"
            rpc = os.getenv(rpc_var_name)

            if not rpc:
                missing_rpcs[chain_name] = rpc_var_name
                continue

            self.apis[f"{chain_name}"] = Web3(Web3.HTTPProvider(rpc))

        # Warn about missing rpcs
        self.skip_chains = []
        if missing_rpcs:
            self.skip_chains = list(missing_rpcs.keys())
            print(
                f"WARNING: the env vars {list(missing_rpcs.values())} have not been set. Calls to {self.skip_chains} chains will be skipped."
            )
            input("Press enter key to continue...")

        # Skip Solana for now
        self.skip_chains.append("solana")

        # Load contracts
        for chain_name, contract_group in CONTRACTS.items():
            # Skip chains without an RPC
            if chain_name in self.skip_chains:
                continue
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

    def get_events(self, chain, contract, event, start_block, end_block=None):
        """Get events"""
        if chain in self.skip_chains:
            return []

        if not end_block:
            latest_block = self.apis[chain].eth.get_block("latest").number
        else:
            latest_block = end_block

        events = []
        from_block = start_block

        print(
            f"Requested events from blocks {start_block} to {latest_block} [{latest_block - start_block} blocks]"
        )

        while True:
            to_block = latest_block

            if to_block - from_block > MAX_BLOCKS:
                to_block = from_block + MAX_BLOCKS

            if to_block > latest_block:
                to_block = latest_block

            print(f"  Parsing batch {from_block} to {to_block}...")
            try:
                new_events = (
                    getattr(contract.events, event)
                    .create_filter(
                        fromBlock=from_block,
                        toBlock=to_block,
                    )
                    .get_all_entries()
                )
            except InsufficientDataBytes:
                print("InsufficientDataBytes exception. Retrying...")
                continue
            except ValueError:
                print("ValueError exception. Retrying...")
                continue
            except OverflowError:
                print("OverflowError exception. Retrying...")
                continue

            events.extend(new_events)
            from_block = to_block

            if from_block >= latest_block:
                break

        return events
