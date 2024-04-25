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

"""Constants"""

CONTRIBUTE_DB_STREAM_ID = (
    "kjzl6cwe1jw148mppot8a8vtq8glw5km6djc8dbfj4q0sztpqd0h05a2m5zsgp6"
)

CONTRACTS = {
    "ethereum": {
        "registries": {
            "component_registry": "0x15bd56669F57192a97dF41A2aa8f4403e9491776",
            "agent_registry": "0x2F1f7D38e4772884b88f3eCd8B6b9faCdC319112",
            "service_registry": "0x48b6af7B12C71f09e2fC8aF4855De4Ff54e775cA",
        },
        "other": {
            "veolas": "0x7e01a500805f8a52fad229b3015ad130a332b7b3",
            "olas": "0x0001A500A6B18995B03f44bb040A5fFc28E45CB0",
            "wveolas": "0x4039B809E0C0Ad04F6Fc880193366b251dDf4B40",
            "depository": "0xfF8697d8d2998d6AA2e09B405795C6F4BEeB0C81",
        },
    },
    "gnosis": {
        "registries": {
            "service_registry": "0x9338b5153AE39BB89f50468E608eD9d764B755fD"
        },
        "staking": {
            "alpine": "0x2Ef503950Be67a98746F484DA0bBAdA339DF3326",
            "everest": "0x5add592ce0a1B5DceCebB5Dcac086Cd9F9e3eA5C",
        },
    },
    "polygon": {
        "registries": {"service_registry": "0xE3607b00E75f6405248323A9417ff6b39B244b50"}
    },
    "arbitrum": {
        "registries": {"service_registry": "0xE3607b00E75f6405248323A9417ff6b39B244b50"}
    },
    "solana": {
        "registries": {
            "service_registry": "AU428Z7KbjRMjhmqWmQwUta2AvydbpfEZNBh8dStHTDi"
        }
    },
}
