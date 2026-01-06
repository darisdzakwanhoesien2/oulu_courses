# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        best_weights = None
        best_accuracy = 0
        best_C = None

        # Iterate over each C value in the grid
        for C in Cgrid:
            # Initialize weights for each C value
            weights = {label: util.Counter() for label in self.legalLabels}

            # Train for multiple iterations
            for iteration in range(self.max_iterations):
                print(f"Training with C={C}, Iteration {iteration}")
                for i in range(len(trainingData)):
                    datum = trainingData[i]
                    true_label = trainingLabels[i]

                    # Predict the label with highest score
                    scores = {label: weights[label] * datum for label in self.legalLabels}
                    predicted_label = max(scores, key=scores.get)

                    if predicted_label != true_label:
                        # Compute τ (step size)
                        tau = min(
                            C,
                            (scores[predicted_label] - scores[true_label] + 1.0) / (2 * (datum * datum))
                        )

                        # Update the weight vectors
                        feature_update = datum.copy()
                        for key in feature_update:
                            feature_update[key] *= tau

                        weights[true_label] += feature_update
                        weights[predicted_label] -= feature_update

            # Validate the model on validation data
            self.weights = weights
            predictions = self.classify(validationData)
            accuracy = sum(int(predictions[i] == validationLabels[i]) for i in range(len(validationLabels))) / len(validationLabels)

            # Store best weights based on accuracy
            if accuracy > best_accuracy or (accuracy == best_accuracy and C < best_C):
                best_accuracy = accuracy
                best_C = C
                best_weights = weights.copy()

        # Set the best found weights
        self.weights = best_weights
        print(f"Best C: {best_C} with accuracy: {best_accuracy}")

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


