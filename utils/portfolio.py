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

def mean_downsid_risk(X: np.ndarray, lmd=0.5, alpha=2):
    T, N = X.shape
    mu = X.mean(axis=0)
    w = cp.Variable(N)

    obj = cp.Maximize(w.T @ mu - lmd/T*sum(cp.pos(mu.T @ w - X @ w)**alpha))
    constraints = [w >= 0, sum(w) == 1]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value

def mean_cvar(X: np.ndarray, lmd=0.5, alpha=0.95):
    T, N = X.shape
    mu = X.mean(axis=0)
    w = cp.Variable(N)
    z = cp.Variable(T)
    zeta = cp.Variable(1)

    obj = cp.Maximize(w.T @ mu - lmd*(zeta + 1/(T*(1-alpha))*sum(z)))
    constraints = [w >= 0, sum(w) == 1, z >= 0,
                   z >= -X @ w -zeta]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value

def mean_max_drawdown(X, c=0.2):
    T, N = X.shape
    X_cum = np.cumsum(X, axis=0)
    mu = X.mean(axis=0)
    w = cp.Variable(N)
    u = cp.Variable(T)

    obj = cp.Maximize(w.T @ mu)
    constraints = [w >= 0, sum(w) == 1,
                   u <= X_cum @ w + c,
                   u >= X_cum @ w,
                   u[1:] >= u[:-1]]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value

def mean_avg_drawdown(X, c=0.2):
    T, N = X.shape
    X_cum = np.cumsum(X, axis=0)
    mu = X.mean(axis=0)
    w = cp.Variable(N)
    u = cp.Variable(T)

    obj = cp.Maximize(w.T @ mu)
    constraints = [w >= 0, sum(w) == 1,
                   cp.mean(u) <= cp.mean(X_cum @ w) + c,
                   u >= X_cum @ w,
                   u[1:] >= u[:-1]]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value