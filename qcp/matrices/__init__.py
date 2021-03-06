# Copyright 2022 Tiernan8r
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module containing pure Python implementations of matrices.
"""
from qcp.matrices.matrix import Matrix  # noqa: F401
from qcp.matrices.sparse_matrix import SparseMatrix  # noqa: F401
from qcp.matrices.dense_matrix import DenseMatrix  # noqa: F401

from qcp.matrices.types import SCALARS, SCALARS_T, VECTOR, \
    MATRIX, SPARSE  # noqa: F401

#: Quick type referencing for the preferred `Matrix` class to use,
#: so that if we want to change it later, all we have to do is modify this
#: line
DefaultMatrix = SparseMatrix
