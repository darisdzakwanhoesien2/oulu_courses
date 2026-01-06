import numpy as np

# Define states
states = ["A", "B", "C", "D", "E", "F"]
num_states = len(states)

# Define actions and transitions
actions = {
    "A": ["a1", "a2"],
    "B": ["b1", "b2"],
    "C": ["c1", "c2"],
    "D": ["d1", "d2"],
    "E": ["e1"],  # Only one action
    "F": []  # Terminal state
}

# Define transition probabilities P(s' | s, a)
P = {
    ("A", "a1"): {"B": 0.3, "C": 0.5, "A": 0.2},
    ("A", "a2"): {"D": 0.2, "E": 0.8},
    ("B", "b1"): {"A": 0.2, "E": 0.8},
    ("B", "b2"): {"C": 0.3, "B": 0.7},
    ("C", "c1"): {"D": 0.6, "F": 0.4},
    ("C", "c2"): {"F": 0.8, "E": 0.1, "B": 0.1},
    ("D", "d2"): {"A": 0.6, "F": 0.4},
    ("D", "d1"): {"C": 1.0},
    ("E", "e1"): {"F": 0.2, "A": 0.8}  
}

# Define reward function R(s)
R = {
    "A": -3,
    "B": -2,
    "C": -2,
    "D": -1,
    "E": -1,
    "F": 10  # Terminal state
}

# Discount factor
gamma = 0.9

# Step 1: Convert states into indices
state_index = {state: i for i, state in enumerate(states)}

# Step 2: Initialize the transition matrix dynamically
P_matrix = np.zeros((num_states, num_states))  # Transition matrix

# Define a fixed policy for each state (choosing one action per state)
policy = {
    "A": "a1",
    "B": "b1",
    "C": "c1",
    "D": "d1",
    "E": "e1",
    "F": None  # Terminal state
}

# Fill in the transition matrix based on the selected policy
for s, a in policy.items():
    if a is None:  # Skip terminal states
        continue
    s_idx = state_index[s]
    for s_prime, prob in P[(s, a)].items():
        s_prime_idx = state_index[s_prime]
        P_matrix[s_idx, s_prime_idx] = prob

# Step 3: Create reward vector
R_vector = np.array([R[s] for s in states])

# Step 4: Solve the system of equations for utilities
I = np.eye(num_states)  # Identity matrix
A = I - gamma * P_matrix  # (I - gamma * P) matrix

## Question 1: linear system of equations: utilities for all states under this policy
print("P", P_matrix)
# print('Reward Matrix', R_vector)
print('A', A)


# Question 2: computed utilities
U = np.linalg.solve(A, R_vector)  # Solve for U
print("State Utilities:", U)

# Step 5: Policy Improvement - Update the policy based on computed utilities
updated_policy = {}

print("\n### Policy Improvement Process ###\n")

for s in states:
    if s == "F":  # Skip terminal state
        updated_policy[s] = None
        print(f"State {s} is a terminal state. No action needed.")
        continue

    print(f"Evaluating best action for State {s}:")
    best_action = None
    best_value = float('-inf')

    for a in actions[s]:  # Loop through all available actions
        expected_value = sum(
            P[(s, a)][s_prime] * (R[s] + gamma * U[state_index[s_prime]]) 
            for s_prime in P[(s, a)]
        )

        # Print the step-by-step computation
        print(f"  Action {a}:")
        for s_prime in P[(s, a)]:
            transition_prob = P[(s, a)][s_prime]
            reward = R[s]
            future_utility = gamma * U[state_index[s_prime]]
            contribution = transition_prob * (reward + future_utility)
            print(f"    - Transition to {s_prime} (P={transition_prob}): "
                  f"({reward} + {gamma}*{U[state_index[s_prime]]}) * {transition_prob} = {contribution:.4f}")

        print(f"    => Expected Utility for {a}: {expected_value:.4f}")

        # Select the action with the highest expected utility
        if expected_value > best_value:
            best_value = expected_value
            best_action = a

    updated_policy[s] = best_action  # Store the best action
    print(f"  => Best action for State {s}: {best_action}\n")

# Print the improved policy
print("\n### Updated Policy ###")
for state, action in updated_policy.items():
    print(f"State {state}: Best Action -> {action}")

