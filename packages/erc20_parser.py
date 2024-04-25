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

"""ERC20Parser"""

import bisect
import csv
import json
import os
from collections import OrderedDict
from pathlib import Path

from web3.exceptions import BadResponseFormat


class ERC20Parser:
    """ERC20Parser"""

    BLOCK_RANGE = 2000  # this range lets us avoid event limits on RPC response, and therefore pagination
    DUMP_THRESHOLD = 1000
    EVENTS_CSV_FILE = Path("data", "events.csv")
    BALANCES_JSON_FILE = Path("data", "balances.json")

    def __init__(self, contract) -> None:
        """ERC20 history"""
        self.contract = contract
        self.event_queue = []
        self.balances = {}
        self.header_written = False
        self.events_file_exist = os.path.isfile(self.EVENTS_CSV_FILE)

    def parse_transfer_events(self, from_block, to_block, address=None):
        """Parse transfer events"""

        for block in range(from_block, to_block, self.BLOCK_RANGE):
            percent = 100 * (block - from_block) / (to_block - from_block)
            while True:
                print(
                    f"Parsing blocks {from_block} to {to_block}: batch {block} to {block + self.BLOCK_RANGE} [{percent:0.2f}%]"
                )
                try:
                    # Single address
                    if address:
                        events = self.contract.events.Transfer().get_logs(
                            fromBlock=block,
                            toBlock=block + self.BLOCK_RANGE,
                            argument_filters={"from": address},
                        )
                        events += self.contract.events.Transfer().get_logs(
                            fromBlock=block,
                            toBlock=block + self.BLOCK_RANGE,
                            argument_filters={"to": address},
                        )
                    # All addresses
                    else:
                        events = self.contract.events.Transfer().get_logs(
                            fromBlock=block, toBlock=block + self.BLOCK_RANGE
                        )
                    break
                except BadResponseFormat as e:
                    print(f"BadResponseFormat exception:\n{e}.\nRetrying...")
                except ValueError as e:
                    print(f"ValueError exception:\n{e}\nRetrying...")

            self.event_queue += [
                dict(e.args)
                | {
                    "block": e.blockNumber,
                    "tx_hash": e.transactionHash.hex(),
                    "tx_index": e.transactionIndex,
                    "log_index": e.logIndex,
                }
                for e in events
            ]
            if len(self.event_queue) >= self.DUMP_THRESHOLD:
                self.store_events()

        self.store_events()

    def store_events(self):
        """Store transfer events"""
        with open(self.EVENTS_CSV_FILE, "a") as event_file:
            writer = csv.writer(event_file, quoting=csv.QUOTE_NONNUMERIC)
            header = [
                "block",
                "from",
                "to",
                "amount",
                "tx_hash",
                "tx_index",
                "log_index",
            ]
            if not self.events_file_exist and not self.header_written:
                writer.writerow(header)
                self.header_written = True
            writer.writerows([[e[field] for field in header] for e in self.event_queue])
            print(f"Dumped {len(self.event_queue)} events to file")
        self.event_queue = []

    def sort_events(self):
        """Sort the events file"""
        with open(self.EVENTS_CSV_FILE, "r") as event_file:
            csv_reader = csv.DictReader(event_file)
            event_list = list(csv_reader)

        # Sort by block
        event_list.sort(key=lambda e: int(e["block"]))

        # Sort by tx index
        block_events = []
        sorted_events = []
        for event in event_list:
            if not block_events:
                block_events.append(event)
                continue

            # Pack txs from the same block together
            if event["block"] == block_events[0]["block"]:
                block_events.append(event)
                continue

            # Block change: sort by tx_index, log_index
            block_events.sort(key=lambda e: (int(e["tx_index"]), int(e["log_index"])))
            sorted_events += block_events
            block_events = [event]

        with open(self.EVENTS_CSV_FILE, "w") as event_file:
            csv_writer = csv.DictWriter(
                event_file, fieldnames=list(sorted_events[0].keys())
            )
            csv_writer.writeheader()
            csv_writer.writerows(sorted_events)

    def clean_event_duplications(self):
        """Remove event duplications from the event file"""

        with open(self.EVENTS_CSV_FILE, "r") as event_file:
            lines = event_file.readlines()

        clean_lines = []
        block_events = []
        current_block = None

        header = lines.pop(0)

        for line in lines:
            block = line.split(",")[0]

            # Block change
            if current_block and block != current_block:
                block_events = []

            # Add unique lines
            if line not in block_events:
                clean_lines.append(line)

            block_events.append(line)

            current_block = block

        with open(self.EVENTS_CSV_FILE, "w") as event_file:
            event_file.write(header)
            event_file.writelines(clean_lines)

    def load_events(self):
        """Load transfer events"""
        with open(self.EVENTS_CSV_FILE, "r") as event_file:
            csv_reader = csv.DictReader(event_file)
            event_list = list(csv_reader)
            event_list.sort(key=lambda e: int(e["block"]))
            return event_list

    def build_balance_history(self):
        """Store transfer events"""
        events = self.load_events()

        for e in events:
            block = int(e["block"])
            from_address = e["from"]
            to_address = e["to"]
            amount = int(e["amount"])

            if from_address not in self.balances:
                self.balances[from_address] = OrderedDict({block: -amount})
            else:
                last_block = next(reversed(self.balances[from_address]))
                self.balances[from_address][block] = (
                    self.balances[from_address][last_block] - amount
                )

            if to_address not in self.balances:
                self.balances[to_address] = OrderedDict({block: amount})
            else:
                last_block = next(reversed(self.balances[to_address]))
                self.balances[to_address][block] = (
                    self.balances[to_address][last_block] + amount
                )

        with open(self.BALANCES_JSON_FILE, "w") as balance_file:
            json.dump(self.balances, balance_file, indent=4)

    def get_balance(self, address, block):
        """Get address balance at a given block"""

        if not self.balances:
            raise ValueError("The build_balance_history method must be called first")

        if address not in self.balances:
            return 0

        if block in self.balances[address]:
            return self.balances[address][block]

        block_list = list(self.balances[address].keys())

        if block < block_list[0]:
            return 0

        if block > block_list[-1]:
            return self.balances[address][block_list[-1]]

        position = bisect.bisect_left(block_list, block)
        block = block_list[position - 1]
        return self.balances[address][block]

    def balance_check_range(self, address, min_balance_wei, from_block, to_block):
        """Verify that a given address has maintained a minimum balance in a block range"""

        if not self.balances:
            raise ValueError("The build_balance_history method must be called first")

        if address not in self.balances:
            return False

        # Get the block range to check from the balance list
        block_list = list(self.balances[address].keys())
        from_position = bisect.bisect_left(block_list, from_block)
        to_position = bisect.bisect_left(block_list, to_block)
        blocks = block_list[from_position:to_position]

        # Check the balance during all the block range
        for block in blocks:
            if self.balances[address][block] < min_balance_wei:
                return False
        return True

    def balance_check_block(self, address, min_balance_wei, block):
        """Verify that a given address has maintained a minimum balance at a given block"""

        if not self.balances:
            raise ValueError("The build_balance_history method must be called first")

        if address not in self.balances:
            return False

        # Get the block range to check from the balance list
        block_list = list(self.balances[address].keys())
        block_position = bisect.bisect_left(block_list, block)
        target_block = block_list[block_position - 1]

        return self.balances[address][target_block] >= min_balance_wei
