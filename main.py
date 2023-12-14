import yaml
import argparse

import numpy as np

from utils.crawler import get_multiple_returns
from utils.visualize import tabulize_result
from utils import portfolio


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg_path', type=str)
    args = parser.parse_args()

    with open(f'./{args.cfg_path}') as f:
        cfg = yaml.safe_load(f)

    codes = cfg['codes']
    codes = [str(c) for c in codes]
    T = cfg['look_back']
    df = get_multiple_returns(codes, T)
    X = df.to_numpy()

    match cfg['method']:
        case 'robust_markowitz_robust':
            mu = df.mean(axis=0).to_numpy()
            Sigma = df.cov().to_numpy()
            kappa = cfg['robust_markowitz_robust']['kappa']
            delta = cfg['robust_markowitz_robust']['delta']/np.sqrt(T-1)
            lmd = cfg['robust_markowitz_robust']['lambda']
            w = portfolio.robust_markowitz_robust(mu, Sigma, kappa, delta, lmd)
        case 'mean_downside_risk':
            lmd = cfg['mean_downside_risk']['lambda']
            alpha = cfg['mean_downside_risk']['alpha']
            w = portfolio.mean_downsid_risk(X, lmd, alpha)
        case 'mean_cvar':
            lmd = cfg['mean_cvar']['lambda']
            alpha = cfg['mean_cvar']['alpha']
            w = portfolio.mean_cvar(X, lmd, alpha)
        case 'mean_max_draw_down':
            c = cfg['mean_max_draw_down']['c']
            w = portfolio.mean_max_drawdown(X, c)
        case 'mean_avg_draw_down':
            c = cfg['mean_avg_draw_down']['c']
            w = portfolio.mean_avg_drawdown(X, c)
        case 'mean_cdar':
            c = cfg['mean_cdar']['c']
            alpha = cfg['mean_cdar']['alpha']
            w = portfolio.mean_CDaR(X, c, alpha)
        case 'most_diversified':
            w = portfolio.most_diversified(X)
        case _:
            w = None
            print('Please Specify an implemented method')
    if w is not None:
        w = np.round(w, 2)
        table = tabulize_result(codes, w)
        print(f'{cfg['method']} portfolio')
        print(table)
