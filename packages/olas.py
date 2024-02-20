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

"""Olas"""

from bond import Bonders
from contracts import ContractManager
from contribute import Contributors
from dotenv import load_dotenv
from hold import veOLAS
from nft import NFT
from stake import Stakers
from vote import Voters


class Olas:

    def __init__(self) -> None:
        """Initializer"""
        load_dotenv()
        self.contract_manager = ContractManager()
        self.contributors = Contributors()
        self.voters = Voters()
        self.veolas_holders = veOLAS(self.contract_manager)
        self.bonders = Bonders(self.contract_manager)
        self.nft_owners = NFT(self.contract_manager)
        self.stakers = Stakers(self.contract_manager)


