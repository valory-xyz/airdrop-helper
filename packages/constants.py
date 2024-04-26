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
        "other": {"olas": "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f"},
    },
    "polygon": {
        "registries": {
            "service_registry": "0xE3607b00E75f6405248323A9417ff6b39B244b50"
        },
        "other": {"olas": "0xFEF5d947472e72Efbb2E388c730B7428406F2F95"},
    },
    "arbitrum": {
        "registries": {
            "service_registry": "0xE3607b00E75f6405248323A9417ff6b39B244b50"
        },
        "other": {"olas": "0x064f8b858c2a603e1b106a2039f5446d32dc81c1"},
    },
    "solana": {
        "registries": {
            "service_registry": "AU428Z7KbjRMjhmqWmQwUta2AvydbpfEZNBh8dStHTDi"
        },
        "other": {"olas": ""},
    },
    "optimism": {
        "registries": {
            "service_registry": "0x3d77596beb0f130a4415df3D2D8232B3d3D31e44"
        },
        "other": {"olas": "0xFC2E6e6BCbd49ccf3A5f029c79984372DcBFE527"},
    },
    "base": {
        "registries": {
            "service_registry": "0x3C1fF68f5aa342D296d4DEe4Bb1cACCA912D95fE"
        },
        "other": {"olas": "0x54330d28ca3357F294334BDC454a032e7f353416"},
    },
}
