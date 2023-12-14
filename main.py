import yaml
import argparse

import numpy as np

from crawler import get_multiple_returns
from portfolio import robust_markowitz_robust
from utils import tabulize_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg_path', type=str)
    args = parser.parse_args()

    with open(f'./{args.cfg_path}') as f:
        cfg = yaml.safe_load(f)

    codes = cfg['codes']
    T = cfg['look_back']
    df = get_multiple_returns(codes, T)

    if cfg['method'] == 'robust_markowitz_robust':
        mu = df.mean(axis=0).to_numpy()
        Sigma = df.cov().to_numpy()
        kappa = cfg['robust_markowitz_robust']['kappa']
        delta = cfg['robust_markowitz_robust']['delta']/np.sqrt(T-1)
        lmd = cfg['robust_markowitz_robust']['lambda']
        w = robust_markowitz_robust(mu, Sigma, kappa, delta, lmd)
        w = np.round(w, 2)
        table = tabulize_result(codes, w)
        print(table)
    else:
        print('Please Specify an implemented method')
