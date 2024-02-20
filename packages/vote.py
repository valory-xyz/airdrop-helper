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

"""Vote"""

import os

import requests
from packages.snapshot import queries


HTTP_OK = 200


class Voters:
    """Voters"""

    def __init__(self) -> None:
        """Initializer"""
        self.snapshot = Snapshot()
        self.boardroom = Boardroom()


class Snapshot:
    """Snapshot"""

    def _get_votes(self):
        """Get votes"""
        step = 200
        i = 0
        votes = []

        while True:
            variables = {"first": step, "skip": step * i, "space_in": ["autonolas.eth"]}

            response = requests.post(
                "https://hub.snapshot.org/graphql?",
                json={
                    "query": queries.olas_votes_query,
                    "variables": variables,
                    "operationName": "Votes",
                },
            )

            if response.status_code != HTTP_OK:
                raise ValueError

            new_votes = response.json()["data"]["votes"]

            if not new_votes:
                break

            votes.extend(new_votes)
            i += 1

        return votes

    def get(self, min_votes=None):
        """Get"""
        votes = self._get_votes()
        address_to_votes = {}
        for vote in votes:
            address_to_votes[vote["voter"]] = address_to_votes.get(vote["voter"], 0) + 1
        return (
            {k: v for k, v in address_to_votes.items() if v >= min_votes}
            if min_votes
            else address_to_votes
        )


class Boardroom:
    """Boardroom"""

    def _get_votes(self):
        """Get voters"""

        api_key = os.getenv("BOARDROOM_API_KEY")
        endpoint_base = f"https://api.boardroom.info/v1/protocols/autonolas/voters?key={api_key}&limit=100"
        cursor = None
        votes = []

        while True:
            endpoint = endpoint_base + f"&cursor={cursor}" if cursor else endpoint_base
            response = requests.get(endpoint)

            if response.status_code != HTTP_OK:
                raise ValueError

            new_votes = response.json()["data"]
            votes.extend(new_votes)

            if "nextCursor" not in response.json():
                break

            cursor = response.json()["nextCursor"]

        return votes

    def get(self, min_votes=None):
        """Get"""
        votes = self._get_votes()
        address_to_votes = {
            vote["address"]: vote["protocols"][0]["totalVotesCast"] for vote in votes
        }
        return (
            {k: v for k, v in address_to_votes.items() if v >= min_votes}
            if min_votes
            else address_to_votes
        )
