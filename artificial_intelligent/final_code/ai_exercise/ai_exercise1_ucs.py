import matplotlib.pyplot as plt
import numpy as np

# Define the grid and the problem ()
grid = [
    [' ', ' ', ' ', ' ',' ', ' ', 'X', ' '],
    [' ', ' ', ' ', 'X',' ', ' ', ' ', ' '],
    [' ', ' ', 'X', ' ', 'X',' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'X',' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'X',' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'X',' ', ' ', ' '],
    [' ', ' ', 'X', ' ', 'X',' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']
]

start = (3, 2)
goal = (2, 5)
directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

def plot_grid(path, visited, step_numbers):
    """Visualize the grid with the path, visited nodes, and step numbers."""
    fig, ax = plt.subplots()
    nrows, ncols = len(grid), len(grid[0])
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.invert_yaxis()

    # Draw the grid
    for row in range(nrows):
        for col in range(ncols):
            if grid[row][col] == 'X':
                ax.add_patch(plt.Rectangle((col, row), 1, 1, color="black"))
            else:
                ax.add_patch(plt.Rectangle((col, row), 1, 1, edgecolor="gray", facecolor="white"))

    # Mark the visited nodes
    for vr, vc in visited:
        ax.add_patch(plt.Circle((vc + 0.5, vr + 0.5), 0.2, color="blue", alpha=0.5))

    # Mark the path and add step numbers
    for i, (pr, pc) in enumerate(path):
        ax.add_patch(plt.Circle((pc + 0.5, pr + 0.5), 0.3, color="green"))
        ax.text(pc + 0.5, pr + 0.5, str(step_numbers[i]), color="white", ha="center", va="center", fontsize=8)

    # Highlight start and goal
    ax.add_patch(plt.Circle((start[1] + 0.5, start[0] + 0.5), 0.3, color="yellow"))
    ax.add_patch(plt.Circle((goal[1] + 0.5, goal[0] + 0.5), 0.3, color="red"))

    ax.set_aspect('equal')
    plt.xticks(np.arange(ncols), [])
    plt.yticks(np.arange(nrows), [])
    plt.show()

import heapq

def uniform_cost_search_visual(problem):
    """Visualize UCS with step-by-step updates."""
    # 1. Initialization
    priority_queue = []
    heapq.heappush(priority_queue, (0, problem['start'], []))
    visited = {}
    step_count = 0

    # 2. Search Loop
    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)

        if state in visited and visited[state] <= cost:
            continue

        # Node is further explored and checked
        visited[state] = cost
        path = path + [state]
        step_numbers = list(range(len(path)))

        # Visualize current step
        print(f"Step {step_count}: Exploring {state} with cost {cost}")
        plot_grid(path, visited, step_numbers)
        step_count += 1

        # The path will be return once the goal is reach
        if state == problem['goal']:
            print("Goal reached!")
            return path

        # Iteration 
        r, c = state
        for action, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != 'X':
                heapq.heappush(priority_queue, (cost + 1, (nr, nc), path))

    print("No solution found.")
    return None

# Define the problem as a dictionary
problem = {
    'start': start,
    'goal': goal,
    'grid': grid
}

# Run and visualize UCS
ucs_path = uniform_cost_search_visual(problem)