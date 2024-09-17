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

import csv
from pathlib import Path


ALPINE_DEPLOYMENT_BLOCK = 32120064
EVEREST_DEPLOYMENT_BLOCK = 30758378
COASTAL_DEPLOYMENT_BLOCK = 33590123
BETA_HOBBYIST_DEPLOYMENT_BLOCK = 35214054
BETA_HOBBYIST_2_DEPLOYMENT_BLOCK = 35709986
BETA_EXPERT_DEPLOYMENT_BLOCK = 35214122
BETA_EXPERT_2_DEPLOYMENT_BLOCK = 35708126
BETA_EXPERT_3_DEPLOYMENT_BLOCK = 35708584


class StakingProgramme:
    """StakingProgramme"""

    def __init__(
        self, contract_manager, staking_contract_name, deployment_block=0
    ) -> None:
        """Initializer"""
        self.contract_manager = contract_manager
        self.staking_contract_name = staking_contract_name
        if "gnosis" not in self.contract_manager.skip_chains:
            self.gnosis_service_registry = contract_manager.contracts["gnosis"][
                "registries"
            ]["service_registry"]
            self.staking_contract = contract_manager.contracts["gnosis"]["staking"][
                staking_contract_name
            ]
        self.deployment_block = deployment_block

    def get(self, block=None, csv_dump=False):
        """Get"""
        if "gnosis" in self.contract_manager.skip_chains:
            print("Warning: Missing GNOSIS_RPC. Skipping call to Gnosis chain")
            return []

        if block == "latest":
            block = self.contract_manager.apis["gnosis"].eth.get_block("latest").number

        stakes = self.contract_manager.get_events(
            "gnosis",
            self.staking_contract,
            "ServiceStaked",
            self.deployment_block,
            block,
        )

        staking_owners = list(set(stake.args.owner for stake in stakes))

        if csv_dump:
            self.dump(staking_owners)

        return staking_owners

    def dump(self, staking_owners):
        """Write to csv"""
        with open(
            Path("data", f"{self.staking_contract_name}_stakers.csv"), "w"
        ) as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["address"])
            writer.writerows([[owner] for owner in staking_owners])


class Alpine(StakingProgramme):
    """Alpine"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "alpine", ALPINE_DEPLOYMENT_BLOCK)


class Everest(StakingProgramme):
    """Everest"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "everest", EVEREST_DEPLOYMENT_BLOCK)


class Coastal(StakingProgramme):
    """Coastal"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "coastal", COASTAL_DEPLOYMENT_BLOCK)


class BetaHobbyist(StakingProgramme):
    """Beta Hobbyist"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "beta_hobbyist", BETA_HOBBYIST_DEPLOYMENT_BLOCK)


class BetaHobbyist2(StakingProgramme):
    """Beta Hobbyist 2"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "beta_hobbyist_2", BETA_HOBBYIST_2_DEPLOYMENT_BLOCK)


class BetaExpert(StakingProgramme):
    """Beta Expert"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "beta_expert", BETA_EXPERT_DEPLOYMENT_BLOCK)


class BetaExpert2(StakingProgramme):
    """Beta Expert 2"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "beta_expert_2", BETA_EXPERT_2_DEPLOYMENT_BLOCK)


class BetaExpert3(StakingProgramme):
    """Beta Expert 3"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        super().__init__(contract_manager, "beta_expert_3", BETA_EXPERT_3_DEPLOYMENT_BLOCK)


class Stakers:
    """Stakers"""

    def __init__(self, contract_manager) -> None:
        """Initializer"""
        self.alpine = Alpine(contract_manager)
        self.everest = Everest(contract_manager)
        self.coastal = Coastal(contract_manager)
        self.beta_hobbyist = BetaHobbyist(contract_manager)
        self.beta_hobbyist_2 = BetaHobbyist2(contract_manager)
        self.beta_expert = BetaExpert(contract_manager)
        self.beta_expert_2 = BetaExpert2(contract_manager)
        self.beta_expert_3 = BetaExpert3(contract_manager)
