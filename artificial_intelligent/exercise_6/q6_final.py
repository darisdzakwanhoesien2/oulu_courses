import numpy as np
from collections import defaultdict

# Define the episodes
training_episodes = [
    [((3,4),'S',(3,3),0), ((3,3),'S',(3,2),0), ((3,2),'S',(3,1),0), ((3,1),'Exit','Done',50)],
    [((3,4),'S',(3,3),0), ((3,3),'S',(3,2),0), ((3,2),'W',(2,2),0), ((2,2),'S',(2,1),0), ((2,1),'Exit','Done',-30)],
    [((3,4),'W',(2,4),0), ((2,4),'W',(1,4),0), ((1,4),'S',(1,3),0), ((1,3),'E',(2,3),0), ((2,3),'Exit','Done',-50)],
    [((3,4),'W',(2,4),0), ((2,4),'W',(1,4),0), ((1,4),'S',(1,3),0), ((1,3),'S',(1,2),0), ((1,2),'S',(1,1),0), ((1,1),'Exit','Done',100)],
]

# Parameters
alpha = 0.5
gamma = 1.0

# Q-values initialization
Q_values = defaultdict(float)

# Process episodes to extract relevant Q-values
for episode in training_episodes:
    G = 0  # Initialize cumulative reward
    visited_q_pairs = set()  # First-visit tracking for Q-values

    for s, a, s_prime, r in reversed(episode):  # Process in reverse order
        G = r + G  # Accumulate reward
        if (s, a) not in visited_q_pairs:
            Q_values[(s, a)] += G  # Store observed returns
            visited_q_pairs.add((s, a))  # Prevent duplicate updates for first-visit MC

# Compute final Q-values as the average observed returns
Q_direct = {key: np.mean(values) if values else 0 for key, values in Q_values.items()}

# Print the results for the requested Q-values
print("\n=== Q-values from Direct Evaluation ===")
print(f"Q((2,4), W) = {Q_direct.get(((2,4), 'W'), 0):.4f}")
print(f"Q((3,3), S) = {Q_direct.get(((3,3), 'S'), 0):.4f}")

# Q-values initialization (for Question 2)
Q_values = defaultdict(float)

# Q-learning iterations
for iteration in range(2):
    print(f"\n=== Run {iteration + 1} ===")
    for episode in training_episodes:
        print(f"\nEpisode:")
        for s, a, s_prime, r in episode:
            old_q_value = Q_values[(s, a)]

            # Determine max Q-value for next state
            if s_prime == "Done":
                max_Q_s_prime = 0
            else:
                possible_actions = ["N", "S", "E", "W", "Exit"]
                available_q = [Q_values[(s_prime, act)] for act in possible_actions if (s_prime, act) in Q_values]
                max_Q_s_prime = max(available_q, default=0)

            # Q-learning update rule
            term_sample = alpha * (r + gamma * max_Q_s_prime)
            term_state = (1-alpha) * old_q_value
            q_term = Q_values[(s, a)] 
            Q_values[(s, a)] = term_sample + term_state
            print( f"  Q({s}, {a}): Old={old_q_value:.1f}, Reward={r}, Next Q={q_term}, Next={s_prime}, Updated Q={Q_values[(s, a)]:.1f}")
    
    # Print all final Q-values
    print("\nFinal Q-values:")
    for (s, a), q in sorted(Q_values.items()):
        print(f"Q({s}, {a}) = {q:.2f}")

# max_Q_s_prime, q_term, term_sample,term_state,
# After two runs, count non-zero Q-values
non_zero_q_values = sum(1 for q in Q_values.values() if q != 0)
print("\nNon-zero Q-values after two runs:", non_zero_q_values)