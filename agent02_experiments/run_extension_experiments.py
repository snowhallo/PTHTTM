"""
agent02_experiments/run_extension_experiments.py
================================================
Extension simulations addressing Laboratory Questions 8, 9, and 10:
1. Extension A: Simultaneous Multi-Agent Q-Learning (Two learning agents competing simultaneously,
   evaluating non-stationarity, moving-target dynamics, and equilibrium convergence).
2. Extension B: Aggressive / Predatory Competitor (Competitor discounts aggressively with prob 0.8),
   evaluating RL agent adaptation in state (*, 1) and defensive margin preservation.
3. Extension C: Demand Elasticity & Inventory Holding Cost (Unsold goods incur holding cost c_h = 1.0/unit),
   evaluating pricing under storage constraints.
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from agent02_experiment import Config, ECommerceEnvironment, QLearningAgent, RuleBasedAgent

# ============================================================
# EXTENSION A: SIMULTANEOUS MULTI-AGENT Q-LEARNING (Q8 & Q9)
# ============================================================

def run_simultaneous_multiagent(config: Config, seed: int = 42):
    """
    Both Agent 1 and Agent 2 use Q-learning and update their policies simultaneously.
    This creates an environment with non-stationarity (the Markov property is violated
    from the perspective of either agent because the environment's transition/reward dynamics
    change as the other agent's policy changes).
    """
    rng = np.random.default_rng(seed)
    env = ECommerceEnvironment(config, seed=seed)
    
    agent1 = QLearningAgent(alpha=config.alpha, gamma=config.gamma, epsilon=config.epsilon_start, seed=seed + 1)
    agent2 = QLearningAgent(alpha=config.alpha, gamma=config.gamma, epsilon=config.epsilon_start, seed=seed + 2)
    
    epsilon = config.epsilon_start
    episodes = config.episodes
    steps_per_episode = config.steps_per_episode
    
    agent1_rewards = []
    agent2_rewards = []
    agent1_discount_rates = []
    agent2_discount_rates = []
    
    for ep in range(episodes):
        states = env.reset()
        ep_r1 = 0.0
        ep_r2 = 0.0
        ep_d1 = 0
        ep_d2 = 0
        
        for step in range(steps_per_episode):
            a1 = agent1.act(states[0], explore=True)
            a2 = agent2.act(states[1], explore=True)
            
            ep_d1 += a1
            ep_d2 += a2
            
            next_states, rewards, info = env.step([a1, a2])
            
            terminal = (step == steps_per_episode - 1)
            agent1.learn(states[0], a1, rewards[0], next_states[0], terminal=terminal)
            agent2.learn(states[1], a2, rewards[1], next_states[1], terminal=terminal)
            
            ep_r1 += rewards[0]
            ep_r2 += rewards[1]
            states = next_states
            
        epsilon = max(config.epsilon_min, epsilon * config.epsilon_decay)
        agent1.epsilon = epsilon
        agent2.epsilon = epsilon
        
        agent1_rewards.append(ep_r1)
        agent2_rewards.append(ep_r2)
        agent1_discount_rates.append(ep_d1 / steps_per_episode)
        agent2_discount_rates.append(ep_d2 / steps_per_episode)
        
    # Evaluate frozen policies
    agent1.epsilon = 0.0
    agent2.epsilon = 0.0
    eval_r1, eval_r2 = 0.0, 0.0
    eval_d1, eval_d2 = 0, 0
    total_steps = config.evaluation_episodes * steps_per_episode
    
    for ep in range(config.evaluation_episodes):
        states = env.reset()
        for step in range(steps_per_episode):
            a1 = agent1.act(states[0], explore=False)
            a2 = agent2.act(states[1], explore=False)
            eval_d1 += a1
            eval_d2 += a2
            next_states, rewards, info = env.step([a1, a2])
            eval_r1 += rewards[0]
            eval_r2 += rewards[1]
            states = next_states
            
    summary = {
        "scenario": "Simultaneous_MultiAgent_RL",
        "agent1_eval_mean_reward": eval_r1 / total_steps,
        "agent2_eval_mean_reward": eval_r2 / total_steps,
        "agent1_eval_discount_rate": eval_d1 / total_steps,
        "agent2_eval_discount_rate": eval_d2 / total_steps,
        "agent1_q_table": agent1.q.copy(),
        "agent2_q_table": agent2.q.copy(),
        "agent1_rewards_history": agent1_rewards,
        "agent2_rewards_history": agent2_rewards,
    }
    return summary


# ============================================================
# EXTENSION B: AGGRESSIVE COMPETITOR (Q9)
# ============================================================

class AggressiveCompetitor:
    """Competitor discounts aggressively with probability p_discount."""
    def __init__(self, p_discount=0.8, seed=999):
        self.p_discount = p_discount
        self.rng = np.random.default_rng(seed)
        
    def act(self, state):
        return 1 if self.rng.random() < self.p_discount else 0

def run_aggressive_competitor_experiment(config: Config, seed: int = 42, p_discount: float = 0.8):
    env = ECommerceEnvironment(config, seed=seed)
    agent = QLearningAgent(alpha=config.alpha, gamma=config.gamma, epsilon=config.epsilon_start, seed=seed + 10)
    opponent = AggressiveCompetitor(p_discount=p_discount, seed=seed + 20)
    
    epsilon = config.epsilon_start
    steps_per_episode = config.steps_per_episode
    rl_rewards = []
    opp_rewards = []
    
    for ep in range(config.episodes):
        states = env.reset()
        ep_r_rl, ep_r_opp = 0.0, 0.0
        for step in range(steps_per_episode):
            a_rl = agent.act(states[0], explore=True)
            a_opp = opponent.act(states[1])
            next_states, rewards, info = env.step([a_rl, a_opp])
            terminal = (step == steps_per_episode - 1)
            agent.learn(states[0], a_rl, rewards[0], next_states[0], terminal=terminal)
            ep_r_rl += rewards[0]
            ep_r_opp += rewards[1]
            states = next_states
        epsilon = max(config.epsilon_min, epsilon * config.epsilon_decay)
        agent.epsilon = epsilon
        rl_rewards.append(ep_r_rl)
        opp_rewards.append(ep_r_opp)
        
    # Evaluate
    agent.epsilon = 0.0
    total_eval_steps = config.evaluation_episodes * steps_per_episode
    eval_r_rl, eval_r_opp = 0.0, 0.0
    eval_d_rl, eval_d_opp = 0, 0
    
    for ep in range(config.evaluation_episodes):
        states = env.reset()
        for step in range(steps_per_episode):
            a_rl = agent.act(states[0], explore=False)
            a_opp = opponent.act(states[1])
            eval_d_rl += a_rl
            eval_d_opp += a_opp
            next_states, rewards, info = env.step([a_rl, a_opp])
            eval_r_rl += rewards[0]
            eval_r_opp += rewards[1]
            states = next_states
            
    return {
        "scenario": f"Aggressive_Competitor_p{p_discount}",
        "rl_eval_mean_reward": eval_r_rl / total_eval_steps,
        "opp_eval_mean_reward": eval_r_opp / total_eval_steps,
        "rl_eval_discount_rate": eval_d_rl / total_eval_steps,
        "opp_eval_discount_rate": eval_d_opp / total_eval_steps,
        "rl_q_table": agent.q.copy(),
        "rl_rewards_history": rl_rewards
    }


# ============================================================
# EXTENSION C: INVENTORY HOLDING COST & PENALTY (Q9 & Q10)
# ============================================================

class InventoryConstrainedEnvironment(ECommerceEnvironment):
    """
    E-Commerce Environment with inventory stocking & unsold holding penalty.
    Stock level = 15 units per step.
    Holding cost per unsold unit = $1.0.
    Unmet demand penalty = $1.0 per lost customer.
    """
    def __init__(self, config, stock_level=15, holding_cost=1.0, stockout_penalty=1.0, seed=None):
        super().__init__(config, seed=seed)
        self.stock_level = stock_level
        self.holding_cost = holding_cost
        self.stockout_penalty = stockout_penalty
        
    def step(self, actions):
        customers = self.config.low_demand_customers if self.demand == 0 else self.config.high_demand_customers
        rewards = []
        sales_list = []
        conversion_list = []
        
        for i in range(2):
            own_action = actions[i]
            comp_action = actions[1 - i]
            
            conv = 0.30 + 0.25 * self.demand + 0.15 * own_action - 0.10 * comp_action
            conv = float(np.clip(conv, 0.05, 0.95))
            demand_realized = int(self.rng.binomial(customers, conv))
            
            # Inventory constraints
            actual_sales = min(demand_realized, self.stock_level)
            unsold_units = max(0, self.stock_level - demand_realized)
            unmet_demand = max(0, demand_realized - self.stock_level)
            
            effective_price = self.config.price * (1.0 - self.config.discount_rate * own_action)
            gross_profit = actual_sales * (effective_price - self.config.unit_cost)
            penalties = unsold_units * self.holding_cost + unmet_demand * self.stockout_penalty
            net_profit = gross_profit - penalties
            
            rewards.append(float(net_profit))
            sales_list.append(actual_sales)
            conversion_list.append(conv)
            
        self.previous_actions = list(actions)
        self.demand = int(self.rng.integers(0, 2))
        next_states = self.get_states()
        info = {"sales": sales_list, "conversion": conversion_list, "customers": customers}
        return next_states, rewards, info

def run_inventory_experiment(config: Config, seed: int = 42):
    env = InventoryConstrainedEnvironment(config, stock_level=12, holding_cost=1.5, stockout_penalty=0.5, seed=seed)
    agent = QLearningAgent(alpha=config.alpha, gamma=config.gamma, epsilon=config.epsilon_start, seed=seed + 30)
    rule_opp = RuleBasedAgent()
    
    epsilon = config.epsilon_start
    steps_per_episode = config.steps_per_episode
    rl_rewards = []
    
    for ep in range(config.episodes):
        states = env.reset()
        ep_r = 0.0
        for step in range(steps_per_episode):
            a_rl = agent.act(states[0], explore=True)
            a_opp = rule_opp.act(states[1])
            next_states, rewards, info = env.step([a_rl, a_opp])
            terminal = (step == steps_per_episode - 1)
            agent.learn(states[0], a_rl, rewards[0], next_states[0], terminal=terminal)
            ep_r += rewards[0]
            states = next_states
        epsilon = max(config.epsilon_min, epsilon * config.epsilon_decay)
        agent.epsilon = epsilon
        rl_rewards.append(ep_r)
        
    # Evaluate
    agent.epsilon = 0.0
    total_eval_steps = config.evaluation_episodes * steps_per_episode
    eval_r_rl, eval_r_opp = 0.0, 0.0
    eval_d_rl, eval_d_opp = 0, 0
    
    for ep in range(config.evaluation_episodes):
        states = env.reset()
        for step in range(steps_per_episode):
            a_rl = agent.act(states[0], explore=False)
            a_opp = rule_opp.act(states[1])
            eval_d_rl += a_rl
            eval_d_opp += a_opp
            next_states, rewards, info = env.step([a_rl, a_opp])
            eval_r_rl += rewards[0]
            eval_r_opp += rewards[1]
            states = next_states
            
    return {
        "scenario": "Inventory_Holding_Cost",
        "rl_eval_mean_reward": eval_r_rl / total_eval_steps,
        "opp_eval_mean_reward": eval_r_opp / total_eval_steps,
        "rl_eval_discount_rate": eval_d_rl / total_eval_steps,
        "opp_eval_discount_rate": eval_d_opp / total_eval_steps,
        "rl_q_table": agent.q.copy(),
        "rl_rewards_history": rl_rewards
    }


# ============================================================
# MAIN RUNNER
# ============================================================

def main():
    cfg = Config()
    out_dir = Path("agent02_experiments/agent02_results")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("[*] Running Extension A: Simultaneous Multi-Agent Q-Learning...")
    res_a = run_simultaneous_multiagent(cfg, seed=42)
    print(f"    Agent 1 Eval Mean Reward: {res_a['agent1_eval_mean_reward']:.4f}, Discount Rate: {res_a['agent1_eval_discount_rate']:.4f}")
    print(f"    Agent 2 Eval Mean Reward: {res_a['agent2_eval_mean_reward']:.4f}, Discount Rate: {res_a['agent2_eval_discount_rate']:.4f}")
    
    print("[*] Running Extension B: Aggressive Competitor (p=0.8)...")
    res_b = run_aggressive_competitor_experiment(cfg, seed=42, p_discount=0.8)
    print(f"    RL Eval Mean Reward: {res_b['rl_eval_mean_reward']:.4f}, Discount Rate: {res_b['rl_eval_discount_rate']:.4f}")
    print(f"    Aggressive Opp Mean Reward: {res_b['opp_eval_mean_reward']:.4f}, Discount Rate: {res_b['opp_eval_discount_rate']:.4f}")
    
    print("[*] Running Extension C: Inventory Constraints & Holding Cost...")
    res_c = run_inventory_experiment(cfg, seed=42)
    print(f"    RL Eval Mean Reward: {res_c['rl_eval_mean_reward']:.4f}, Discount Rate: {res_c['rl_eval_discount_rate']:.4f}")
    print(f"    Rule Opp Mean Reward: {res_c['opp_eval_mean_reward']:.4f}, Discount Rate: {res_c['opp_eval_discount_rate']:.4f}")
    
    # Save Extension Results to CSV
    summary_rows = [
        {"Experiment": "Baseline (RL vs Fixed Rule)", "Agent": "RL Agent", "Mean_Reward_Per_Step": 35.1275, "Discount_Action_Rate": 0.0000},
        {"Experiment": "Baseline (RL vs Fixed Rule)", "Agent": "Rule-based Agent", "Mean_Reward_Per_Step": 34.9685, "Discount_Action_Rate": 0.0000},
        {"Experiment": "Extension A (Simultaneous RL)", "Agent": "Agent 1 (RL)", "Mean_Reward_Per_Step": res_a['agent1_eval_mean_reward'], "Discount_Action_Rate": res_a['agent1_eval_discount_rate']},
        {"Experiment": "Extension A (Simultaneous RL)", "Agent": "Agent 2 (RL)", "Mean_Reward_Per_Step": res_a['agent2_eval_mean_reward'], "Discount_Action_Rate": res_a['agent2_eval_discount_rate']},
        {"Experiment": "Extension B (Aggressive Opponent)", "Agent": "RL Agent", "Mean_Reward_Per_Step": res_b['rl_eval_mean_reward'], "Discount_Action_Rate": res_b['rl_eval_discount_rate']},
        {"Experiment": "Extension B (Aggressive Opponent)", "Agent": "Aggressive Opp (p=0.8)", "Mean_Reward_Per_Step": res_b['opp_eval_mean_reward'], "Discount_Action_Rate": res_b['opp_eval_discount_rate']},
        {"Experiment": "Extension C (Inventory Cost)", "Agent": "RL Agent", "Mean_Reward_Per_Step": res_c['rl_eval_mean_reward'], "Discount_Action_Rate": res_c['rl_eval_discount_rate']},
        {"Experiment": "Extension C (Inventory Cost)", "Agent": "Rule-based Opponent", "Mean_Reward_Per_Step": res_c['opp_eval_mean_reward'], "Discount_Action_Rate": res_c['opp_eval_discount_rate']},
    ]
    df_ext = pd.DataFrame(summary_rows)
    df_ext.to_csv(out_dir / "extension_experiments_summary.csv", index=False)
    print(f"[+] Saved extension results to {out_dir / 'extension_experiments_summary.csv'}")
    
    # Save Q-tables for Extension B & C
    with open(out_dir / "extension_q_tables.txt", "w", encoding="utf-8") as f:
        f.write("=== EXTENSION A: SIMULTANEOUS RL (AGENT 1) ===\n")
        for d in range(2):
            for c in range(2):
                q0 = res_a['agent1_q_table'][d, c, 0]
                q1 = res_a['agent1_q_table'][d, c, 1]
                f.write(f"State=({d}, {c}) | Q0={q0:.6f} | Q1={q1:.6f} | Greedy={np.argmax([q0, q1])}\n")
        f.write("\n=== EXTENSION B: AGGRESSIVE OPPONENT (RL AGENT) ===\n")
        for d in range(2):
            for c in range(2):
                q0 = res_b['rl_q_table'][d, c, 0]
                q1 = res_b['rl_q_table'][d, c, 1]
                f.write(f"State=({d}, {c}) | Q0={q0:.6f} | Q1={q1:.6f} | Greedy={np.argmax([q0, q1])}\n")
        f.write("\n=== EXTENSION C: INVENTORY HOLDING COST (RL AGENT) ===\n")
        for d in range(2):
            for c in range(2):
                q0 = res_c['rl_q_table'][d, c, 0]
                q1 = res_c['rl_q_table'][d, c, 1]
                f.write(f"State=({d}, {c}) | Q0={q0:.6f} | Q1={q1:.6f} | Greedy={np.argmax([q0, q1])}\n")
    print(f"[+] Saved extension Q-tables to {out_dir / 'extension_q_tables.txt'}")

if __name__ == "__main__":
    main()

