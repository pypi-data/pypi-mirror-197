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
# Autogenerated From : scripts/builtin/l2svm.dml

from typing import Dict, Iterable

from systemds.operator import OperationNode, Matrix, Frame, List, MultiReturn, Scalar
from systemds.script_building.dag import OutputType
from systemds.utils.consts import VALID_INPUT_TYPES


def l2svm(X: Matrix,
          Y: Matrix,
          **kwargs: Dict[str, VALID_INPUT_TYPES]):
    """
     This builting function implements binary-class Support Vector Machine (SVM)
     with squared slack variables (l2 regularization).
    
    
    
    :param X: Feature matrix X (shape: m x n)
    :param Y: Label vector y of class labels (shape: m x 1), assumed binary
        in -1/+1 or 1/2 encoding.
    :param intercept: Indicator if a bias column should be added to X and the model
    :param epsilon: Tolerance for early termination if the reduction of objective
        function is less than epsilon times the initial objective
    :param reg: Regularization parameter (lambda) for L2 regularization
    :param maxIterations: Maximum number of conjugate gradient (outer) iterations
    :param maxii: Maximum number of line search (inner) iterations
    :param verbose: Indicator if training details should be printed
    :param columnId: An optional class ID used in verbose print output,
        eg. used when L2SVM is used in MSVM.
    :return: Trained model/weights (shape: n x 1, w/ intercept: n+1)
    """

    params_dict = {'X': X, 'Y': Y}
    params_dict.update(kwargs)
    return Matrix(X.sds_context,
        'l2svm',
        named_input_nodes=params_dict)
