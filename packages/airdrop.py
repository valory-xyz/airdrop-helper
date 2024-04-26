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

"""Airdrop"""

import csv
from pathlib import Path

from packages.olas import Olas


class Airdrop:
    """Airdrop"""

    def __init__(self, parameters) -> None:
        """Init"""
        self.olas = Olas()
        self.parameters = parameters
        self.weights = {}

    def add_weight(self, address, weight):
        """Add weight"""
        if not address:
            return
        if address in self.parameters["skip_wallets"]:
            return
        self.weights[address] = self.weights.get(address, 0) + weight

    def calculate(self, csv_dump=False):
        """Calculate"""
        blocks = self.parameters["blocks"]

        # Contribute
        weight = self.parameters["weight_per_contributor"]
        use_decile_based_multiplier = self.parameters["use_decile_based_multiplier"]

        if weight:
            print("Collecting contributors...")

            contributors = self.olas.contributors.get(
                min_points=self.parameters["min_contribute_points"]
            )

            for c in contributors:
                point_multiplier = (
                    c["point_multiplier"] if use_decile_based_multiplier else 1
                )
                self.add_weight(
                    c["wallet_address"], weight * c["points"] * point_multiplier
                )

        # Snapshot
        weight = self.parameters["weight_per_vote"]

        if weight:
            print("Collecting Snapshot voters...")

            snapshot_voters = self.olas.voters.snapshot.get(
                min_votes=self.parameters["min_votes"],
            )

            for address, votes in snapshot_voters.items():
                self.add_weight(address, votes * weight)

        # Boardroom
        weight = self.parameters["weight_per_vote"]

        if weight:
            print("Collecting Boardroom voters...")

            boardroom_voters = self.olas.voters.boardroom.get(
                min_votes=3,
            )

            for address, votes in boardroom_voters.items():
                self.add_weight(address, votes * weight)

        # veOLAS holders
        weight = self.parameters["weight_per_veolas_holder"]

        if weight:
            print("Collecting veOLAS holders...")

            veolas_holders = self.olas.veolas_holders.get(
                block=blocks["ethereum"], min_power=self.parameters["min_voting_power"]
            )

            for address in veolas_holders.keys():
                self.add_weight(address, weight)

        # OLAS holders
        weight = self.parameters["weight_per_olas_holder"]

        if weight:
            print("Collecting OLAS holders...")

            olas_holders = self.olas.olas_holders.get(
                block=blocks, min_balance_wei=self.parameters["min_olas_balance_wei"]
            )

            for address, balance in olas_holders.items():
                multiplier = 1 if self.parameters["constant_reward"] else balance / 1e18
                self.add_weight(address, weight * multiplier)

        # Bonders
        weight = self.parameters["weight_per_bonder"]

        if weight:
            print("Collecting bonders...")

            bonders = self.olas.bonders.get(
                block=blocks["ethereum"], min_amount=self.parameters["min_bond_amount"]
            )

            for address in bonders.keys():
                self.add_weight(address, weight)

        # NFT owners
        weight = self.parameters["weight_per_nft_owner"]

        if weight:
            print("Collecting component NFT holders...")

            nft_holders = self.olas.nft_owners.get()

            for address, data in nft_holders.items():
                for nfts in data.values():
                    self.add_weight(address, nfts * weight)

        # Stakers
        weight = self.parameters["weight_per_staker"]

        if weight:
            print("Collecting Alpine stakers...")
            alpine_stakers = self.olas.stakers.alpine.get(block=blocks["ethereum"])

            print("Collecting Everest stakers...")
            everest_stakers = self.olas.stakers.everest.get(block=blocks["ethereum"])

            for address in alpine_stakers + everest_stakers:
                self.add_weight(address, weight)

        # Calculate rewards
        allocation_per_weight = self.parameters["token_allocation_per_weight_unit"]
        rewards = {k: v * allocation_per_weight for k, v in self.weights.items()}

        # Sort by reward
        rewards = dict(sorted(rewards.items(), key=lambda x: x[1], reverse=True))

        if csv_dump:
            self.dump(rewards)

        return rewards

    def dump(self, rewards):
        """Write to csv"""
        with open(Path("data", "airdrop.csv"), "w") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["address", "allocation"])
            writer.writerows(list(rewards.items()))
