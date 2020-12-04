import numpy as np
from numpy.linalg import lstsq
from src.arnoldi import arnoldi_iteration
from src.csr import CSRMatrix


def generate_e(n):
    arr = [0] * (n+1)
    arr[0] = 1
    return np.array(arr)


def gmres(A, b, max_iter=50, min_residual=1e-8):
    A_csr = CSRMatrix(A)

    Q_values = []
    y = np.random.rand(1, len(b))

    for n in range(1, max_iter+1):
        Qn, hn = arnoldi_iteration(A_csr, b, n)
        Q_values.append(Qn)

        y = minimize(hn, b, n)

        rn = calculate_residual(hn, b, y, n)
        if rn < min_residual:
            return Qn.mult(y)

    return Q_values[:-1].mult(y)


def calculate_residual(hn, b, y, n):
    e1 = generate_e(n)
    b_norm = np.linalg.norm(b)
    return np.linalg.norm(hn.mult(y) - (b_norm*e1)) / b_norm


def minimize(hn, b, n):
    e1 = generate_e(n)
    b_norm = np.linalg.norm(b)
    negated_b_norm = np.negative(b_norm)
    negated_hn = hn.negative()
    negated_b_times_e1 = negated_b_norm * e1
    x, residuals, _, _ = lstsq(negated_hn.to_dense(), negated_b_times_e1, rcond=-1)
    return x
