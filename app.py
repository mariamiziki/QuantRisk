import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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


# =========================================================
# PROFESSIONAL DASHBOARD DESIGN
# =========================================================

st.markdown(
    """
<style>

/* MAIN APP */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(37, 99, 235, 0.20),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #07111f 0%,
            #0f172a 50%,
            #111c35 100%
        );

    color: #f8fafc;
}


.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0b1220 0%,
        #111827 100%
    );

    border-right: 1px solid rgba(56, 189, 248, 0.20);
}


/* HEADINGS */

h1 {
    color: #f8fafc !important;
}

h2, h3 {
    color: #38bdf8 !important;
}


/* HERO */

.hero-card {
    position: relative;
    overflow: hidden;

    padding: 38px 42px;
    margin-bottom: 30px;

    background: linear-gradient(
        120deg,
        rgba(14, 165, 233, 0.18),
        rgba(37, 99, 235, 0.12)
    );

    border: 1px solid rgba(56, 189, 248, 0.30);
    border-radius: 22px;

    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.28);
}


.hero-card::after {
    content: "";
    position: absolute;

    width: 260px;
    height: 260px;

    right: -80px;
    top: -100px;

    background: rgba(56, 189, 248, 0.10);
    border-radius: 50%;
}


.hero-badge {
    display: inline-block;

    padding: 7px 14px;
    margin-bottom: 10px;

    background: rgba(56, 189, 248, 0.10);

    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 30px;

    color: #7dd3fc;

    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.2px;
}


.hero-card h1 {
    margin: 5px 0 2px 0;

    font-size: 48px;
    font-weight: 800;

    color: #f8fafc !important;
}


.hero-card h3 {
    margin-top: 0;
    color: #38bdf8 !important;
    font-size: 22px;
}


.hero-card p {
    max-width: 780px;

    margin-top: 15px;

    color: #cbd5e1;

    font-size: 16px;
    line-height: 1.7;
}


/* METRIC CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(30, 41, 59, 0.95),
        rgba(15, 23, 42, 0.95)
    );

    border: 1px solid rgba(56, 189, 248, 0.20);
    border-radius: 16px;

    padding: 18px 20px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.20);
}


[data-testid="stMetricLabel"] {
    color: #94a3b8;
}


[data-testid="stMetricValue"] {
    color: #f8fafc;
    font-weight: 700;
}


/* BUTTON */

.stButton > button {
    width: 100%;

    background: linear-gradient(
        90deg,
        #0ea5e9,
        #2563eb
    );

    color: white;

    border: none;
    border-radius: 10px;

    padding: 0.70rem 1rem;

    font-weight: 700;
    font-size: 16px;

    transition: all 0.25s ease;

    box-shadow:
        0 5px 18px rgba(37, 99, 235, 0.25);
}


.stButton > button:hover {
    transform: translateY(-2px);

    background: linear-gradient(
        90deg,
        #38bdf8,
        #3b82f6
    );

    color: white;
    border: none;

    box-shadow:
        0 8px 25px rgba(14, 165, 233, 0.40);
}


/* DATAFRAMES */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;
    overflow: hidden;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.15);
}


/* ALERTS */

[data-testid="stAlert"] {
    border-radius: 12px;
}


/* TEXT */

p {
    color: #cbd5e1;
}

hr {
    border-color: rgba(148, 163, 184, 0.15);
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """<div class="hero-card">
<div class="hero-badge">QUANTITATIVE FINANCE • RISK ANALYTICS</div>
<h1>📊 QuantRisk</h1>
<h3>Portfolio Risk & Decision Support System</h3>
<p>Analyze financial markets, optimize portfolio allocation, measure downside risk and simulate future portfolio scenarios through a quantitative decision-support dashboard.</p>
</div>""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Portfolio Settings")

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
    "🚀 Analyze Portfolio",
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

    st.subheader("📌 Selected Portfolio")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Selected Assets",
        len(tickers)
    )

    col2.metric(
        "Portfolio Value",
        f"${portfolio_value:,.0f}"
    )

    col3.metric(
        "Risk-Free Rate",
        f"{risk_free_rate:.2f}%"
    )

    st.caption(
        f"Assets: {', '.join(tickers)} • "
        f"Historical data starting from {start_date}"
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

        prices = prices.dropna(
            axis=1,
            how="all"
        )

        if prices.shape[1] < 2:

            st.error(
                "Not enough valid assets were downloaded. "
                "Please check the ticker symbols and enter "
                "at least two valid assets."
            )

            st.stop()

        st.success(
            "✓ Market data downloaded successfully!"
        )


        # =================================================
        # PORTFOLIO OVERVIEW
        # =================================================

        st.subheader("📊 Portfolio Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Assets",
            len(prices.columns)
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

        st.subheader("📈 Historical Prices")

        st.dataframe(
            prices.tail(),
            use_container_width=True
        )

        st.line_chart(
            prices,
            use_container_width=True
        )


        # =================================================
        # RETURNS AND STATISTICS
        # =================================================

        returns = prices.pct_change().dropna()

        trading_days = 252

        annual_returns = (
            returns.mean()
            * trading_days
        )

        annual_volatility = (
            returns.std()
            * (trading_days ** 0.5)
        )

        covariance_matrix = (
            returns.cov()
            * trading_days
        )


        # =================================================
        # ASSET PERFORMANCE
        # =================================================

        st.subheader("📋 Asset Performance")

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
            }),
            use_container_width=True
        )


        # =================================================
        # CORRELATION & DIVERSIFICATION
        # =================================================

        st.subheader(
            "🔗 Asset Correlation & Diversification"
        )

        correlation_matrix = returns.corr()

        fig, ax = plt.subplots(
            figsize=(8, 6)
        )

        fig.patch.set_facecolor("#0f172a")
        ax.set_facecolor("#0f172a")

        heatmap = ax.imshow(
            correlation_matrix.values,
            cmap="coolwarm",
            vmin=-1,
            vmax=1
        )

        ax.set_xticks(
            range(len(correlation_matrix.columns))
        )

        ax.set_yticks(
            range(len(correlation_matrix.index))
        )

        ax.set_xticklabels(
            correlation_matrix.columns,
            color="#e2e8f0"
        )

        ax.set_yticklabels(
            correlation_matrix.index,
            color="#e2e8f0"
        )

        for i in range(
            len(correlation_matrix.index)
        ):
            for j in range(
                len(correlation_matrix.columns)
            ):

                value = correlation_matrix.iloc[i, j]

                ax.text(
                    j,
                    i,
                    f"{value:.2f}",
                    ha="center",
                    va="center",
                    color="white",
                    fontweight="bold"
                )

        ax.set_title(
            "Asset Return Correlation Matrix",
            color="#f8fafc",
            pad=15
        )

        colorbar = fig.colorbar(
            heatmap,
            ax=ax
        )

        colorbar.ax.tick_params(
            colors="#cbd5e1"
        )

        colorbar.set_label(
            "Correlation",
            color="#cbd5e1"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

        upper_triangle = correlation_matrix.where(
            np.triu(
                np.ones(
                    correlation_matrix.shape
                ),
                k=1
            ).astype(bool)
        )

        average_correlation = (
            upper_triangle
            .stack()
            .mean()
        )

        st.metric(
            "Average Pairwise Correlation",
            f"{average_correlation:.2f}"
        )

        if average_correlation < 0.30:

            st.success(
                "The selected assets show relatively low "
                "average correlation, which supports "
                "portfolio diversification."
            )

        elif average_correlation < 0.60:

            st.info(
                "The selected assets show moderate average "
                "correlation. The portfolio has some "
                "diversification benefits."
            )

        else:

            st.warning(
                "The selected assets show relatively high "
                "average correlation, which may limit "
                "diversification benefits."
            )


        # =================================================
        # MINIMUM VARIANCE
        # =================================================

        st.subheader(
            "🛡️ Minimum Variance Portfolio"
        )

        min_var_weights = (
            minimum_variance_portfolio(
                covariance_matrix
            )
        )

        min_var_return = (
            min_var_weights
            @ annual_returns
        )

        min_var_volatility = (
            min_var_weights
            @ covariance_matrix
            @ min_var_weights
        ) ** 0.5

        min_var_df = pd.DataFrame({
            "Asset":
                prices.columns,

            "Weight (%)":
                min_var_weights * 100
        })

        st.dataframe(
            min_var_df.style.format({
                "Weight (%)": "{:.2f}%"
            }),
            hide_index=True,
            use_container_width=True
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
        # MAXIMUM SHARPE
        # =================================================

        st.subheader(
            "⚡ Maximum Sharpe Portfolio"
        )

        risk_free_decimal = (
            risk_free_rate / 100
        )

        max_sharpe_weights = (
            maximum_sharpe_portfolio(
                annual_returns,
                covariance_matrix,
                risk_free_decimal
            )
        )

        max_sharpe_return = (
            max_sharpe_weights
            @ annual_returns
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

        max_sharpe_df = pd.DataFrame({
            "Asset":
                prices.columns,

            "Weight (%)":
                max_sharpe_weights * 100
        })

        st.dataframe(
            max_sharpe_df.style.format({
                "Weight (%)": "{:.2f}%"
            }),
            hide_index=True,
            use_container_width=True
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

        st.subheader(
            "⚖️ Strategy Comparison"
        )

        min_var_sharpe = (
            min_var_return
            - risk_free_decimal
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
                "Expected Return (%)":
                    "{:.2f}%",

                "Volatility (%)":
                    "{:.2f}%",

                "Sharpe Ratio":
                    "{:.3f}"
            }),
            hide_index=True,
            use_container_width=True
        )

        st.divider()


        # =================================================
        # EFFICIENT FRONTIER
        # =================================================

        st.subheader("🌐 Efficient Frontier")

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
            figsize=(10, 6)
        )

        fig.patch.set_facecolor("#0f172a")
        ax.set_facecolor("#0f172a")

        scatter = ax.scatter(
            random_volatilities,
            random_returns,
            c=random_sharpe_ratios,
            cmap="viridis",
            alpha=0.7
        )

        ax.scatter(
            min_var_volatility,
            min_var_return,
            marker="*",
            s=300,
            label="Minimum Variance"
        )

        ax.scatter(
            max_sharpe_volatility,
            max_sharpe_return,
            marker="*",
            s=300,
            label="Maximum Sharpe"
        )

        ax.set_xlabel(
            "Annual Volatility"
        )

        ax.set_ylabel(
            "Expected Annual Return"
        )

        ax.set_title(
            "Efficient Frontier — Risk vs Return"
        )

        ax.tick_params(
            colors="#cbd5e1"
        )

        ax.xaxis.label.set_color(
            "#cbd5e1"
        )

        ax.yaxis.label.set_color(
            "#cbd5e1"
        )

        ax.title.set_color(
            "#f8fafc"
        )

        for spine in ax.spines.values():
            spine.set_color("#334155")

        legend = ax.legend()

        plt.setp(
            legend.get_texts(),
            color="#e2e8f0"
        )

        legend.get_frame().set_facecolor(
            "#1e293b"
        )

        legend.get_frame().set_edgecolor(
            "#334155"
        )

        colorbar = fig.colorbar(
            scatter,
            ax=ax
        )

        colorbar.set_label(
            "Sharpe Ratio",
            color="#cbd5e1"
        )

        colorbar.ax.tick_params(
            colors="#cbd5e1"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

        st.caption(
            "Each point represents a randomly generated "
            "portfolio. The visualization illustrates "
            "the trade-off between expected return and risk."
        )


        # =================================================
        # RECOMMENDED PORTFOLIO
        # =================================================

        st.subheader(
            "🎯 Recommended Portfolio"
        )

        st.success(
            f"Recommended Strategy: {strategy}"
        )

        if strategy == "Minimum Variance":

            recommended_weights = (
                min_var_weights
            )

            recommended_return = (
                min_var_return
            )

            recommended_volatility = (
                min_var_volatility
            )

        else:

            recommended_weights = (
                max_sharpe_weights
            )

            recommended_return = (
                max_sharpe_return
            )

            recommended_volatility = (
                max_sharpe_volatility
            )

        recommended_df = pd.DataFrame({
            "Asset":
                prices.columns,

            "Recommended Weight (%)":
                recommended_weights * 100
        })

        col_chart, col_table = st.columns(
            [1.1, 1]
        )

        with col_chart:

            fig, ax = plt.subplots(
                figsize=(6, 6)
            )

            fig.patch.set_facecolor("#0f172a")
            ax.set_facecolor("#0f172a")

            wedges, texts, autotexts = ax.pie(
                recommended_weights,
                labels=prices.columns,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={
                    "edgecolor": "#0f172a",
                    "linewidth": 2
                }
            )

            for text in texts:
                text.set_color("#e2e8f0")

            for autotext in autotexts:
                autotext.set_color("#ffffff")
                autotext.set_fontweight("bold")

            ax.set_title(
                f"{strategy} Allocation"
            )

            ax.title.set_color("#f8fafc")

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

        with col_table:

            st.dataframe(
                recommended_df.style.format({
                    "Recommended Weight (%)":
                        "{:.2f}%"
                }),
                hide_index=True,
                use_container_width=True
            )

            st.write("")

            col1, col2 = st.columns(2)

            col1.metric(
                "Expected Return",
                f"{recommended_return:.2%}"
            )

            col2.metric(
                "Volatility",
                f"{recommended_volatility:.2%}"
            )


        # =================================================
        # PORTFOLIO DAILY RETURNS
        # =================================================

        portfolio_daily_returns = (
            returns.dot(
                recommended_weights
            )
        )


        # =================================================
        # DRAWDOWN ANALYSIS
        # =================================================

        st.subheader(
            "📉 Drawdown Analysis"
        )

        portfolio_growth = (
            1 + portfolio_daily_returns
        ).cumprod()

        running_peak = (
            portfolio_growth.cummax()
        )

        drawdown = (
            portfolio_growth
            / running_peak
        ) - 1

        max_drawdown = (
            drawdown.min()
        )

        st.metric(
            "Maximum Drawdown",
            f"{max_drawdown:.2%}"
        )

        drawdown_chart = (
            drawdown * 100
        ).rename("Drawdown (%)")

        st.line_chart(
            drawdown_chart,
            use_container_width=True
        )

        st.caption(
            "Drawdown measures the decline of the portfolio "
            "from a previous historical peak. Maximum Drawdown "
            "represents the largest peak-to-trough loss observed "
            "during the selected historical period."
        )


        # =================================================
        # RISK ANALYSIS
        # =================================================

        st.subheader(
            "⚠️ Risk Analysis"
        )

        var_95 = (
            portfolio_daily_returns
            .quantile(0.05)
        )

        cvar_95 = (
            portfolio_daily_returns[
                portfolio_daily_returns
                <= var_95
            ].mean()
        )

        var_loss = (
            abs(var_95)
            * portfolio_value
        )

        cvar_loss = (
            abs(cvar_95)
            * portfolio_value
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
        # MONTE CARLO
        # =================================================

        st.subheader(
            "🎲 Monte Carlo Simulation"
        )

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
            final_values
            < portfolio_value
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

        simulation_df = pd.DataFrame(
            simulated_values[:, :50]
        )

        st.line_chart(
            simulation_df,
            use_container_width=True
        )

        st.caption(
            "Monte Carlo simulation based on historical "
            "daily mean return and volatility. "
            "10,000 scenarios over 252 trading days."
        )


        # =================================================
        # DECISION SUPPORT
        # =================================================

        st.subheader(
            "💡 Decision Support"
        )

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

        st.subheader(
            "🔎 Risk Interpretation"
        )

        st.write(
            f"The maximum historical drawdown of the selected "
            f"portfolio is approximately "
            f"**{max_drawdown:.2%}**."
        )

        st.write(
            f"At a 95% confidence level, the portfolio's "
            f"1-day Value at Risk (VaR) is approximately "
            f"**${var_loss:,.2f}**."
        )

        st.write(
            f"If losses exceed the VaR threshold, the "
            f"average loss in these extreme cases (CVaR) "
            f"is approximately **${cvar_loss:,.2f}**."
        )

        st.write(
            f"Based on the Monte Carlo simulation, the "
            f"estimated probability of ending the 252-day "
            f"period below the initial portfolio value is "
            f"**{probability_of_loss:.2%}**."
        )

        st.divider()

        st.caption(
            "QuantRisk • Quantitative Portfolio Risk "
            "& Decision Support System"
        )