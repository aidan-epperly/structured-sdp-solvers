import numpy as np
import scipy as sp
from scipy.linalg import toeplitz
import itertools

def sparse_toeplitz(constant, offset, dimension):
    diag_length = dimension - abs(offset)
    vec = constant * np.ones(diag_length)
    if offset == 0:
        return sp.sparse.diags(vec, 0)
    else:
        return sp.sparse.diags([vec, vec.conj()], [offset, -offset])

def kron_array(matrix_array):
    initial = matrix_array[0]
    for i in range(1, len(matrix_array)):
        initial = sp.sparse.kron(initial, matrix_array[i])
    return initial

def generate_toeplitz_basis(n, d):
    one_dimension_toeplitz_basis = []
    for i in range(0, 2 * d + 1):
        one_dimension_toeplitz_basis.append(sparse_toeplitz(1, i, 2 * d + 1))
    for i in range(1, 2 * d + 1):
        one_dimension_toeplitz_basis.append(sparse_toeplitz(1j, i, 2 * d + 1))
    iter_range = itertools.product(one_dimension_toeplitz_basis, repeat = n)
    return [kron_array(element) for element in iter_range]

if __name__ == "__main__":
    temp = generate_toeplitz_basis(1, 1)
    for matrix in temp:
        print(matrix.toarray())
