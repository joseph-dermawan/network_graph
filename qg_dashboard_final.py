import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import networkx as nx
import pandas as pd
import numpy as np
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler
import yfinance as yf
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
WINDOW_SIZE = 60
REBALANCE_DAYS = 20

# --- 1. DATA & BACKTEST ---
def get_data_and_backtest():
    print("Step 1: Downloading Data & Running Backtest...")
    
    u_data = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=False)['Adj Close'].ffill().dropna()
    b_data = yf.download(BENCHMARK_TICKER, start=START_DATE, end=END_DATE, auto_adjust=False)['Adj Close'].ffill().dropna()
    common = u_data.index.intersection(b_data.index)
    u_data, b_data = u_data.loc[common], b_data.loc[common]
    
    returns = u_data.pct_change().dropna()
    b_ret = b_data.pct_change().dropna()
    
    equity = [INITIAL_CAPITAL]
    bench = [INITIAL_CAPITAL]
    hold = [INITIAL_CAPITAL]
    curr_w = pd.Series(0, index=u_data.columns)
    history_dates = [returns.index[0]]
    
    for t in range(WINDOW_SIZE, len(returns) - 1):
        idx = returns.index[t]
        history_dates.append(idx)
        
        if t % REBALANCE_DAYS == 0:
            train = returns.iloc[t-WINDOW_SIZE : t]
            clean = train.dropna(axis=1)
            valid = clean.columns[clean.std() > 1e-6]
            if len(valid) > 5:
                work = clean[valid]
                centered = work.sub(work.mean(axis=1), axis=0)
                try:
                    scaler = StandardScaler()
                    X = scaler.fit_transform(centered)
                    glasso = GraphicalLassoCV(cv=3, max_iter=50).fit(X)
                    prec = glasso.precision_
                    adj = np.abs(prec)
                    np.fill_diagonal(adj, 0)
                    G = nx.from_numpy_array(adj)
                    
                    try: cent = nx.eigenvector_centrality_numpy(G)
                    except: 
                        try: cent = nx.eigenvector_centrality(G, max_iter=500)
                        except: cent = nx.degree_centrality(G)
                            
                    cent_s = pd.Series(list(cent.values()), index=valid)
                    mom = (1 + work).prod() - 1
                    score = cent_s * mom
                    top = score.nlargest(10).index
                    target = pd.Series(0.0, index=train.columns)
                    target[top] = 0.1
                    curr_w = target
                except:
                    pass

        next_ret = returns.iloc[t+1].fillna(0)
        pnl = np.sum(curr_w * next_ret)
        equity.append(equity[-1] * (1 + pnl))
        
        try: br = b_ret.iloc[t+1].item()
        except: br = float(b_ret.iloc[t+1])
        bench.append(bench[-1] * (1 + br))
        
        hr = np.mean(next_ret)
        hold.append(hold[-1] * (1 + hr))

    df_res = pd.DataFrame({
        'Strategy': equity,
        'S&P 500': bench,
        'Buy & Hold': hold
    }, index=history_dates)
    
    return df_res, returns

# --- 2. PDF GENERATION LOOP ---
def generate_pdf(df_results, returns_data):
    print("Step 2: Generating PDF Pages...")
    
    sector_map = {}
    for t in TICKERS:
        if t in ['XOM', 'CVX', 'COP', 'SLB']: sector_map[t] = '#ff4d4d' 
        elif t in ['NVDA', 'AMD', 'AAPL', 'MSFT', 'GOOGL']: sector_map[t] = '#00cc00' 
        elif t in ['JPM', 'BAC', 'GS', 'MS', 'V', 'MA']: sector_map[t] = '#ffd700' 
        else: sector_map[t] = '#4da6ff' 

    # Generate Monthly Snapshots
    step = 30 
    indices = range(WINDOW_SIZE, len(df_results), step)
    
    # Initialize PDF
    with PdfPages('strategy_dashboard.pdf') as pdf:
        for i, t in enumerate(indices):
            current_date = df_results.index[t]
            
            # Use fixed A4 Landscape size (inches)
            fig = plt.figure(figsize=(11.69, 8.27)) 
            gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1.5], figure=fig)
            
            # --- TOP PANEL ---
            ax_top = fig.add_subplot(gs[0])
            subset = df_results.iloc[:t]
            
            ax_top.plot(subset.index, subset['Strategy'], color='blue', linewidth=2, label='Centrality Strat')
            ax_top.plot(subset.index, subset['S&P 500'], color='black', alpha=0.6, label='S&P 500')
            ax_top.plot(subset.index, subset['Buy & Hold'], color='gray', linestyle='--', alpha=0.5, label='Univ Buy&Hold')
            
            ax_top.set_title(f"Performance vs Market ({current_date.date()})", fontsize=14, fontweight='bold')
            ax_top.legend(loc='upper left', fontsize=8)
            ax_top.grid(True, alpha=0.3)
            ax_top.set_ylabel("Portfolio Value ($)")
            
            # Fixed Axes for consistency across PDF pages
            ax_top.set_xlim(df_results.index[0], df_results.index[-1])
            ax_top.set_ylim(0.8 * df_results.min().min(), 1.1 * df_results.max().max())
            ax_top.axvline(x=current_date, color='red', linestyle=':', alpha=0.8)
            
            vals = ax_top.get_yticks()
            ax_top.set_yticklabels(['${:,.0f}'.format(x) for x in vals])

            # --- BOTTOM PANEL ---
            ax_bot = fig.add_subplot(gs[1])
            
            try:
                window = returns_data.iloc[t-WINDOW_SIZE : t]
                clean = window.dropna(axis=1)
                valid = clean.columns[clean.std() > 1e-6]
                
                if len(valid) < 5: raise ValueError("Not enough stocks")
                clean = clean[valid]
                centered = clean.sub(clean.mean(axis=1), axis=0)
                
                scaler = StandardScaler()
                X = scaler.fit_transform(centered)
                
                try:
                    glasso = GraphicalLassoCV(cv=3, max_iter=200).fit(X)
                    adj = np.abs(glasso.precision_)
                except:
                    corr = np.corrcoef(X.T)
                    try: adj = np.abs(np.linalg.inv(corr))
                    except: adj = np.abs(corr)

                np.fill_diagonal(adj, 0)
                
                G = nx.from_numpy_array(adj)
                mapping = {i: col for i, col in enumerate(valid)}
                G = nx.relabel_nodes(G, mapping)
                
                all_weights = [d['weight'] for u,v,d in G.edges(data=True)]
                threshold = np.percentile(all_weights, 85) if len(all_weights) > 0 else 0
                edges = [(u, v) for (u, v, d) in G.edges(data=True) if d.get('weight', 0) > threshold]
                
                try: cent = nx.eigenvector_centrality_numpy(G)
                except: 
                    try: cent = nx.eigenvector_centrality(G, max_iter=500)
                    except: cent = nx.degree_centrality(G)
                
                node_sizes = [cent.get(n, 0) * 3000 for n in G.nodes()]
                node_colors = [sector_map.get(n, 'gray') for n in G.nodes()]
                
                pos = nx.spring_layout(G, k=0.4, seed=42)
                
                nx.draw_networkx_nodes(G, pos, ax=ax_bot, node_size=node_sizes, node_color=node_colors, alpha=0.9)
                nx.draw_networkx_edges(G, pos, ax=ax_bot, edgelist=edges, edge_color='gray', alpha=0.3)
                nx.draw_networkx_labels(G, pos, ax=ax_bot, font_size=9, font_weight='bold')
                
                ax_bot.set_title("Market Structure (Green=Tech, Red=Energy, Gold=Finance)", fontsize=10)
                ax_bot.axis('off')
                
            except Exception as e:
                ax_bot.text(0.5, 0.5, f"Graph Computation Error: {str(e)}", ha='center')
                ax_bot.axis('off')

            pdf.savefig(fig) 
            plt.close(fig) 
            
            if i % 10 == 0: print(f"Saved page {i}/{len(indices)}")
    
    print("pdf is ready: strategy_dashboard.pdf")

if __name__ == "__main__":
    res, ret = get_data_and_backtest()
    generate_pdf(res, ret)