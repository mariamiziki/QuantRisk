import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf



from src.portfolio import (
    minimum_variance_portfolio,
    maximum_sharpe_portfolio,
    monte_carlo_simulation
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="QuantRisk",
    page_icon="📊",
    layout="wide"
)

st.title("📊 QuantRisk")

st.subheader(
    "Quantitative Portfolio Risk & Decision Support System"
)

st.write(
    "Analyze portfolio performance, optimize asset allocation, "
    "measure risk, and simulate future portfolio scenarios."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Portfolio Settings")

tickers_input = st.sidebar.text_input(
    "Asset Tickers",
    value="AAPL, MSFT, JPM, GLD"
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2021-01-01")
)

portfolio_value = st.sidebar.number_input(
    "Portfolio Value ($)",
    min_value=1000,
    value=100000,
    step=1000
)

risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate (%)",
    min_value=0.0,
    value=0.0,
    step=0.1
)

strategy = st.sidebar.selectbox(
    "Portfolio Strategy",
    [
        "Minimum Variance",
        "Maximum Sharpe"
    ]
)

tickers = [
    ticker.strip().upper()
    for ticker in tickers_input.split(",")
    if ticker.strip()
]

analyze_button = st.sidebar.button(
    "Analyze Portfolio",
    type="primary"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if len(tickers) < 2:
        st.error(
            "Please enter at least two valid asset tickers "
            "to perform portfolio optimization."
        )
        st.stop()

    st.write("### Selected Portfolio")

    st.write("Assets:", tickers)

    st.write(
        "Start Date:",
        start_date
    )

    st.write(
        f"Portfolio Value: ${portfolio_value:,.2f}"
    )

    st.write(
        f"Risk-Free Rate: {risk_free_rate:.2f}%"
    )

    # =====================================================
    # DOWNLOAD MARKET DATA
    # =====================================================

    with st.spinner("Downloading market data..."):
        data = yf.download(
            tickers,
            start=start_date,
            auto_adjust=True,
            progress=False
        )

    if data.empty:

        st.error(
            "No market data found. Please check the tickers."
        )

    else:

        prices = data["Close"]
        prices = prices.dropna(axis=1, how="all")

        if prices.shape[1] < 2:
            st.error(
                "Not enough valid assets were downloaded. "
                "Please check the ticker symbols and enter "
                "at least two valid assets."
            )
            st.stop()

        st.success(
            "Market data downloaded successfully!"
        )
               # =================================================
        # PORTFOLIO OVERVIEW
        # =================================================

        st.subheader("Portfolio Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Assets",
            len(tickers)
        )

        col2.metric(
            "Portfolio Value",
            f"${portfolio_value:,.0f}"
        )

        col3.metric(
            "Selected Strategy",
            strategy
        )

        st.divider()

        # =================================================
        # HISTORICAL PRICES
        # =================================================

        st.subheader("Historical Prices")

        # =================================================
        # HISTORICAL PRICES
        # =================================================

        st.subheader("Historical Prices")

        st.dataframe(prices.tail())

        st.line_chart(prices)

        # =================================================
        # RETURNS AND STATISTICS
        # =================================================

        returns = prices.pct_change().dropna()

        trading_days = 252

        annual_returns = (
            returns.mean() * trading_days
        )

        annual_volatility = (
            returns.std()
            * (trading_days ** 0.5)
        )

        covariance_matrix = (
            returns.cov() * trading_days
        )

        # =================================================
        # ASSET PERFORMANCE
        # =================================================

        st.subheader("Asset Performance")

        performance = pd.DataFrame({
            "Annual Return (%)":
                annual_returns * 100,
            "Annual Volatility (%)":
                annual_volatility * 100
        })

        st.dataframe(
            performance.style.format({
                "Annual Return (%)": "{:.2f}%",
                "Annual Volatility (%)": "{:.2f}%"
            })
        )

        # =================================================
        # MINIMUM VARIANCE PORTFOLIO
        # =================================================

        min_var_weights = minimum_variance_portfolio(
            covariance_matrix
        )

        min_var_return = (
            min_var_weights @ annual_returns
        )

        min_var_volatility = (
            min_var_weights
            @ covariance_matrix
            @ min_var_weights
        ) ** 0.5

        st.subheader(
            "Minimum Variance Portfolio"
        )

        min_var_df = pd.DataFrame({
            "Asset": prices.columns,
            "Weight (%)": min_var_weights * 100
        })

        st.dataframe(
            min_var_df.style.format({
                "Weight (%)": "{:.2f}%"
            }),
            hide_index=True
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Expected Annual Return",
            f"{min_var_return:.2%}"
        )

        col2.metric(
            "Annual Volatility",
            f"{min_var_volatility:.2%}"
        )

        # =================================================
        # MAXIMUM SHARPE PORTFOLIO
        # =================================================

        risk_free_decimal = risk_free_rate / 100

        max_sharpe_weights = maximum_sharpe_portfolio(
            annual_returns,
            covariance_matrix,
            risk_free_decimal
        )

        max_sharpe_return = (
            max_sharpe_weights @ annual_returns
        )

        max_sharpe_volatility = (
            max_sharpe_weights
            @ covariance_matrix
            @ max_sharpe_weights
        ) ** 0.5

        max_sharpe_ratio = (
            max_sharpe_return
            - risk_free_decimal
        ) / max_sharpe_volatility

        st.subheader(
            "Maximum Sharpe Portfolio"
        )

        max_sharpe_df = pd.DataFrame({
            "Asset": prices.columns,
            "Weight (%)": max_sharpe_weights * 100
        })

        st.dataframe(
            max_sharpe_df.style.format({
                "Weight (%)": "{:.2f}%"
            }),
            hide_index=True
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Expected Annual Return",
            f"{max_sharpe_return:.2%}"
        )

        col2.metric(
            "Annual Volatility",
            f"{max_sharpe_volatility:.2%}"
        )

        col3.metric(
            "Sharpe Ratio",
            f"{max_sharpe_ratio:.3f}"
        )
                # =================================================
        # STRATEGY COMPARISON
        # =================================================

        st.subheader("Strategy Comparison")

        min_var_sharpe = (
            min_var_return - risk_free_decimal
        ) / min_var_volatility

        comparison_df = pd.DataFrame({
            "Strategy": [
                "Minimum Variance",
                "Maximum Sharpe"
            ],
            "Expected Return (%)": [
                min_var_return * 100,
                max_sharpe_return * 100
            ],
            "Volatility (%)": [
                min_var_volatility * 100,
                max_sharpe_volatility * 100
            ],
            "Sharpe Ratio": [
                min_var_sharpe,
                max_sharpe_ratio
            ]
        })

        st.dataframe(
            comparison_df.style.format({
                "Expected Return (%)": "{:.2f}%",
                "Volatility (%)": "{:.2f}%",
                "Sharpe Ratio": "{:.3f}"
            }),
            hide_index=True
        )

        st.divider()
                # =================================================
        # EFFICIENT FRONTIER
        # =================================================

        st.subheader("Efficient Frontier")

        import numpy as np

        np.random.seed(42)

        num_portfolios = 5000

        random_returns = []
        random_volatilities = []
        random_sharpe_ratios = []

        for _ in range(num_portfolios):

            weights = np.random.random(
                len(prices.columns)
            )

            weights = weights / weights.sum()

            portfolio_return = (
                weights @ annual_returns
            )

            portfolio_volatility = (
                weights
                @ covariance_matrix
                @ weights
            ) ** 0.5

            sharpe_ratio = (
                portfolio_return
                - risk_free_decimal
            ) / portfolio_volatility

            random_returns.append(
                portfolio_return
            )

            random_volatilities.append(
                portfolio_volatility
            )

            random_sharpe_ratios.append(
                sharpe_ratio
            )

        fig, ax = plt.subplots(
            figsize=(9, 6)
        )

        scatter = ax.scatter(
            random_volatilities,
            random_returns,
            c=random_sharpe_ratios,
            cmap="viridis",
            alpha=0.6
        )

        ax.scatter(
            min_var_volatility,
            min_var_return,
            marker="*",
            s=250,
            label="Minimum Variance"
        )

        ax.scatter(
            max_sharpe_volatility,
            max_sharpe_return,
            marker="*",
            s=250,
            label="Maximum Sharpe"
        )

        ax.set_xlabel(
            "Annual Volatility"
        )

        ax.set_ylabel(
            "Expected Annual Return"
        )

        ax.set_title(
            "Efficient Frontier - Risk vs Return"
        )

        ax.legend()

        fig.colorbar(
            scatter,
            ax=ax,
            label="Sharpe Ratio"
        )

        st.pyplot(fig)

        st.caption(
            "Each point represents a randomly generated portfolio. "
            "The chart illustrates the trade-off between expected "
            "return and portfolio risk."
        )

        # =================================================
        # RECOMMENDED PORTFOLIO
        # =================================================

        st.subheader("Recommended Portfolio")
        st.success(
            f"Recommended Strategy: {strategy}"
        )

        if strategy == "Minimum Variance":

            recommended_weights = min_var_weights
            recommended_return = min_var_return
            recommended_volatility = min_var_volatility

        else:

            recommended_weights = max_sharpe_weights
            recommended_return = max_sharpe_return
            recommended_volatility = max_sharpe_volatility

        recommended_df = pd.DataFrame({
            "Asset": prices.columns,
            "Recommended Weight (%)":
                recommended_weights * 100
        })

        st.dataframe(
            recommended_df.style.format({
                "Recommended Weight (%)": "{:.2f}%"
            }),
            hide_index=True
        )
                # Portfolio Allocation Chart

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            recommended_weights,
            labels=prices.columns,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            f"{strategy} - Portfolio Allocation"
        )

        st.pyplot(fig)


        col1, col2 = st.columns(2)

        col1.metric(
            "Recommended Expected Return",
            f"{recommended_return:.2%}"
        )

        col2.metric(
            "Recommended Volatility",
            f"{recommended_volatility:.2%}"
        )

        # =================================================
        # RISK ANALYSIS
        # =================================================

        st.subheader("Risk Analysis")

        portfolio_daily_returns = returns.dot(
            recommended_weights
        )

        # Historical VaR 95%

        var_95 = portfolio_daily_returns.quantile(
            0.05
        )

        # Historical CVaR 95%

        cvar_95 = portfolio_daily_returns[
            portfolio_daily_returns <= var_95
        ].mean()

        # Convert to monetary losses

        var_loss = (
            abs(var_95) * portfolio_value
        )

        cvar_loss = (
            abs(cvar_95) * portfolio_value
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "1-Day VaR (95%)",
            f"${var_loss:,.2f}"
        )

        col2.metric(
            "1-Day CVaR (95%)",
            f"${cvar_loss:,.2f}"
        )

        # =================================================
        # MONTE CARLO SIMULATION
        # =================================================

        st.subheader("Monte Carlo Simulation")

        simulated_values, final_values = (
            monte_carlo_simulation(
                portfolio_daily_returns,
                portfolio_value
            )
        )

        average_final_value = (
            final_values.mean()
        )

        probability_of_loss = (
            final_values < portfolio_value
        ).mean()

        percentile_5 = (
            pd.Series(final_values)
            .quantile(0.05)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Final Value",
            f"${average_final_value:,.2f}"
        )

        col2.metric(
            "Probability of Loss",
            f"{probability_of_loss:.2%}"
        )

        col3.metric(
            "5th Percentile Value",
            f"${percentile_5:,.2f}"
        )

        # Display first 50 paths

        simulation_df = pd.DataFrame(
            simulated_values[:, :50]
        )

        st.line_chart(simulation_df)

        st.caption(
            "Monte Carlo simulation based on historical "
            "daily mean return and volatility. "
            "10,000 scenarios over 252 trading days."
        )

        # =================================================
        # DECISION SUPPORT
        # =================================================

        st.subheader("Decision Support")

        if strategy == "Minimum Variance":

            st.info(
                "This strategy prioritizes risk reduction. "
                "The portfolio is optimized to achieve the "
                "lowest possible volatility given the "
                "selected assets."
            )

        else:

            st.info(
                "This strategy prioritizes risk-adjusted "
                "performance. The portfolio is optimized "
                "to maximize the Sharpe Ratio, balancing "
                "expected return against portfolio volatility."
            )

        # =================================================
        # RISK INTERPRETATION
        # =================================================

        st.write("### Risk Interpretation")

        st.write(
            f"At a 95% confidence level, the portfolio's "
            f"1-day Value at Risk (VaR) is approximately "
            f"${var_loss:,.2f}."
        )

        st.write(
            f"If losses exceed the VaR threshold, the "
            f"average loss in these extreme cases (CVaR) "
            f"is approximately ${cvar_loss:,.2f}."
        )

        st.write(
            f"Based on the Monte Carlo simulation, the "
            f"estimated probability of ending the 252-day "
            f"period below the initial portfolio value is "
            f"{probability_of_loss:.2%}."
        )

