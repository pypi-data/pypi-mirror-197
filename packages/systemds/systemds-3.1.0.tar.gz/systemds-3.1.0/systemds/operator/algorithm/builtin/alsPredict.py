# -------------------------------------------------------------
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# -------------------------------------------------------------

# Autogenerated By   : src/main/python/generator/generator.py
# Autogenerated From : scripts/builtin/alsPredict.dml

from typing import Dict, Iterable

from systemds.operator import OperationNode, Matrix, Frame, List, MultiReturn, Scalar
from systemds.script_building.dag import OutputType
from systemds.utils.consts import VALID_INPUT_TYPES


def alsPredict(userIDs: Matrix,
               I: Matrix,
               L: Matrix,
               R: Matrix):
    """
     This script computes the rating/scores for a given list of userIDs 
     using 2 factor matrices L and R. We assume that all users have rates 
     at least once and all items have been rates at least once.
    
    
    
    :param userIDs: Column vector of user-ids (n x 1)
    :param I: Indicator matrix user-id x user-id to exclude from scoring
    :param L: The factor matrix L: user-id x feature-id
    :param R: The factor matrix R: feature-id x item-id
    :return: The output user-id/item-id/score#
    """

    params_dict = {'userIDs': userIDs, 'I': I, 'L': L, 'R': R}
    return Matrix(userIDs.sds_context,
        'alsPredict',
        named_input_nodes=params_dict)
