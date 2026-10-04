# 📊 QuantRisk

## Quantitative Portfolio Risk & Decision Support System

QuantRisk is a Python-based quantitative finance application designed to analyze financial assets, optimize portfolio allocation, measure portfolio risk, and support investment decision-making through an interactive Streamlit dashboard.

## 🎯 Project Objectives

The main objectives of QuantRisk are to:

- Analyze historical financial market data
- Estimate expected returns and volatility
- Study asset diversification
- Optimize portfolio allocation
- Compare portfolio strategies
- Measure downside risk
- Simulate future portfolio scenarios
- Provide decision-support insights

## ⚙️ Main Features

### Market Data Analysis
- Historical market data using Yahoo Finance
- Historical price visualization
- Daily return calculation
- Annualized expected return
- Annualized volatility

### Portfolio Optimization
- Minimum Variance Portfolio
- Maximum Sharpe Ratio Portfolio
- Long-only portfolio constraints
- Portfolio weights summing to 100%

### Strategy Comparison
QuantRisk compares the Minimum Variance and Maximum Sharpe strategies using:

- Expected annual return
- Annual volatility
- Sharpe Ratio

### Efficient Frontier
The application generates thousands of portfolio allocations to visualize the relationship between expected return and risk.

The Minimum Variance and Maximum Sharpe portfolios are highlighted on the graph.

### Risk Analysis
QuantRisk includes:

- 95% Historical Value at Risk (VaR)
- 95% Conditional Value at Risk (CVaR)
- Monetary risk estimates based on portfolio value

### Monte Carlo Simulation
The system performs Monte Carlo simulations using historical daily return and volatility.

Default simulation:

- 10,000 scenarios
- 252 trading days
- Portfolio value evolution
- Average final portfolio value
- Probability of loss
- 5th percentile final value

### Decision Support
Users can choose between:

- Minimum Variance — prioritizes risk reduction
- Maximum Sharpe — prioritizes risk-adjusted performance

QuantRisk then displays the recommended allocation and provides an interpretation of the portfolio's risk.

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- yfinance
- Streamlit
- Jupyter Notebook

## 📁 Project Structure

```text
QuantRisk/
│
├── app.py
├── README.md
│
├── src/
│   └── portfolio.py
│
├── notebooks/
│
├── data/
│   ├── raw/
│   └── processed/
│
└── reports/