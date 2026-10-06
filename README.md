# 📊 QuantRisk

## Quantitative Portfolio Risk & Decision Support System

QuantRisk is a Python-based quantitative finance application designed to analyze financial assets, optimize portfolio allocation, measure portfolio risk, compare investment strategies, and support investment decision-making through an interactive Streamlit dashboard.

The project combines concepts from **portfolio theory, risk management, optimization, statistics, and financial simulation** in a practical decision-support system.

---

## 🎯 Project Objectives

The main objectives of QuantRisk are to:

- Analyze historical financial market data
- Estimate expected returns and volatility
- Study asset correlation and diversification
- Optimize portfolio allocation
- Compare portfolio strategies
- Visualize the risk-return trade-off
- Measure downside risk
- Compare an optimized portfolio with a market benchmark
- Simulate future portfolio scenarios
- Provide quantitative decision-support insights

---

## ⚙️ Main Features

### 📈 Market Data Analysis

QuantRisk downloads historical financial data using Yahoo Finance and performs several statistical calculations.

The application provides:

- Historical adjusted market prices
- Historical price visualization
- Daily return calculation
- Annualized expected return
- Annualized volatility
- Covariance matrix estimation

Users can select their own financial assets and historical starting date directly from the dashboard.

---

### 🔗 Correlation & Diversification Analysis

QuantRisk calculates the correlation matrix of asset returns and displays it through a correlation heatmap.

The system also calculates the **average pairwise correlation** between the selected assets.

This analysis helps evaluate diversification:

- Lower correlations generally indicate stronger diversification potential
- Moderate correlations indicate partial diversification benefits
- Higher correlations may reduce diversification benefits

The diagonal elements of the correlation matrix are excluded from the average pairwise correlation calculation.

---

### 🛡️ Minimum Variance Portfolio

The Minimum Variance strategy searches for the portfolio allocation that minimizes total portfolio volatility.

The optimization is performed under the following constraints:

- Portfolio weights sum to 100%
- Long-only positions
- Individual asset weights remain between 0% and 100%

The strategy is suitable for an investor whose main objective is **risk reduction**.

---

### ⚡ Maximum Sharpe Ratio Portfolio

The Maximum Sharpe strategy searches for the portfolio with the highest risk-adjusted performance.

The Sharpe Ratio is defined as:

```text
Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Portfolio Volatility
```

The risk-free rate can be configured directly from the Streamlit dashboard.

The optimization uses the same long-only and fully invested portfolio constraints.

---

### ⚖️ Strategy Comparison

QuantRisk compares the Minimum Variance and Maximum Sharpe strategies using:

- Expected annual return
- Annual volatility
- Sharpe Ratio

This comparison allows the user to understand the trade-off between minimizing risk and maximizing risk-adjusted performance.

---

### 🌐 Efficient Frontier

The application generates **5,000 random portfolio allocations** to visualize the relationship between expected return and portfolio risk.

Each simulated portfolio is represented according to:

- Expected annual return
- Annual volatility
- Sharpe Ratio

The Minimum Variance and Maximum Sharpe portfolios are highlighted on the graph.

The Efficient Frontier visualization provides an intuitive representation of the fundamental **risk-return trade-off** in portfolio management.

---

### 🎯 Recommended Portfolio

Users can select their preferred optimization strategy:

- **Minimum Variance** — prioritizes risk reduction
- **Maximum Sharpe** — prioritizes risk-adjusted performance

QuantRisk then displays:

- Recommended portfolio weights
- Expected annual return
- Annual volatility
- Portfolio allocation chart

The recommended allocation becomes the basis for the subsequent risk analysis.

---

### 📊 S&P 500 Benchmark Comparison

QuantRisk compares the selected optimized portfolio with the **S&P 500 Index (`^GSPC`)** over the same historical period.

The comparison includes:

- Cumulative historical performance
- Annualized return
- Annualized volatility
- Sharpe Ratio
- Total cumulative return
- Excess return relative to the S&P 500

The application also provides an automatic interpretation indicating whether the optimized portfolio historically outperformed or underperformed the benchmark.

The S&P 500 is used only as a **performance benchmark** and does not participate in the portfolio optimization process.

---

### 📉 Drawdown Analysis

QuantRisk calculates the historical drawdown of the recommended portfolio.

Drawdown measures the decline in portfolio value relative to a previous historical peak.

The system provides:

- Historical drawdown evolution
- Maximum Drawdown

Maximum Drawdown represents the largest observed peak-to-trough decline during the selected historical period.

This metric complements volatility by providing a more intuitive measure of historical downside risk.

---

### ⚠️ Risk Analysis

QuantRisk includes historical downside risk measures:

- 95% Historical Value at Risk (VaR)
- 95% Conditional Value at Risk (CVaR)
- Monetary risk estimates based on the selected portfolio value

**Value at Risk (VaR)** estimates a loss threshold associated with the lower tail of historical daily returns.

**Conditional Value at Risk (CVaR)** estimates the average loss when returns fall beyond the VaR threshold.

These measures provide additional information about potential downside losses that may not be fully represented by volatility alone.

---

### 🎲 Monte Carlo Simulation

QuantRisk performs Monte Carlo simulations using the historical daily mean return and volatility of the recommended portfolio.

Default simulation parameters:

- 10,000 scenarios
- 252 trading days
- Historical daily mean return
- Historical daily volatility
- Fixed random seed for reproducibility

The simulation provides:

- Portfolio value evolution across simulated scenarios
- Average final portfolio value
- Probability of finishing below the initial portfolio value
- 5th percentile final portfolio value

Monte Carlo results represent **model-generated scenarios rather than forecasts of future market performance**.

---

### 💡 Decision Support

QuantRisk combines portfolio optimization and risk analytics into a decision-support framework.

Depending on the selected strategy, the application explains whether the recommended portfolio prioritizes:

- Risk minimization
- Risk-adjusted performance

The system also provides interpretations of:

- Diversification
- Benchmark performance
- Maximum Drawdown
- Value at Risk
- Conditional Value at Risk
- Monte Carlo probability of loss

The objective is not to provide investment advice, but to transform quantitative results into understandable decision-support information.

---

## 🧮 Quantitative Methodology

QuantRisk follows the following analytical workflow:

```text
Historical Market Data
        ↓
Daily Asset Returns
        ↓
Expected Returns + Volatility + Covariance
        ↓
Correlation & Diversification Analysis
        ↓
Portfolio Optimization
        ↓
Minimum Variance / Maximum Sharpe
        ↓
Efficient Frontier
        ↓
Recommended Portfolio
        ↓
S&P 500 Benchmark Comparison
        ↓
Drawdown + VaR + CVaR
        ↓
Monte Carlo Simulation
        ↓
Decision Support & Risk Interpretation
```

Annualized expected returns are estimated using:

```text
Annual Return = Mean Daily Return × 252
```

Annualized volatility is estimated using:

```text
Annual Volatility = Daily Volatility × √252
```

Portfolio volatility is calculated from the covariance matrix:

```text
Portfolio Volatility = √(wᵀΣw)
```

where:

- `w` represents the portfolio weight vector
- `Σ` represents the annualized covariance matrix

---

## 📐 Optimization Method

Portfolio optimization is implemented using **SciPy's SLSQP optimization algorithm**.

The optimization problems use the constraints:

```text
Sum of portfolio weights = 1
0 ≤ individual asset weight ≤ 1
```

Short selling and leverage are therefore not included in the current version.

---

## 🧠 Assumptions

The current QuantRisk model makes several simplifying assumptions:

- Historical returns provide useful information for estimating portfolio characteristics
- Approximately 252 trading days are used per year
- Portfolio weights are long-only
- Portfolio weights sum to 100%
- Transaction costs are ignored
- Taxes are ignored
- Bid-ask spreads and market impact are ignored
- Portfolio rebalancing costs are ignored
- Historical VaR and CVaR are estimated from observed historical returns
- Monte Carlo simulations use historical mean return and volatility
- Monte Carlo daily returns are generated using a normal distribution

These assumptions simplify the model and make the quantitative methodology transparent and reproducible.

---

## ⚠️ Limitations

QuantRisk is an analytical and educational decision-support project.

Important limitations include:

- Historical performance does not guarantee future performance
- Expected returns are sensitive to the selected historical period
- Correlations and covariance can change over time
- Financial returns may exhibit fat tails and volatility clustering that are not fully captured by a normal distribution
- Monte Carlo scenarios are simulations, not market forecasts
- Transaction costs and taxes are not included
- The model currently uses long-only portfolios
- Portfolio optimization can be sensitive to estimated expected returns and covariance
- Benchmark outperformance during a historical period does not imply future outperformance

The results should therefore be interpreted as **quantitative analytical estimates rather than investment recommendations**.

---

## 🛠️ Technologies

QuantRisk is developed using:

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- yfinance
- Streamlit
- Jupyter Notebook
- Git
- GitHub

---

## 📁 Project Structure

```text
QuantRisk/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   └── portfolio.py
│
├── notebooks/
│   ├── 01_setup.ipynb
│   ├── 02_data_collection.ipynb
│   └── 03_returns_analysis.ipynb
│
├── data/
│   ├── raw/
│   │   └── market_data_raw.csv
│   └── processed/
│       └── close_prices.csv
│
└── reports/
```

---

## 🚀 Running the Application

Clone the repository:

```bash
git clone https://github.com/mariamiziki/QuantRisk.git
```

Move into the project directory:

```bash
cd QuantRisk
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

---

## 📊 Example Workflow

A typical QuantRisk analysis can be performed as follows:

1. Select financial assets such as `AAPL`, `MSFT`, `JPM`, and `GLD`
2. Select the historical starting date
3. Enter the portfolio value
4. Enter the risk-free rate
5. Choose Minimum Variance or Maximum Sharpe
6. Run the portfolio analysis
7. Analyze asset correlation and diversification
8. Compare optimized strategies
9. Examine the Efficient Frontier
10. Review the recommended allocation
11. Compare the portfolio with the S&P 500
12. Analyze Maximum Drawdown, VaR, and CVaR
13. Examine Monte Carlo simulation results
14. Review the final decision-support interpretation

---

## 🎓 Academic Purpose

QuantRisk was developed as a quantitative finance and decision-support project combining concepts from:

- Portfolio Theory
- Financial Risk Management
- Statistical Analysis
- Numerical Optimization
- Monte Carlo Simulation
- Decision Support Systems

The project demonstrates how quantitative methods can be transformed into an interactive analytical application for portfolio evaluation and risk analysis.

---

## 🔮 Possible Future Improvements

Possible extensions include:

- Additional benchmark indices
- Rolling volatility and rolling correlation
- Parametric and Monte Carlo VaR
- Expected Shortfall extensions
- Black-Litterman portfolio optimization
- Portfolio rebalancing analysis
- Transaction cost modeling
- Alternative return distributions
- Stress testing and scenario analysis
- PDF or Excel report generation
- Deployment as an online application

---

## ⚖️ Disclaimer

QuantRisk is developed for **educational and analytical purposes only**.

It does not constitute financial advice, investment advice, or a recommendation to buy or sell any financial asset.

All quantitative results depend on historical data, model assumptions, and user-selected parameters.
