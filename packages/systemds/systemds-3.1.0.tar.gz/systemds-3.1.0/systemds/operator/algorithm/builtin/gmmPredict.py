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
# Autogenerated From : scripts/builtin/gmmPredict.dml

from typing import Dict, Iterable

from systemds.operator import OperationNode, Matrix, Frame, List, MultiReturn, Scalar
from systemds.script_building.dag import OutputType
from systemds.utils.consts import VALID_INPUT_TYPES


def gmmPredict(X: Matrix,
               weight: Matrix,
               mu: Matrix,
               precisions_cholesky: Matrix,
               **kwargs: Dict[str, VALID_INPUT_TYPES]):
    """
     Prediction function for a Gaussian Mixture Model (gmm).
     Compute posterior probabilities for new instances given the variance and mean of fitted dat.
    
    
    
    :param X: Dataset input to predict the labels from
    :param weight: Weight of learned model:
        A matrix whose [i,k]th entry is the probability
        that observation i in the test data belongs to the kth class
    :param mu: Fitted clusters mean
    :param precisions_cholesky: Fitted precision matrix for each mixture
    :param model: "VVV": unequal variance (full),each component has its own general covariance matrix
        "EEE": equal variance (tied), all components share the same general covariance matrix
        "VVI": spherical, unequal volume (diag), each component has its own diagonal
        covariance matrix
        "VII": spherical, equal volume (spherical), each component has its own single variance
    :return: The predictions made by the gaussian model on the X input dataset
    :return: Probability of the predictions given the X input dataset
    """

    params_dict = {'X': X, 'weight': weight, 'mu': mu, 'precisions_cholesky': precisions_cholesky}
    params_dict.update(kwargs)
    
    vX_0 = Matrix(X.sds_context, '')
    vX_1 = Matrix(X.sds_context, '')
    output_nodes = [vX_0, vX_1, ]

    op = MultiReturn(X.sds_context, 'gmmPredict', output_nodes, named_input_nodes=params_dict)

    vX_0._unnamed_input_nodes = [op]
    vX_1._unnamed_input_nodes = [op]

    return op
