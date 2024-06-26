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

"""Examples"""

import json

from packages.olas import Olas


#############################################################################
# WARNING: some of the following tools require API keys or RPCs to be set   #
# in a .env file. Please rename the sample.env file to .env and fill in the #
# RPCs/keys you need to retrieve the required data.                         #
#############################################################################

# Instantiate the Olas airdrop helper
olas = Olas()

# Get all Contribute users that have at least 50k points
contributors = olas.contributors.get(min_points=100, csv_dump=True)
print("\nContributors\n", json.dumps(contributors, indent=4))

# Get addresses that have voted at least 3 times on Snapshot
snapshot_voters = olas.voters.snapshot.get(min_votes=3, csv_dump=True)
print("\nSnapshot voters\n", json.dumps(snapshot_voters, indent=4))

# Get addresses that have voted at least 3 times on Boardroom
# Requires BOARDROOM_API_KEY to be set in the .env file
# See https://docs.boardroom.io/docs/api/cd5e0c8aa2bc1-overview#request-an-api-key
boardroom_voters = olas.voters.boardroom.get(min_votes=3, csv_dump=True)
print("\nBoardroom voters\n", json.dumps(boardroom_voters, indent=4))

# Get veOLAS holders at a given block (ignore block argument to retrieve latest) with a minimum voting power of 100
# Requires ETHEREUM_RPC to be set in the .env file
veolas_holders = olas.veolas_holders.get(block=19263301, min_power=100, csv_dump=True)
print("\nveOLAS holders\n", json.dumps(veolas_holders, indent=4))

# Get OLAS holders at a given block (ignore block argument to retrieve latest) with a minimum balance power of 100 OLAS
# Requires ETHEREUM_RPC to be set in the .env file
blocks = {
    "ethereum": 19733758,
    "arbitrum": "latest",
    "polygon": "latest",
    "gnosis": "latest",
    "base": "latest",
    "optimism": "latest",
}
olas_holders = olas.olas_holders.get(blocks=blocks, min_balance_wei=int(100e18), csv_dump=True)
print("\nOLAS holders\n", json.dumps(olas_holders, indent=4))

# Get addresses that have bonded up to a given block (ignore block argument to retrieve latest)
# Requires ETHEREUM_RPC to be set in the .env file
bonders = olas.bonders.get(block=19269490, csv_dump=True)
print("\nBonders\n", json.dumps(bonders, indent=4))

# Get service, agent and component NFT owners
# Requires RPC to be set in the .env file for all the chains you need to interact with
nft_holders = olas.nft_owners.get(csv_dump=True)
print("\nNFT owners\n", json.dumps(nft_holders, indent=4))

# Get stakers who have participated in the Alpine programme up to a given block
# Requires GNOSIS_RPC to be set in the .env file
alpine_stakers = olas.stakers.alpine.get(block=32130064, csv_dump=True)
print("\nAlpine stakers\n", json.dumps(alpine_stakers, indent=4))

# Get stakers who have participated in the Everest programme up to a given block
# Requires GNOSIS_RPC to be set in the .env file
everest_stakers = olas.stakers.everest.get(block=30768378, csv_dump=True)
print("\nEverest stakers\n", json.dumps(everest_stakers, indent=4))