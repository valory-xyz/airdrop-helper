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

"""Stake"""

ALPINE_DEPLOYMENT_BLOCK = 32121777
EVEREST_DEPLOYMENT_BLOCK = 30758378


class Stakers:
    """Stakers"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        self.contract_manager = contract_manager
        if "gnosis" not in self.contract_manager.skip_chains:
            self.alpine = contract_manager.contracts["gnosis"]["staking"]["alpine"]
            self.everest = contract_manager.contracts["gnosis"]["staking"]["everest"]
            self.gnosis_service_registry = contract_manager.contracts["gnosis"][
                "registries"
            ]["service_registry"]

    def get(self, block=None):
        """Get"""
        if "gnosis" in self.contract_manager.skip_chains:
            print("Warning: Missing GNOSIS_RPC. Skipping call to Gnosis chain")
            return []

        alpine_stakes = self.contract_manager.get_events(
            "gnosis", self.alpine, "ServiceStaked", ALPINE_DEPLOYMENT_BLOCK, block
        )
        everest_stakes = self.contract_manager.get_events(
            "gnosis", self.everest, "ServiceStaked", EVEREST_DEPLOYMENT_BLOCK, block
        )

        staking_owners = list(
            set(stake.args.owner for stake in alpine_stakes + everest_stakes)
        )
        return staking_owners
