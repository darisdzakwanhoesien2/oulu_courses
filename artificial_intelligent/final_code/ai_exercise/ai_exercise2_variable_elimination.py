import pandas as pd

# Define the probability tables as Pandas DataFrames
P_S = pd.DataFrame({'S': ['+s', '-s'], 'P(S)': [0.1, 0.9]})
P_W = pd.DataFrame({'W': ['+w', '-w'], 'P(W)': [0.6, 0.4]})
P_SC_A = pd.DataFrame({
    'S': ['+s', '+s', '+s', '+s', '-s', '-s', '-s', '-s'],
    'C': ['+c', '+c', '-c', '-c', '+c', '+c', '-c', '-c'],
    'A': ['+a', '-a', '+a', '-a', '+a', '-a', '+a', '-a'],
    'P(A|S,C)': [0.90, 0.10, 0.30, 0.70, 0.80, 0.02, 0.20, 0.98]
})
P_C_W = pd.DataFrame({
    'W': ['+w', '+w', '-w', '-w'],
    'C': ['+c', '-c', '+c', '-c'],
    'P(C|W)': [0.8, 0.2, 0.3, 0.7]
})

# Step 1: Join P(C|W) and P(W) on W
joint_CW_W = pd.merge(P_C_W, P_W, on='W')
joint_CW_W['P(W,C)'] = joint_CW_W['P(C|W)'] * joint_CW_W['P(W)']

# Step 2: Marginalize over W to get P(C)
P_C = joint_CW_W.groupby('C').agg({'P(W,C)': 'sum'}).reset_index()
P_C.rename(columns={'P(W,C)': 'P(C)'}, inplace=True)

# Step 3: Join P(C) and P(A|S,C) on C
joint_AC_SC = pd.merge(P_SC_A, P_C, on='C')
joint_AC_SC['P(A,S,C)'] = joint_AC_SC['P(A|S,C)'] * joint_AC_SC['P(C)']

# Step 4: Marginalize over C to get P(A, S)
P_AS = joint_AC_SC.groupby(['A', 'S']).agg({'P(A,S,C)': 'sum'}).reset_index()
P_AS.rename(columns={'P(A,S,C)': 'P(A,S)'}, inplace=True)

# Step 5: Marginalize over A to normalize P(A | +S)
P_A_given_S = P_AS[P_AS['S'] == '+s']
P_A_given_S['P(A|+S)'] = P_A_given_S['P(A,S)'] / P_A_given_S['P(A,S)'].sum()

# Final Output: Probability of A given +S
print(P_A_given_S[['A', 'P(A|+S)']])