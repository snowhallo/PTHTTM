"""
agent02_experiments/generate_report_plots.py
============================================
Generates high-resolution (300 DPI) academic-grade figures for the AGENT_02 report:
- Fig 1: Multi-Agent E-Commerce Architecture Diagram
- Fig 2: Baseline RL Training Convergence Curve (Episode Reward & 100-step MA)
- Fig 3: Parameter Study: Learning Rate Comparison (alpha in {0.01, 0.10, 0.50})
- Fig 4: Parameter Study: Exploration Strategy Comparison (Low, Baseline, High)
- Fig 5: Learned Q-Table Heatmap (4 States x 2 Actions)
- Fig 6: Multi-Seed Robustness Evaluation (Boxplot across 5 Seeds)
- Fig 7: Extension Experiments: Dynamic Opponents & Inventory Constraints
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# UTF-8 configuration
sys.stdout.reconfigure(encoding='utf-8')

# Set matplotlib publication style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.grid': True,
    'grid.alpha': 0.35,
    'grid.linestyle': '--'
})

RESULTS_DIR = Path("agent02_experiments/agent02_results")
PLOTS_DIR = Path("agent02_experiments/report_figures")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# FIG 1: Multi-Agent E-Commerce Architecture Diagram
# -------------------------------------------------------------------
def generate_fig1_architecture():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis('off')
    
    # Environment Box
    env_box = patches.FancyBboxPatch((3.0, 1.2), 4.0, 3.2, boxstyle="round,pad=0.2",
                                     edgecolor='#1f77b4', facecolor='#e8f4f8', linewidth=2)
    ax.add_patch(env_box)
    ax.text(5.0, 4.0, "E-COMMERCE MARKETPLACE ENVIRONMENT", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#104e8b')
    ax.text(5.0, 3.3, r"State: $s_i(t) = (d_t, c_i(t)) \in \{0, 1\}^2$", ha='center', va='center',
            fontsize=10.5, color='#333333')
    ax.text(5.0, 2.6, r"Demand: $N_t = 10$ ($d_t=0$) or $20$ ($d_t=1$)", ha='center', va='center',
            fontsize=10, color='#333333')
    ax.text(5.0, 1.9, r"Conversion: $p_i = \mathrm{clip}(0.30 + 0.25d_t + 0.15a_i - 0.10a_{-i})$",
            ha='center', va='center', fontsize=9.5, color='#222222')
    ax.text(5.0, 1.4, r"Reward: $r_i = S_i \times [P(1 - \delta a_i) - C]$, $S_i \sim \mathrm{Binomial}(N_t, p_i)$",
            ha='center', va='center', fontsize=9.5, color='#b22222', fontweight='bold')
    
    # Agent 1 (RL Agent)
    rl_box = patches.FancyBboxPatch((0.2, 1.8), 2.2, 2.2, boxstyle="round,pad=0.15",
                                    edgecolor='#2ca02c', facecolor='#ebfaeb', linewidth=2)
    ax.add_patch(rl_box)
    ax.text(1.3, 3.6, "AGENT 1 (RL)", ha='center', va='center', fontsize=11, fontweight='bold', color='#1b611b')
    ax.text(1.3, 3.0, "Tabular Q-Learning\n" + r"$\alpha=0.10, \gamma=0.90$" + "\n" + r"$\epsilon$-Greedy Decay",
            ha='center', va='center', fontsize=9.5, color='#222222')
    ax.text(1.3, 2.1, r"$Q(s, a) \leftarrow Q + \alpha \delta_{TD}$", ha='center', va='center',
            fontsize=9.5, color='#1b611b', fontweight='bold')
    
    # Agent 2 (Rule-Based Opponent)
    rule_box = patches.FancyBboxPatch((7.6, 1.8), 2.2, 2.2, boxstyle="round,pad=0.15",
                                      edgecolor='#d62728', facecolor='#fdf0f0', linewidth=2)
    ax.add_patch(rule_box)
    ax.text(8.7, 3.6, "AGENT 2 (Rule-Based)", ha='center', va='center', fontsize=11, fontweight='bold', color='#8b1a1a')
    ax.text(8.7, 3.0, "Fixed Policy IF/THEN\n" + r"Rule 1: $d=0 \to a=0$" + "\n" + r"Rule 2: $d=1, c=1 \to a=1$" + "\n" + r"Rule 3: $d=1, c=0 \to a=0$",
            ha='center', va='center', fontsize=9.0, color='#222222')
    ax.text(8.7, 2.05, "Deterministic Expert", ha='center', va='center',
            fontsize=9.0, color='#8b1a1a', fontstyle='italic')
    
    # Arrows and Annotations
    # Agent 1 -> Env (Action a1)
    ax.annotate("", xy=(3.0, 3.2), xytext=(2.4, 3.2),
                arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2))
    ax.text(2.7, 3.4, r"$a_1(t)$", ha='center', va='bottom', fontsize=10.5, color='#2ca02c', fontweight='bold')
    
    # Env -> Agent 1 (State s1, Reward r1)
    ax.annotate("", xy=(2.4, 2.4), xytext=(3.0, 2.4),
                arrowprops=dict(arrowstyle="->", color='#1f77b4', lw=2))
    ax.text(2.7, 2.1, r"$s_1(t), r_1(t)$", ha='center', va='top', fontsize=10.5, color='#1f77b4', fontweight='bold')
    
    # Agent 2 -> Env (Action a2)
    ax.annotate("", xy=(7.0, 3.2), xytext=(7.6, 3.2),
                arrowprops=dict(arrowstyle="->", color='#d62728', lw=2))
    ax.text(7.3, 3.4, r"$a_2(t)$", ha='center', va='bottom', fontsize=10.5, color='#d62728', fontweight='bold')
    
    # Env -> Agent 2 (State s2, Reward r2)
    ax.annotate("", xy=(7.6, 2.4), xytext=(7.0, 2.4),
                arrowprops=dict(arrowstyle="->", color='#1f77b4', lw=2))
    ax.text(7.3, 2.1, r"$s_2(t), r_2(t)$", ha='center', va='top', fontsize=10.5, color='#1f77b4', fontweight='bold')
    
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(0.8, 4.8)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_1_system_architecture.png")
    plt.close()
    print("[+] Generated fig_1_system_architecture.png")


# -------------------------------------------------------------------
# FIG 2: Baseline RL Training Convergence Curve
# -------------------------------------------------------------------
def generate_fig2_training_curve():
    csv_file = RESULTS_DIR / "baseline_episode_rewards.csv"
    if not csv_file.exists():
        print("[-] baseline_episode_rewards.csv not found")
        return
    df = pd.read_csv(csv_file)
    
    # Calculate moving averages
    window = 100
    df['rl_ma'] = df['rl_episode_reward'].rolling(window=window, min_periods=1).mean()
    df['rule_ma'] = df['rule_episode_reward'].rolling(window=window, min_periods=1).mean()
    df['rl_std'] = df['rl_episode_reward'].rolling(window=window, min_periods=1).std().fillna(0)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={'height_ratios': [2.5, 1]})
    
    # Upper Plot: Episode Rewards
    ax1.plot(df['episode'], df['rl_episode_reward'], color='#2ca02c', alpha=0.15, label='RL Episode Reward (Raw)')
    ax1.plot(df['episode'], df['rl_ma'], color='#1b611b', linewidth=2.0, label=f'RL Moving Average (window={window})')
    ax1.fill_between(df['episode'], df['rl_ma'] - df['rl_std'], df['rl_ma'] + df['rl_std'], color='#2ca02c', alpha=0.2, label=r'RL MA $\pm 1\sigma$')
    
    ax1.plot(df['episode'], df['rule_ma'], color='#d62728', linewidth=1.8, linestyle='--', label=f'Rule-based MA (window={window})')
    
    ax1.set_ylabel("Total Reward per Episode (20 steps)")
    ax1.set_title("Figure 2: Baseline Q-Learning Agent Training Convergence (5,000 Episodes)", fontweight='bold')
    ax1.legend(loc='lower right', framealpha=0.9)
    
    # Lower Plot: Epsilon Decay
    ax2.plot(df['episode'], df['epsilon'], color='#ff7f0e', linewidth=2.0, label=r'Exploration Rate ($\epsilon$)')
    ax2.set_xlabel("Training Episode")
    ax2.set_ylabel(r"$\epsilon$ Value")
    ax2.set_ylim(0, 0.22)
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_2_baseline_training.png")
    plt.close()
    print("[+] Generated fig_2_baseline_training.png")


# -------------------------------------------------------------------
# FIG 3: Learning Rate Comparison
# -------------------------------------------------------------------
def generate_fig3_learning_rate():
    csv_file = RESULTS_DIR / "learning_rate_comparison.csv"
    if not csv_file.exists():
        return
    df = pd.read_csv(csv_file)
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    x = np.arange(len(df['alpha']))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, df['rl_mean_reward_per_step'], width, label='Mean Reward / Step ($/step)',
                    color=['#1f77b4', '#2ca02c', '#d62728'], edgecolor='black', alpha=0.85)
    
    ax1.set_ylabel("Mean Reward per Step ($)", fontweight='bold')
    ax1.set_title("Figure 3: Sensitivity Analysis on Learning Rate $\\alpha \\in \\{0.01, 0.10, 0.50\\}$", fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"α = {a}\n({'Slow' if a==0.01 else 'Optimal' if a==0.10 else 'Unstable'})" for a in df['alpha']])
    ax1.set_ylim(0, 42)
    
    # Add values on top of bars
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"${yval:.2f}", ha='center', va='bottom', fontweight='bold', fontsize=10)
        
    # Second y-axis for discount rate
    ax2 = ax1.twinx()
    ax2.grid(False)
    bars2 = ax2.bar(x + width/2, df['rl_discount_action_rate'] * 100, width, label='Discount Action Rate (%)',
                    color='#ff7f0e', edgecolor='black', alpha=0.75)
    ax2.set_ylabel("Discount Action Rate (%)", color='#cc5500', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#cc5500')
    ax2.set_ylim(0, 60)
    
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', color='#cc5500', fontweight='bold', fontsize=10)
        
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_3_learning_rate.png")
    plt.close()
    print("[+] Generated fig_3_learning_rate.png")


# -------------------------------------------------------------------
# FIG 4: Exploration Strategy Comparison
# -------------------------------------------------------------------
def generate_fig4_exploration():
    csv_file = RESULTS_DIR / "exploration_comparison.csv"
    if not csv_file.exists():
        return
    df = pd.read_csv(csv_file)
    
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.arange(len(df['exploration_setting']))
    
    bars = ax.bar(x, df['rl_mean_reward_per_step'], width=0.45,
                  color=['#3b528b', '#21918c', '#5ec962'], edgecolor='black', alpha=0.88)
    
    ax.set_ylabel("Evaluation Mean Reward / Step ($)", fontweight='bold')
    ax.set_title("Figure 4: Impact of Exploration Policy on Post-Training Evaluation", fontweight='bold')
    ax.set_xticks(x)
    labels = [
        "Low (0.05 → 0.01)\nUnder-exploration",
        "Baseline (0.20 → 0.02)\nBalanced Decay",
        "High (0.50 → 0.05)\nOver-exploration"
    ]
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 42)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 0.8, f"${h:.3f}", ha='center', va='bottom', fontweight='bold', fontsize=10.5)
        
    ax.axhline(35.1275, color='gray', linestyle=':', label='Baseline Mean ($35.128)')
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_4_exploration.png")
    plt.close()
    print("[+] Generated fig_4_exploration.png")


# -------------------------------------------------------------------
# FIG 5: Learned Q-Table Heatmap
# -------------------------------------------------------------------
def generate_fig5_qtable_heatmap():
    # Values extracted from agent02_results/q_tables.txt
    # State: (0,0), (0,1), (1,0), (1,1)
    # Q(s, a0: No Discount), Q(s, a1: Discount)
    states = [
        "State (0, 0)\nLow Demand, Comp No-Disc",
        "State (0, 1)\nLow Demand, Comp Disc",
        "State (1, 0)\nHigh Demand, Comp No-Disc",
        "State (1, 1)\nHigh Demand, Comp Disc"
    ]
    actions = ["Action 0: No Discount", "Action 1: Discount (20%)"]
    
    q_matrix = np.array([
        [228.302398, 178.849438],
        [177.992001, 207.205116],
        [246.879938, 235.233833],
        [211.419819, 242.962865]
    ])
    
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(q_matrix, cmap='YlGnBu', aspect='auto')
    
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Expected Cumulative Return Q(s, a)", rotation=-90, va="bottom", fontweight='bold')
    
    ax.set_xticks(np.arange(len(actions)))
    ax.set_yticks(np.arange(len(states)))
    ax.set_xticklabels(actions, fontweight='bold')
    ax.set_yticklabels(states, fontweight='bold')
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(states)):
        best_a = np.argmax(q_matrix[i])
        for j in range(len(actions)):
            val = q_matrix[i, j]
            is_best = (j == best_a)
            text_str = f"{val:.2f}\n{'[BEST]' if is_best else ''}"
            color = "white" if val > 220 else "black"
            weight = "bold" if is_best else "normal"
            ax.text(j, i, text_str, ha="center", va="center", color=color,
                    fontweight=weight, fontsize=11)
            
    ax.set_title("Figure 5: Learned Q-Value Matrix Q(s, a) and Greedy Optimal Policy", fontweight='bold', pad=15)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_5_qtable_heatmap.png")
    plt.close()
    print("[+] Generated fig_5_qtable_heatmap.png")


# -------------------------------------------------------------------
# FIG 6: Multi-Seed Robustness Evaluation (Boxplot)
# -------------------------------------------------------------------
def generate_fig6_multi_seed():
    csv_file = RESULTS_DIR / "multi_seed_summary.csv"
    if not csv_file.exists():
        return
    df = pd.read_csv(csv_file)
    
    rl_rewards = df[df['agent'] == 'RL']['mean_reward_per_step'].values
    rule_rewards = df[df['agent'] == 'Rule-based']['mean_reward_per_step'].values
    
    fig, ax = plt.subplots(figsize=(7, 5))
    
    data = [rl_rewards, rule_rewards]
    box = ax.boxplot(data, tick_labels=['RL Agent (Q-Learning)', 'Rule-Based Agent'],
                     patch_artist=True, widths=0.45, medianprops=dict(color='black', lw=2))
    
    colors = ['#2ca02c', '#d62728']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
        
    # Overlay individual data points
    for i, pts in enumerate(data):
        x = np.random.normal(i + 1, 0.04, size=len(pts))
        ax.plot(x, pts, 'o', color='darkblue', alpha=0.8, markersize=8)
        
    ax.set_ylabel("Evaluation Mean Reward per Step ($)", fontweight='bold')
    ax.set_title("Figure 6: Robustness & Statistical Dispersion across 5 Random Seeds", fontweight='bold')
    ax.set_ylim(34.2, 35.8)
    
    # Statistical annotations
    ax.text(1, 34.35, f"RL: μ={np.mean(rl_rewards):.3f}\nσ={np.std(rl_rewards):.3f}",
            ha='center', fontsize=9.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(2, 34.35, f"Rule: μ={np.mean(rule_rewards):.3f}\nσ={np.std(rule_rewards):.3f}",
            ha='center', fontsize=9.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_6_multi_seed_boxplot.png")
    plt.close()
    print("[+] Generated fig_6_multi_seed_boxplot.png")


# -------------------------------------------------------------------
# FIG 7: Extension Experiments Comparison
# -------------------------------------------------------------------
def generate_fig7_extension():
    csv_file = RESULTS_DIR / "extension_experiments_summary.csv"
    if not csv_file.exists():
        print("[-] extension_experiments_summary.csv not found yet, will generate after run completes.")
        return
    df = pd.read_csv(csv_file)
    
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    
    # Group by Experiment
    exps = df['Experiment'].unique()
    x = np.arange(len(exps))
    width = 0.35
    
    # For each experiment, pick RL vs Opponent
    rl_means = []
    opp_means = []
    
    for exp in exps:
        sub = df[df['Experiment'] == exp]
        rl_means.append(sub.iloc[0]['Mean_Reward_Per_Step'])
        opp_means.append(sub.iloc[1]['Mean_Reward_Per_Step'])
        
    bars1 = ax1.bar(x - width/2, rl_means, width, label='Agent 1 (RL)', color='#2ca02c', edgecolor='black', alpha=0.85)
    bars2 = ax1.bar(x + width/2, opp_means, width, label='Agent 2 (Opponent)', color='#1f77b4', edgecolor='black', alpha=0.85)
    
    ax1.set_ylabel("Evaluation Mean Reward / Step ($)", fontweight='bold')
    ax1.set_title("Figure 7: Extension Experiments: Non-Stationarity, Aggressive Opponent & Inventory Cost", fontweight='bold')
    ax1.set_xticks(x)
    labels = [
        "Baseline\n(RL vs Fixed Rule)",
        "Ext A: Simultaneous\n(Two RL Agents)",
        "Ext B: Aggressive\n(Opponent p=0.8)",
        "Ext C: Inventory Cost\n(Holding & Penalty)"
    ]
    ax1.set_xticklabels(labels)
    ax1.set_ylim(0, 42)
    
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, h + 0.7, f"${h:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=9.5)
        
    for bar in bars2:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, h + 0.7, f"${h:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=9.5)
        
    ax1.legend(loc='upper right')
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "fig_7_extension_dynamic.png")
    plt.close()
    print("[+] Generated fig_7_extension_dynamic.png")


def main():
    print("[*] Generating Publication-Grade Figures (300 DPI)...")
    generate_fig1_architecture()
    generate_fig2_training_curve()
    generate_fig3_learning_rate()
    generate_fig4_exploration()
    generate_fig5_qtable_heatmap()
    generate_fig6_multi_seed()
    generate_fig7_extension()
    print("[+] All Figures Generated in:", PLOTS_DIR.resolve())

if __name__ == "__main__":
    main()
