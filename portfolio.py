import numpy as np
import cvxpy as cp

def robust_markowitz_robust(mu_hat, sigma_hat, kappa, delta, lmd=0.5):
    N = len(mu_hat)
    S12 = np.linalg.cholesky(sigma_hat).T
    w = cp.Variable(N)

    obj = cp.Maximize(w.T @ mu_hat - kappa*cp.norm2(S12 @ w) - lmd*(cp.norm2(S12 @ w) + delta*cp.norm2(w))**2)
    constraints = [w >= 0, sum(w) == 1]
    prob = cp.Problem(obj, constraints)
    prob.solve(solver=cp.ECOS)
    return w.value