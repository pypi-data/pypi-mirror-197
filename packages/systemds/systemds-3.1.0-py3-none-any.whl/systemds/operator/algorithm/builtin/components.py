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
# Autogenerated From : scripts/builtin/components.dml

from typing import Dict, Iterable

from systemds.operator import OperationNode, Matrix, Frame, List, MultiReturn, Scalar
from systemds.script_building.dag import OutputType
from systemds.utils.consts import VALID_INPUT_TYPES


def components(G: Matrix,
               **kwargs: Dict[str, VALID_INPUT_TYPES]):
    """
     Computes the connected components of a graph and returns a
     vector indicating the assignment of vertices to components,
     where each component is identified by the maximum vertex ID
     (i.e., row/column position of the input graph) 
    
    
    
    :param X: Location to read the matrix of feature vectors
    :param Y: Location to read the matrix with category labels
    :param icpt: Intercept presence, shifting and rescaling X columns: 0 = no intercept,
        no shifting, no rescaling; 1 = add intercept, but neither shift nor rescale X;
        2 = add intercept, shift & rescale X columns to mean = 0, variance = 1
    :param tol: tolerance ("epsilon")
    :param reg: regularization parameter (lambda = 1/C); intercept is not regularized
    :param maxi: max. number of outer (Newton) iterations
    :param maxii: max. number of inner (conjugate gradient) iterations, 0 = no max
    :param verbose: flag specifying if logging information should be printed
    :return: regression betas as output for prediction
    """

    params_dict = {'G': G}
    params_dict.update(kwargs)
    return Matrix(G.sds_context,
        'components',
        named_input_nodes=params_dict)
