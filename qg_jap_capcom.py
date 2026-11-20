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
    '9697.T', '7203.T', '6758.T', '7974.T', '9984.T',
    '8306.T', '7267.T', '8035.T', '9983.T', '9433.T',
    '4063.T', '6861.T', '6098.T', '6501.T', '8001.T',
    '8316.T', '8411.T', '6367.T', '4502.T', '7269.T',
    '6954.T', '5108.T', '7751.T', '6752.T', '3382.T'
]
TARGET_TICKER = '9697.T'
BENCHMARK_TICKER = '^N225'

START_DATE = '2022-01-01'
END_DATE = '2024-06-01'
WINDOW_SIZE = 60

# --- 1. DATA ENGINE ---
def get_japanese_data():
    print("Step 1: Downloading Japanese Market Data...")

    # Download data
    u_data = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=False)['Adj Close'].ffill().dropna()
    b_data = yf.download(BENCHMARK_TICKER, start=START_DATE, end=END_DATE, auto_adjust=False)['Adj Close'].ffill().dropna()

    # Ensure common index
    common = u_data.index.intersection(b_data.index)
    u_data, b_data = u_data.loc[common], b_data.loc[common]

    # Calculate returns
    returns = u_data.pct_change().dropna()
    b_returns = b_data.pct_change().dropna()

    # Align again after pct_change
    common_ret = returns.index.intersection(b_returns.index)
    return returns.loc[common_ret], b_returns.loc[common_ret], u_data

# --- 2. NETWORK ANALYSIS ENGINE ---
def analyze_stock_network(returns):
    print(f"Step 2: Analyzing Network Interaction for {TARGET_TICKER}...")

    dates = returns.index

    # Metrics storage
    dates_analyzed = []
    actual_returns = []
    network_implied_returns = []
    centrality_scores = []
    degree_scores = []

    # For the final snapshot
    last_graph = None
    last_date = None

    # Optimization: Step every 10 days to avoid timeout
    step = 10
    for t in range(WINDOW_SIZE, len(dates) - 1, step):
        window = returns.iloc[t-WINDOW_SIZE : t]
        if t+1 >= len(returns): break
        next_ret_row = returns.iloc[t+1]
        current_date = dates[t]

        # Clean data for Glasso
        clean_window = window.dropna(axis=1)
        valid_cols = clean_window.columns[clean_window.std() > 1e-6]

        if TARGET_TICKER not in valid_cols:
            continue

        work_data = clean_window[valid_cols]
        centered = work_data.sub(work_data.mean(axis=1), axis=0)

        try:
            scaler = StandardScaler()
            X = scaler.fit_transform(centered)

            # Glasso
            try:
                glasso = GraphicalLassoCV(cv=3, max_iter=200).fit(X)
                prec = glasso.precision_

                # Calculate Partial Correlations for signed weights
                # rho_ij = - p_ij / sqrt(p_ii * p_jj)
                d = np.diag(prec)
                rho = -prec / np.sqrt(np.outer(d, d))

                adj = np.abs(prec)
            except:
                corr = np.corrcoef(X.T)
                rho = corr # Fallback to correlation if Glasso fails
                try: adj = np.abs(np.linalg.inv(corr))
                except: adj = np.abs(corr)

            np.fill_diagonal(adj, 0)
            G = nx.from_numpy_array(adj)

            # Map indices to tickers
            mapping = {i: col for i, col in enumerate(valid_cols)}
            rev_mapping = {col: i for i, col in enumerate(valid_cols)} # Needed for rho lookup
            G = nx.relabel_nodes(G, mapping)

            # Analyze Target Stock
            if TARGET_TICKER in G:
                # 1. Centrality
                try:
                    cent = nx.eigenvector_centrality_numpy(G)
                except:
                    try: cent = nx.eigenvector_centrality(G, max_iter=500)
                    except: cent = nx.degree_centrality(G)

                centrality = cent.get(TARGET_TICKER, 0)
                degree = G.degree(TARGET_TICKER)

                # 2. Network Implied Return
                # Find neighbors and edge weights
                neighbors = list(G.neighbors(TARGET_TICKER))

                if neighbors:
                    weighted_sum = 0
                    total_weight = 0

                    target_idx = rev_mapping[TARGET_TICKER]

                    for neighbor in neighbors:
                        # Use signed partial correlation (rho) for direction
                        neighbor_idx = rev_mapping[neighbor]

                        # Handle fallback case where rho might not be from precision matrix
                        try:
                            weight_signed = rho[target_idx, neighbor_idx]
                        except:
                            weight_signed = G[TARGET_TICKER][neighbor]['weight'] # Fallback

                        n_ret = next_ret_row.get(neighbor, 0)

                        weighted_sum += weight_signed * n_ret
                        total_weight += abs(weight_signed)

                    if total_weight > 0:
                        implied_ret = weighted_sum / total_weight
                    else:
                        implied_ret = 0
                else:
                    implied_ret = 0

                actual_ret = next_ret_row.get(TARGET_TICKER, 0)

                dates_analyzed.append(current_date)
                actual_returns.append(actual_ret)
                network_implied_returns.append(implied_ret)
                centrality_scores.append(centrality)
                degree_scores.append(degree)

                last_graph = G
                last_date = current_date

        except Exception as e:
            # print(f"Error at {current_date}: {e}")
            pass

    results = pd.DataFrame({
        'Actual': actual_returns,
        'Network_Implied': network_implied_returns,
        'Centrality': centrality_scores,
        'Degree': degree_scores
    }, index=dates_analyzed)

    return results, last_graph, last_date

# --- 3. VISUALIZATION ENGINE ---
def generate_report(results, graph, date):
    print("Step 3: Generating Report...")

    with PdfPages('capcom_network_analysis.pdf') as pdf:
        # PAGE 1: Performance & Interaction
        fig1 = plt.figure(figsize=(11.69, 8.27))
        gs = gridspec.GridSpec(3, 1, height_ratios=[1.5, 1, 1], figure=fig1)

        # Plot 1: Cumulative Returns
        ax1 = fig1.add_subplot(gs[0])
        cum_actual = (1 + results['Actual']).cumprod()
        cum_network = (1 + results['Network_Implied']).cumprod()

        ax1.plot(cum_actual.index, cum_actual, label=f'{TARGET_TICKER} Actual', color='blue', linewidth=2)
        ax1.plot(cum_network.index, cum_network, label='Network Implied (Neighbors)', color='orange', linestyle='--', linewidth=2)
        ax1.set_title(f"{TARGET_TICKER} vs Network Influence (Cumulative Return)", fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylabel("Growth of $1")

        # Plot 2: Rolling Correlation
        ax2 = fig1.add_subplot(gs[1])
        rolling_corr = results['Actual'].rolling(60).corr(results['Network_Implied'])
        ax2.plot(rolling_corr.index, rolling_corr, color='purple')
        ax2.set_title("Rolling 60-Day Correlation: Actual vs Network Implied", fontsize=12)
        ax2.axhline(0, color='black', linestyle=':', alpha=0.5)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylabel("Correlation")

        # Plot 3: Centrality
        ax3 = fig1.add_subplot(gs[2])
        ax3.plot(results.index, results['Centrality'], color='green', alpha=0.7)
        ax3.set_title(f"{TARGET_TICKER} Eigenvector Centrality", fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.set_ylabel("Centrality Score")

        plt.tight_layout()
        pdf.savefig(fig1)
        plt.close(fig1)

        # PAGE 2: Network Snapshot
        if graph:
            fig2 = plt.figure(figsize=(11.69, 8.27))
            ax_net = fig2.add_subplot(111)

            # Filter edges for visibility
            all_weights = [d['weight'] for u,v,d in graph.edges(data=True)]
            threshold = np.percentile(all_weights, 70) if len(all_weights) > 0 else 0
            edges = [(u, v) for (u, v, d) in graph.edges(data=True) if d.get('weight', 0) > threshold]

            # Position
            pos = nx.spring_layout(graph, k=0.5, seed=42)

            # Node Colors
            node_colors = []
            node_sizes = []

            neighbors = list(graph.neighbors(TARGET_TICKER)) if TARGET_TICKER in graph else []

            for node in graph.nodes():
                if node == TARGET_TICKER:
                    node_colors.append('red')
                    node_sizes.append(2000)
                elif node in neighbors:
                    node_colors.append('orange')
                    node_sizes.append(1000)
                else:
                    node_colors.append('lightblue')
                    node_sizes.append(300)

            nx.draw_networkx_nodes(graph, pos, ax=ax_net, node_size=node_sizes, node_color=node_colors, alpha=0.9)
            nx.draw_networkx_edges(graph, pos, ax=ax_net, edgelist=edges, edge_color='gray', alpha=0.2)
            nx.draw_networkx_labels(graph, pos, ax=ax_net, font_size=8, font_weight='bold')

            ax_net.set_title(f"Market Network Snapshot ({date.date()})\nRed: {TARGET_TICKER}, Orange: Neighbors", fontsize=14)
            ax_net.axis('off')

            pdf.savefig(fig2)
            plt.close(fig2)

    print("PDF generated: capcom_network_analysis.pdf")

if __name__ == "__main__":
    ret_data, bench_data, raw_prices = get_japanese_data()
    if not ret_data.empty:
        results, last_G, last_D = analyze_stock_network(ret_data)
        if not results.empty:
            generate_report(results, last_G, last_D)
        else:
            print("No analysis results generated.")
    else:
        print("Failed to download data.")
