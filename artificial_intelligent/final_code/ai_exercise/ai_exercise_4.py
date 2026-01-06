import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Dataset
data = np.array([
    [1.0, 0.75, 1.0, -1],
    [1.0, 1.0, 0.5, 0],
    [1.0, 0.0, 0.0, 1],
    [1.0, 0.25, 0.5, 1],
    [1.0, 1.0, 1.0, -1],
    [1.0, 0.75, 0.0, 0]
])

# Initial weights (changed to float)
weights = {
    -1: np.array([0.0, 0.0, 0.0]),
    0: np.array([1.0, 0.0, 0.0]),
    1: np.array([0.0, 0.0, 0.0])
}

# Modified Perceptron update function with debug prints
def perceptron_update(weights, x, true_label):
    print(f"\nInput Vector: {x}, True Label: {true_label}")

    # Calculate scores for each class
    scores = {label: np.dot(weights[label], x) for label in weights}
    predicted_label = max(scores, key=scores.get)

    print(f"Scores: {scores}")
    print(f"Predicted Label: {predicted_label}, True Label: {true_label}")

    # Check if update is needed
    if predicted_label != true_label:
        print(f"Updating Weights:")
        print(f"  - Adding {x} to class {true_label}")
        print(f"  - Subtracting {x} from class {predicted_label}")

        weights[true_label] += x
        weights[predicted_label] -= x

        # Display updated weights
        print(f"Updated Weights for Class {true_label}: {weights[true_label]}")
        print(f"Updated Weights for Class {predicted_label}: {weights[predicted_label]}")
    else:
        print("No update needed. Prediction is correct.")

    return weights

# Apply updates for the first two data examples
weights_after_first = perceptron_update(weights.copy(), data[0, :3], data[0, 3])
weights_after_second = perceptron_update(weights_after_first.copy(), data[1, :3], data[1, 3])

# Display the weight updates in a table
table_data = {
    "Weights for Class -1": [weights[-1], weights_after_first[-1], weights_after_second[-1]],
    "Weights for Class 0": [weights[0], weights_after_first[0], weights_after_second[0]],
    "Weights for Class +1": [weights[1], weights_after_first[1], weights_after_second[1]],
}

df = pd.DataFrame(table_data, index=["Initial Weights", "After First Example", "After Second Example"])
print("\nWeight Updates Table:")
print(df)

# Visualization
fig, ax = plt.subplots()

# Plot data points
for label, color, marker in zip([-1, 0, 1], ['red', 'blue', 'green'], ['o', 's', '^']):
    subset = data[data[:, 3] == label]
    ax.scatter(subset[:, 1], subset[:, 2], c=color, label=f'Class {label}', marker=marker)

ax.set_xlabel('Turbidity (t)')
ax.set_ylabel('Microbe Content (m)')
ax.set_title('Water Quality Dataset Visualization')
ax.legend()

# Perceptron Prediction for (1.0, 0.5, 0.25)
x_new = np.array([1.0, 0.5, 0.25])
learned_weights = {
    -1: np.array([1.0, 1.0, -1.0]),
    0: np.array([1.0, 2.0, -2.0]),
    1: np.array([-1.0, -1.0, 1.0])
}

# Prediction calculation
predictions = {label: np.dot(w, x_new) for label, w in learned_weights.items()}
predicted_class = max(predictions, key=predictions.get)

# Return predicted class
print(f"\nPredicted Class for New Input {x_new}: {predicted_class}")