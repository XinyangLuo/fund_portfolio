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
    T = cfg['look_back']
    N = len(codes)
    df = get_multiple_returns(codes, T)
    X = df.to_numpy()
    portfolio_name = cfg['portfolio_name']

    match portfolio_name:
        case 'robust_markowitz_robust':
            kappa = cfg['robust_markowitz_robust']['kappa']
            delta = cfg['robust_markowitz_robust']['delta']/np.sqrt(T-1)
            lmd = cfg['robust_markowitz_robust']['lambda']
            w = portfolio.robust_markowitz_robust(X, kappa, delta, lmd)
        case 'mean_downside_risk':
            lmd = cfg['mean_downside_risk']['lambda']
            alpha = cfg['mean_downside_risk']['alpha']
            w = portfolio.mean_downside_risk(X, lmd, alpha)
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
        case 'risk_parity':
            if cfg['risk_parity']['equal_risk']:
                budget = np.repeat(1/N, N)
            else:
                budget = np.array(cfg['risk_parity']['budget'])
            w = portfolio.risk_parity(X, budget)
        case _:
            w = None
            print('Please Specify an implemented method')
    if w is not None:
        code_name_dict = cfg['code_name_dict']
        table = tabulize_result(codes, w, cfg['capital'], code_name_dict, portfolio_name)
        print(table)
