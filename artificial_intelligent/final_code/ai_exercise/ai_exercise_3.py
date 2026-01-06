from itertools import permutations

# Variables
variables = ['F', 'O', 'U', 'R', 'I', 'V', 'E', 'N']

# Constraints
# R is fixed to 0
fixed_values = {'R': 0}

# Domains
domain = {var: list(range(10)) for var in variables}
domain['R'] = [0]  # R is fixed to 0
domain['N'] = [1, 2, 4, 5, 6, 7, 8, 9]  # N ≠ 3
domain['F'] = list(range(1, 10))  # F ≠ 0

# Helper function to evaluate the equation
def is_valid(assignment):
    try:
        F = assignment['F']
        O = assignment['O']
        U = assignment['U']
        R = assignment['R']
        I = assignment['I']
        V = assignment['V']
        E = assignment['E']
        N = assignment['N']

        FOUR = 1000 * F + 100 * O + 10 * U + R
        FIVE = 1000 * F + 100 * I + 10 * V + E
        NINE = 1000 * N + 100 * I + 10 * N + E

        return FOUR + FIVE == NINE
    except KeyError:
        return False

# Backtracking search to find all solutions
def backtrack_all(assignment, solutions):
    if len(assignment) == len(variables):
        if is_valid(assignment):
            solutions.append(assignment.copy())
        return

    # Choose the next variable to assign
    unassigned = [v for v in variables if v not in assignment]
    mrv_var = min(unassigned, key=lambda var: len(domain[var]))

    for value in domain[mrv_var]:
        if value in assignment.values():  # All-different constraint
            continue

        assignment[mrv_var] = value
        backtrack_all(assignment, solutions)
        del assignment[mrv_var]  # Backtrack

# Solve the problem
solutions = []
backtrack_all(fixed_values.copy(), solutions)

# Display the solutions
results = []
for solution in solutions:
    FOUR = 1000 * solution['F'] + 100 * solution['O'] + 10 * solution['U'] + solution['R']
    FIVE = 1000 * solution['F'] + 100 * solution['I'] + 10 * solution['V'] + solution['E']
    NINE = 1000 * solution['N'] + 100 * solution['I'] + 10 * solution['N'] + solution['E']

    results.append({
        "FOUR": FOUR,
        "FIVE": FIVE,
        "NINE": NINE,
        "Assignment": solution
    })