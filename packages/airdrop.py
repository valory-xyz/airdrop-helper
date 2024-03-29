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

from packages.olas import Olas
import csv

class Airdrop():
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
        block = self.parameters["block"]

        # Contribute
        weight = self.parameters["weight_per_contributor"]

        if weight:
            print("Collecting contributors...")

            contributors = self.olas.contributors.get(
                min_points=self.parameters["min_contribute_points"]
            )

            for c in contributors:
                self.add_weight(c["wallet_address"], weight)

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
        weight = self.parameters["weight_per_holder"]

        if weight:
            print("Collecting veOLAS holders...")

            veolas_holders = self.olas.veolas_holders.get(
                block=block, min_power=self.parameters["min_voting_power"]
            )

            for address in veolas_holders.keys():
                self.add_weight(address, weight)

        # Bonders
        weight = self.parameters["weight_per_bonder"]

        if weight:
            print("Collecting bonders...")

            bonders = self.olas.bonders.get(
                block=block,
                min_amount=self.parameters["min_bond_amount"]
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
            alpine_stakers = self.olas.stakers.alpine.get(block=block)

            print("Collecting Everest stakers...")
            everest_stakers = self.olas.stakers.everest.get(block=block)

            for address in alpine_stakers + everest_stakers:
                self.add_weight(address, weight)

        # Calculate rewards
        allocation_per_weight = self.parameters["token_allocation_per_weight_unit"]
        rewards = {k: v * allocation_per_weight for k, v in self.weights.items()}

        # Sort by reward
        rewards = dict(sorted(rewards.items(), key=lambda x:x[1], reverse=True))

        if csv_dump:
            self.dump(rewards)

        return rewards

    def dump(self, rewards):
        """Write to csv"""
        with open("airdrop.csv", "w") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["address", "allocation"])
            writer.writerows(list(rewards.items()))