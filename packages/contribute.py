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

"""Contribute"""

import csv
import json
from packages.ceramic.ceramic import Ceramic
from packages.constants import CONTRIBUTE_DB_STREAM_ID


class Contributors:
    """Contribute"""

    def __init__(self) -> None:
        """Initializer"""
        self.ceramic = Ceramic(Ceramic.HIRENODES)

    def get(self, min_points=None, csv_dump=False):
        """Get contributors"""
        data, _, _ = self.ceramic.get_data(CONTRIBUTE_DB_STREAM_ID)
        users = (
            list(filter(lambda u: u["points"] >= min_points, data["users"]))
            if min_points
            else data["users"]
        )

        points = [u["points"] for u in users]
        points_min = min(points)
        points_max = max(points)

        for user in users:
            del user["tweet_id_to_points"]
            del user["current_period_points"]
            # Calculate the user decile
            decile = int((user["points"] - points_min) / (points_max - points_min) / 0.1)
            user["point_multiplier"] = 1 + decile
        if csv_dump:
            self.dump(users)

        return users

    def dump(self, users):
        """Write to csv"""
        with open("contributors.csv", "w") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["twitter_handle", "discord_handle", "address", "points"])
            writer.writerows(
                [
                    [
                        user["twitter_handle"],
                        user["discord_handle"],
                        user["wallet_address"],
                        user["points"],
                    ]
                    for user in users
                ]
            )

        with open("contributors.json", "w") as file:
            json.dump(users, file, indent=4)