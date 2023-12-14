## Introduction

This repo will crawl the historical data of designated funds and calculate a optimized portfolio with specified method

## Environment Setup

Use the following command to install the dependencies

```
conda create -n fof
conda activate fof
pip install -r requirements.txt
```

## Running
Run the following command to get the optimized weight. *CONFIG_PATH* is the path to your yaml config file

```
python main.py --cfg_path={CONFIG_PATH}
```

## Supported Portfolio

### robust Markowitz’s mean-variance portfolio

$$

\begin{align*}
    \max\limits_w & \quad w^T\hat\mu - \kappa||\hat\Sigma^{\frac{1}{2}}w||_2 - \lambda(||\hat\Sigma^{\frac{1}{2}}w||_2 + \frac{\delta}{\sqrt{T-1}}||w||_2) \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0
\end{align*}

$$

### Mean downside risk portfolio

$$
\begin{align*}
    \max\limits_w & \quad w^T - \lambda\frac{1}{T}\sum\limits_{t=1}^T(w^T\mu - w^Tr_t)^\alpha \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0
\end{align*}
$$

### Mean CVaR portfolio

$$
\begin{align*}
    \max\limits_{w,z,\zeta} & \quad w^T\mu - \lambda(\zeta + \frac{1}{1-\alpha}\frac{1}{T}\sum\limits_{t=1}^Tz_t) \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0 \\
    & \quad z \geq 0 \\
    & \quad z_t \geq -w^Tr_t - \zeta
\end{align*}
$$

### Mean Max Drawdown portfolio

$$
\begin{align*}
    \max\limits_{w,u} & \quad w^T\mu \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0 \\
    & \quad u_{t-1} \leq u_t \\
    & \quad w^Tr_t^{cum} \leq u_t \leq w^Tr_t^{cum} + c
\end{align*}
$$

### Mean Average Drawdown portfolio

$$
\begin{align*}
    \max\limits_{w,u} & \quad w^T\mu \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0 \\
    & \quad u_{t-1} \leq u_t \quad \forall 1 < t \leq T \\
    & \quad w^Tr_t^{cum} \leq u_t \\
    & \quad \frac{1}{T}\sum\limits_{t=1}^Tu_t \leq \frac{1}{T}\sum\limits_{t=1}^Tw^Tr_t^{cum} + c
\end{align*}
$$

### Mean CDaR portfolio

$$
\begin{align*}
    \max\limits_{w,u,z,\zeta} & \quad w^T\mu \\
    s.t. & \quad 1^Tw = 1 \\
    & \quad w \geq 0 \\
    & \quad \zeta + \frac{1}{1-\alpha}\frac{1}{T}\sum\limits_{t=1}^Tz_t \leq c \\
    & \quad z_t \geq 0 \\
    & \quad z_t \geq u_t - w^Tr_t^{cum} - \zeta \\
    & \quad u_t \geq w^Tr_t^{cum} \\
    & \quad u_{t} \geq u_{t-1}
\end{align*}
$$