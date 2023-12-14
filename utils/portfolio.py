import numpy as np
import cvxpy as cp

def robust_markowitz_robust(mu_hat: np.ndarray, sigma_hat: np.ndarray, kappa: float, delta: float, lmd: float=0.5) -> np.ndarray:
    N = len(mu_hat)
    S12 = np.linalg.cholesky(sigma_hat).T
    w = cp.Variable(N)

    obj = cp.Maximize(w.T @ mu_hat - kappa*cp.norm2(S12 @ w) - lmd*(cp.norm2(S12 @ w) + delta*cp.norm2(w))**2)
    constraints = [w >= 0, sum(w) == 1]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value

def mean_downsid_risk(X: np.ndarray, lmd: float=0.5, alpha: int=2) -> np.ndarray:
    T, N = X.shape
    mu = X.mean(axis=0)
    w = cp.Variable(N)

    obj = cp.Maximize(w.T @ mu - lmd/T*sum(cp.pos(mu.T @ w - X @ w)**alpha))
    constraints = [w >= 0, sum(w) == 1]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value

def mean_cvar(X: np.ndarray, lmd: float=0.5, alpha: float=0.95) -> np.ndarray:
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

def mean_max_drawdown(X: np.ndarray, c: float=0.2) -> np.ndarray:
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

def mean_avg_drawdown(X: np.ndarray, c: float=0.2) -> np.ndarray:
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

def mean_CDaR(X: np.ndarray, c: float=0.1, alpha: float=0.95) -> np.ndarray:
    T, N = X.shape
    X_cum = np.cumsum(X, axis=0)
    mu = X.mean(axis=0)
    w = cp.Variable(N)
    z = cp.Variable(T)
    zeta = cp.Variable(1)
    u = cp.Variable(T)

    obj = cp.Maximize(w.T @ mu)
    constraints = [w >= 0, sum(w) == 1,
                   zeta + 1/(1-alpha) * cp.mean(z) <= c,
                   z >= 0, z >= u - X_cum @ w - zeta,
                   u >= X_cum @ w,
                   u[1:] >= u[:-1]]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value

def most_diversified(X: np.ndarray) -> np.ndarray:
    T, N = X.shape
    Sigma = np.cov(X.T)
    w = cp.Variable(N)

    obj = cp.Minimize(cp.quad_form(w, Sigma))
    constraints = [w >= 0, w.T @ Sigma.diagonal() == 1]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return w.value/sum(w.value)