## Introduction

This repo will crawl the historical data of designated funds and calculate a optimized portfolio with specified method

## Environment Setup

Use the following command to install the dependencies

``
conda create -n fof
conda activate fof
pip install -r requirements.txt
``

## Running
Run the following command to get the optimized weight. *CONFIG_PATH* is the path to your yaml config file

``
python main.py --cfg_path={CONFIG_PATH}
``

## Supported Portfolio

### robust Markowitz’s mean-variance portfolio
Optimize the following problem:

$$

\begin{align*}
    \max\limits_w & \quad w^T\hat\mu - \kappa||\hat\Sigma^{\frac{1}{2}}w||_2 - \lambda(||\hat\Sigma^{\frac{1}{2}}w||_2 + \frac{\delta}{\sqrt{T-1}}||w||_2) \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0
\end{align*}

$$