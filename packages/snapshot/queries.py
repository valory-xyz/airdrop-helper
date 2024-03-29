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

"""Snapshot queries"""

olas_space_query = """
{
  space(id: "autonolas.eth") {
    id
    name
    about
    network
    symbol
    members
  }
}
"""

olas_proposals_query = """
query Proposals(
  $first: Int
  $skip: Int
  $state: String
  $space_in: [String]
) {
  proposals (
    first: $first,
    skip: $skip,
    where: {
      state: $state,
      space_in: $space_in
    }
  ) {
    id
    network
    title
    snapshot
    state
  }
}
"""

olas_votes_query = """
query Votes(
  $first: Int
  $skip: Int
  $space_in: [String]
) {
  votes (
    first: $first,
    skip: $skip,
    where: {
      space_in: $space_in
    }
    orderBy: "created"
    orderDirection: desc
  ) {
    id
    voter
    vp
    proposal {
      id
    }
    space {
      id
    }
  }
}
"""
