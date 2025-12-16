import yfinance as yf
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore")

# --- CONFIGURATION ---
TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'AMD', 'CRM', 'ADBE', 'INTC', 'CSCO', 'QCOM',
    'JPM', 'BAC', 'GS', 'MS', 'V', 'MA',
    'XOM', 'CVX', 'COP', 'SLB',
    'JNJ', 'PFE', 'UNH', 'LLY', 'MRK',
    'AMZN', 'TSLA', 'HD', 'MCD', 'PG', 'KO', 'PEP', 'WMT', 'COST',
    'CAT', 'BA', 'HON', 'GE', 'DIS'
]
BENCHMARK_TICKER = '^GSPC' 

START_DATE = '2019-01-01'
END_DATE = '2024-06-01'
INITIAL_CAPITAL = 1_000_000
TRANSACTION_COST_BPS = 0.0010 
WINDOW_SIZE = 60
REBALANCE_DAYS = 20  

# --- 1. DATA ENGINE ---
def get_data(tickers, benchmark, start, end):
    print("Downloading Final Data...")
    u_data = yf.download(tickers, start=start, end=end, auto_adjust=False)['Adj Close'].ffill().dropna()
    b_data = yf.download(benchmark, start=start, end=end, auto_adjust=False)['Adj Close'].ffill().dropna()
    common = u_data.index.intersection(b_data.index)
    return u_data.loc[common], b_data.loc[common]

# --- 2. STRATEGY ENGINE ---
class CentralityMomentumStrategy:
    def __init__(self, lookback=60):
        self.lookback = lookback
        
    def get_allocation(self, historical_returns):
        clean_hist = historical_returns.dropna(axis=1)
        valid_cols = clean_hist.columns[clean_hist.std() > 1e-6]
        work_data = clean_hist[valid_cols]
        centered = work_data.sub(work_data.mean(axis=1), axis=0)
        
        try:
            scaler = StandardScaler()
            X = scaler.fit_transform(centered)
            
            # --- GRAPH BUILDING ---
            try:
                glasso = GraphicalLassoCV(cv=3, max_iter=200).fit(X)
                prec = glasso.precision_
                adj = np.abs(prec)
            except:
                corr = np.corrcoef(X.T)
                try: adj = np.abs(np.linalg.inv(corr))
                except: adj = np.abs(corr)
                
            np.fill_diagonal(adj, 0)
            G = nx.from_numpy_array(adj)
            
            # --- CENTRALITY CALCULATION ---
            try:
                centrality = nx.eigenvector_centrality_numpy(G)
            except:
                try:
                    centrality = nx.eigenvector_centrality(G, max_iter=500)
                except:
                    centrality = nx.degree_centrality(G)
            
            centrality_series = pd.Series(list(centrality.values()), index=valid_cols)
            
        except:
            return pd.Series(1/len(valid_cols), index=valid_cols)

        # Momentum Calculation
        momentum = (1 + work_data).prod() - 1
        score = centrality_series * momentum
        
        top_n = 10
        top_stocks = score.nlargest(top_n).index
        allocation = pd.Series(0.0, index=historical_returns.columns)
        allocation[top_stocks] = 1.0 / top_n 
        
        return allocation

# --- 3. METRICS ENGINE ---
def calculate_metrics(equity_curve, bench_curve):
    ret = pd.Series(equity_curve).pct_change().dropna()
    bench = pd.Series(bench_curve).pct_change().dropna()
    
    days = len(equity_curve)
    cagr = (equity_curve[-1] / equity_curve[0]) ** (252/days) - 1
    
    rf = 0.04 / 252
    excess = ret - rf
    sharpe = np.sqrt(252) * (excess.mean() / ret.std())
    
    downside = excess[excess < 0]
    sortino = np.sqrt(252) * (excess.mean() / downside.std())
    
    peak = pd.Series(equity_curve).cummax()
    dd = (pd.Series(equity_curve) - peak) / peak
    max_dd = dd.min()
    
    cov = np.cov(ret, bench)[0,1]
    var = np.var(bench)
    beta = cov / var
    
    return {
        "CAGR": cagr,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_dd,
        "Beta": beta
    }

# --- 4. BACKTESTER ---
class Backtester:
    def __init__(self, prices, benchmark_prices, strategy, capital, cost_bps):
        self.prices = prices
        self.returns = prices.pct_change().dropna()
        
        self.bench_prices = benchmark_prices
        self.bench_returns = benchmark_prices.pct_change().dropna()
        
        common = self.returns.index.intersection(self.bench_returns.index)
        self.returns = self.returns.loc[common]
        self.bench_returns = self.bench_returns.loc[common]
        
        self.strategy = strategy
        self.capital = capital
        self.cost_bps = cost_bps
        
        self.equity_curve = [capital]
        self.benchmark_curve = [capital]
        self.hold_curve = [capital] 
        
    def run(self):
        print(f"Starting Backtest ({len(self.returns)} days)...")
        dates = self.returns.index
        current_weights = pd.Series(0, index=self.returns.columns)
        
        for t in range(self.strategy.lookback, len(dates) - 1):
            
            # Rebalance Logic
            if t % REBALANCE_DAYS == 0:
                train = self.returns.iloc[t-self.strategy.lookback : t]
                target_weights = self.strategy.get_allocation(train)
                
                turnover = np.abs(target_weights - current_weights).sum()
                cost = turnover * self.cost_bps * self.equity_curve[-1]
                
                current_weights = target_weights
                self.equity_curve[-1] -= cost
            
            # 1. Strategy PnL
            next_ret = self.returns.iloc[t+1].fillna(0)
            port_ret = np.sum(current_weights * next_ret)
            self.equity_curve.append(self.equity_curve[-1] * (1 + port_ret))
            
            # 2. Benchmark PnL (S&P 500)
            try: sp_ret = self.bench_returns.iloc[t+1].item()
            except: sp_ret = float(self.bench_returns.iloc[t+1])
            self.benchmark_curve.append(self.benchmark_curve[-1] * (1 + sp_ret))
            
            # 3. Universe Buy & Hold PnL (Equal Weight)
            univ_ret = np.mean(next_ret)
            self.hold_curve.append(self.hold_curve[-1] * (1 + univ_ret))
            
            if t % 200 == 0:
                print(f"Day {t} | Strat: ${self.equity_curve[-1]:,.0f} | Bench: ${self.benchmark_curve[-1]:,.0f}")
        
        self.report()

    def report(self):
        # Calculate Metrics
        m = calculate_metrics(self.equity_curve, self.benchmark_curve)
        
        print("\n--- FINAL PERFORMANCE METRICS ---")
        print(f"Final Capital: ${self.equity_curve[-1]:,.2f}")
        print(f"CAGR:          {m['CAGR']:.2%}")
        print(f"Sharpe Ratio:  {m['Sharpe']:.2f}")
        print(f"Sortino Ratio: {m['Sortino']:.2f}")
        print(f"Max Drawdown:  {m['Max Drawdown']:.2%}")
        print(f"Beta:          {m['Beta']:.2f}")
        
        # Plotting in DOLLARS
        plt.figure(figsize=(12, 6))
        plt.plot(self.equity_curve, label='Graph Centrality Strategy', color='blue', linewidth=2)
        plt.plot(self.benchmark_curve, label='S&P 500 Benchmark', color='black', linewidth=1.5)
        plt.plot(self.hold_curve, label='Universe Buy & Hold (Eq Weight)', color='gray', linestyle='--', alpha=0.7)
        
        plt.title(f"Performance: $1M Initial Capital (Monthly Rebalance)", fontsize=14)
        plt.ylabel("Portfolio Value ($)")
        plt.xlabel("Trading Days")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Format Y-axis as currency
        current_values = plt.gca().get_yticks()
        plt.gca().set_yticklabels(['${:,.0f}'.format(x) for x in current_values])
        
        plt.savefig('final_dollar_performance.png')
        print("\nChart saved to 'final_dollar_performance.png'")

if __name__ == "__main__":
    u_data, b_data = get_data(TICKERS, BENCHMARK_TICKER, START_DATE, END_DATE)
    if not u_data.empty:
        strat = CentralityMomentumStrategy(lookback=WINDOW_SIZE)
        bt = Backtester(u_data, b_data, strat, INITIAL_CAPITAL, TRANSACTION_COST_BPS)
        bt.run()