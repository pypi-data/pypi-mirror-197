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
# Autogenerated From : scripts/builtin/decisionTree.dml

from typing import Dict, Iterable

from systemds.operator import OperationNode, Matrix, Frame, List, MultiReturn, Scalar
from systemds.script_building.dag import OutputType
from systemds.utils.consts import VALID_INPUT_TYPES


def decisionTree(X: Matrix,
                 Y: Matrix,
                 R: Matrix,
                 **kwargs: Dict[str, VALID_INPUT_TYPES]):
    """
     Builtin script implementing classification trees with scale and categorical features
    
    
    
    :param X: Feature matrix X; note that X needs to be both recoded and dummy coded
    :param Y: Label matrix Y; note that Y needs to be both recoded and dummy coded
    :param R: Matrix R which for each feature in X contains the following information
        - R[1,]: Row Vector which indicates if feature vector is scalar or categorical. 1 indicates
        a scalar feature vector, other positive Integers indicate the number of categories
        If R is not provided by default all variables are assumed to be scale
    :param bins: Number of equiheight bins per scale feature to choose thresholds
    :param depth: Maximum depth of the learned tree
    :param verbose: boolean specifying if the algorithm should print information while executing
    :return: Matrix M where each column corresponds to a node in the learned tree and each row
        contains the following information:
        M[1,j]: id of node j (in a complete binary tree)
        M[2,j]: Offset (no. of columns) to left child of j if j is an internal node, otherwise 0
        M[3,j]: Feature index of the feature (scale feature id if the feature is scale or
        categorical feature id if the feature is categorical)
        that node j looks at if j is an internal node, otherwise 0
        M[4,j]: Type of the feature that node j looks at if j is an internal node: holds
        the same information as R input vector
        M[5,j]: If j is an internal node: 1 if the feature chosen for j is scale,
        otherwise the size of the subset of values
        stored in rows 6,7,... if j is categorical
        If j is a leaf node: number of misclassified samples reaching at node j
        M[6:,j]: If j is an internal node: Threshold the example's feature value is compared
        to is stored at M[6,j] if the feature chosen for j is scale,
        otherwise if the feature chosen for j is categorical rows 6,7,... depict the value subset chosen for j
        If j is a leaf node 1 if j is impure and the number of samples at j > threshold, otherwise 0
    """

    params_dict = {'X': X, 'Y': Y, 'R': R}
    params_dict.update(kwargs)
    return Matrix(X.sds_context,
        'decisionTree',
        named_input_nodes=params_dict)
