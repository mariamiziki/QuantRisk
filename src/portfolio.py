import numpy as np
from scipy.optimize import minimize


# =========================================================
# PORTFOLIO VOLATILITY
# =========================================================

def portfolio_volatility(weights, covariance_matrix):
    portfolio_variance = np.dot(
        weights.T,
        np.dot(covariance_matrix, weights)
    )

    return np.sqrt(portfolio_variance)


# =========================================================
# MINIMUM VARIANCE PORTFOLIO
# =========================================================

def minimum_variance_portfolio(covariance_matrix):

    num_assets = len(covariance_matrix)

    initial_weights = np.ones(num_assets) / num_assets

    constraints = {
        "type": "eq",
        "fun": lambda weights: np.sum(weights) - 1
    }

    bounds = tuple(
        (0, 1) for _ in range(num_assets)
    )

    result = minimize(
        portfolio_volatility,
        initial_weights,
        args=(covariance_matrix,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    return result.x


# =========================================================
# SHARPE RATIO
# =========================================================

def negative_sharpe_ratio(
    weights,
    annual_returns,
    covariance_matrix,
    risk_free_rate
):
    portfolio_return = np.dot(
        weights,
        annual_returns
    )

    portfolio_vol = portfolio_volatility(
        weights,
        covariance_matrix
    )

    sharpe_ratio = (
        portfolio_return - risk_free_rate
    ) / portfolio_vol

    return -sharpe_ratio


# =========================================================
# MAXIMUM SHARPE PORTFOLIO
# =========================================================

def maximum_sharpe_portfolio(
    annual_returns,
    covariance_matrix,
    risk_free_rate=0.0
):
    num_assets = len(annual_returns)

    initial_weights = (
        np.ones(num_assets) / num_assets
    )

    constraints = {
        "type": "eq",
        "fun": lambda weights: np.sum(weights) - 1
    }

    bounds = tuple(
        (0, 1) for _ in range(num_assets)
    )

    result = minimize(
        negative_sharpe_ratio,
        initial_weights,
        args=(
            annual_returns,
            covariance_matrix,
            risk_free_rate
        ),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    return result.x


# =========================================================
# MONTE CARLO SIMULATION
# =========================================================

def monte_carlo_simulation(
    portfolio_daily_returns,
    initial_value,
    simulation_days=252,
    num_simulations=10000
):
    daily_mean = portfolio_daily_returns.mean()
    daily_volatility = portfolio_daily_returns.std()

    np.random.seed(42)

    simulated_returns = np.random.normal(
        daily_mean,
        daily_volatility,
        size=(simulation_days, num_simulations)
    )

    simulated_values = (
        initial_value
        * np.cumprod(
            1 + simulated_returns,
            axis=0
        )
    )

    final_values = simulated_values[-1, :]

    return simulated_values, final_values
