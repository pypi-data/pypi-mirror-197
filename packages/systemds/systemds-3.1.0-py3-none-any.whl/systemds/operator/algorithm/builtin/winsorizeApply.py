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
# Autogenerated From : scripts/builtin/winsorizeApply.dml

from typing import Dict, Iterable

from systemds.operator import OperationNode, Matrix, Frame, List, MultiReturn, Scalar
from systemds.script_building.dag import OutputType
from systemds.utils.consts import VALID_INPUT_TYPES


def winsorizeApply(X: Matrix,
                   qLower: Matrix,
                   qUpper: Matrix):
    """
     winsorizeApply takes the upper and lower quantile values per column, and
     remove outliers by replacing them with these upper and lower bound values.
    
    
    
    :param X: Input feature matrix
    :param qLower: row vector of upper bounds per column
    :param qUpper: row vector of lower bounds per column
    :return: Matrix without outlier values
    """

    params_dict = {'X': X, 'qLower': qLower, 'qUpper': qUpper}
    return Matrix(X.sds_context,
        'winsorizeApply',
        named_input_nodes=params_dict)
