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

"""Tests and examples"""

from olas import Olas
import json

olas = Olas()

# Contribute
contributors = olas.contributors.get(min_points=50000)
print("\nContributors\n", json.dumps(contributors, indent=4))

# Snapshot votes
snapshot_voters = olas.voters.snapshot.get(min_votes=3)
print("\nSnapshot voters\n", json.dumps(snapshot_voters, indent=4))

# Boardroom votes - requires an API key to be set in a .env file
boardroom_voters = olas.voters.boardroom.get()
print("\nBoardroom voters\n", json.dumps(boardroom_voters, indent=4))