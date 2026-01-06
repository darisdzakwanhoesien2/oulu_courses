# dataClassifier.py
# -----------------
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


# This file contains feature extraction methods and harness
# code for data classification

import mostFrequent
import naiveBayes
import perceptron
import perceptron_pacman
import mira
import samples
import sys
import util
from pacman import GameState

TEST_SET_SIZE = 100
DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28
FACE_DATUM_WIDTH=60
FACE_DATUM_HEIGHT=70


def basicFeatureExtractorDigit(datum):
    """
    Returns a set of pixel features indicating whether
    each pixel in the provided datum is white (1) or gray/black (0)
    """
    a = datum.getPixels()

    features = util.Counter()
    for x in range(DIGIT_DATUM_WIDTH):
        for y in range(DIGIT_DATUM_HEIGHT):
            if datum.getPixel(x, y) > 0:
                features[(x,y)] = 1
            else:
                features[(x,y)] = 0
    return features

def basicFeatureExtractorFace(datum):
    """
    Returns a set of pixel features indicating whether
    each pixel in the provided datum is an edge (1) or no edge (0)
    """
    a = datum.getPixels()

    features = util.Counter()
    for x in range(FACE_DATUM_WIDTH):
        for y in range(FACE_DATUM_HEIGHT):
            if datum.getPixel(x, y) > 0:
                features[(x,y)] = 1
            else:
                features[(x,y)] = 0
    return features

def enhancedFeatureExtractorDigit(datum):
    """
    Your feature extraction playground.

    You should return a util.Counter() of features
    for this datum (datum is of type samples.Datum).

    ## DESCRIBE YOUR ENHANCED FEATURES HERE...

    ##
    """
    features = basicFeatureExtractorDigit(datum) # Start with basic pixel features

    # Example features which is always 0 and 1
    #features["zeroExample"] = 0
    #features["oneExample"] = 1

    "*** YOUR CODE HERE ***"
    """
    Extracts advanced features to improve digit classification.
    Your enhanced feature extractor. We add:
      - Black region counting (DFS)
      - Loops in white space (BFS)
      - Horizontal and vertical symmetry (binned)
      - Quadrant density (binned)

    All features are stored as binary indicators (0/1).
    """
    width, height = DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT

    # Convert image to a 2D boolean array: True = black pixel, False = white pixel
    image = [[(datum.getPixel(x, y) > 0) for x in range(width)] for y in range(height)]

    #--------------------------------------------------------------------------
    # 2) Count Black Regions (DFS)
    #--------------------------------------------------------------------------
    def count_black_regions(img):
        visited = set()
        regions = 0

        def dfs(sx, sy):
            stack = [(sx, sy)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                # Explore neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if img[ny][nx] and (nx, ny) not in visited:
                            stack.append((nx, ny))

        for row in range(height):
            for col in range(width):
                if img[row][col] and (col, row) not in visited:
                    regions += 1
                    dfs(col, row)

        return regions

    num_black_regions = count_black_regions(image)
    # Binning black region counts (0, 1, 2+)
    features["black_regions_0"] = 1 if num_black_regions == 0 else 0
    features["black_regions_1"] = 1 if num_black_regions == 1 else 0
    features["black_regions_2+"] = 1 if num_black_regions >= 2 else 0

    #--------------------------------------------------------------------------
    # 3) Count Loops in White Space (BFS)
    #--------------------------------------------------------------------------
    def count_white_loops(img):
        visited = set()
        loops = 0

        def bfs(sx, sy):
            queue = [(sx, sy)]
            inside = True
            while queue:
                cx, cy = queue.pop(0)
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                # Check neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    # If we go out of bounds, it means the white region touches the edge
                    if not (0 <= nx < width and 0 <= ny < height):
                        inside = False
                    else:
                        # If it's still white and not visited
                        if not img[ny][nx] and (nx, ny) not in visited:
                            queue.append((nx, ny))
            return inside

        for row in range(height):
            for col in range(width):
                # If it's white and not visited, do BFS
                if not img[row][col] and (col, row) not in visited:
                    if bfs(col, row):
                        loops += 1
        return loops

    num_loops = count_white_loops(image)
    # Binning loops (0, 1, 2+)
    features["loops_0"] = 1 if num_loops == 0 else 0
    features["loops_1"] = 1 if num_loops == 1 else 0
    features["loops_2+"] = 1 if num_loops >= 2 else 0

    #--------------------------------------------------------------------------
    # 4) Symmetry (Horizontal & Vertical)
    #--------------------------------------------------------------------------
    # We'll count how many pixels match their opposite side.
    # Then convert that match count to a fraction of total possible matches,
    # and bin the fraction.

    def check_symmetry(img):
        # horizontal_sym: compare row y with row (height-y-1)
        horizontal_matches = 0
        total_pairs_h = 0
        for y in range(height // 2):
            for x in range(width):
                total_pairs_h += 1
                if img[y][x] == img[height - 1 - y][x]:
                    horizontal_matches += 1

        # vertical_sym: compare col x with col (width-x-1)
        vertical_matches = 0
        total_pairs_v = 0
        for y in range(height):
            for x in range(width // 2):
                total_pairs_v += 1
                if img[y][x] == img[y][width - 1 - x]:
                    vertical_matches += 1

        # Fraction of matched pixels
        h_frac = float(horizontal_matches) / total_pairs_h if total_pairs_h > 0 else 0
        v_frac = float(vertical_matches) / total_pairs_v if total_pairs_v > 0 else 0
        return h_frac, v_frac

    h_sym_frac, v_sym_frac = check_symmetry(image)

    # Example binning for horizontal symmetry (low, medium, high)
    features["hSym_low"] = 1 if h_sym_frac < 0.3 else 0
    features["hSym_med"] = 1 if 0.3 <= h_sym_frac < 0.7 else 0
    features["hSym_high"] = 1 if h_sym_frac >= 0.7 else 0

    # Example binning for vertical symmetry
    features["vSym_low"] = 1 if v_sym_frac < 0.3 else 0
    features["vSym_med"] = 1 if 0.3 <= v_sym_frac < 0.7 else 0
    features["vSym_high"] = 1 if v_sym_frac >= 0.7 else 0

    #--------------------------------------------------------------------------
    # 5) Quadrant Density (Binned)
    #--------------------------------------------------------------------------
    half_w = width // 2
    half_h = height // 2

    top_left = sum(image[r][c] for r in range(0, half_h) for c in range(0, half_w))
    top_right = sum(image[r][c] for r in range(0, half_h) for c in range(half_w, width))
    bottom_left = sum(image[r][c] for r in range(half_h, height) for c in range(0, half_w))
    bottom_right = sum(image[r][c] for r in range(half_h, height) for c in range(half_w, width))

    # We'll convert each count to a fraction of its quadrant area
    quad_area = half_w * half_h  # area of each quadrant
    tl_frac = float(top_left) / quad_area if quad_area > 0 else 0
    tr_frac = float(top_right) / quad_area if quad_area > 0 else 0
    bl_frac = float(bottom_left) / quad_area if quad_area > 0 else 0
    br_frac = float(bottom_right) / quad_area if quad_area > 0 else 0

    # Example 3-bin approach for each quadrant
    def bin_quadrant_density(fraction, prefix):
        features[prefix+"_low"] = 1 if fraction < 0.3 else 0
        features[prefix+"_med"] = 1 if 0.3 <= fraction < 0.6 else 0
        features[prefix+"_high"] = 1 if fraction >= 0.6 else 0

    bin_quadrant_density(tl_frac, "Q_tl")
    bin_quadrant_density(tr_frac, "Q_tr")
    bin_quadrant_density(bl_frac, "Q_bl")
    bin_quadrant_density(br_frac, "Q_br")

    return features

def basicFeatureExtractorPacman(state):
    """
    A basic feature extraction function.

    You should return a util.Counter() of features
    for each (state, action) pair along with a list of the legal actions

    ##
    """
    features = util.Counter()
    for action in state.getLegalActions():
        successor = state.generateSuccessor(0, action)
        foodCount = successor.getFood().count()
        featureCounter = util.Counter()
        featureCounter['foodCount'] = foodCount
        features[action] = featureCounter
    return features, state.getLegalActions()

def enhancedFeatureExtractorPacman(state):
    """
    Your feature extraction playground.

    You should return a util.Counter() of features
    for each (state, action) pair along with a list of the legal actions

    ##
    """

    features = basicFeatureExtractorPacman(state)[0]
    for action in state.getLegalActions():
        features[action] = util.Counter(features[action], **enhancedPacmanFeatures(state, action))
    return features, state.getLegalActions()

def enhancedPacmanFeatures(state, action):
    """
    For each state, this function is called with each legal action.
    It should return a counter with { <feature name> : <feature value>, ... }
    """
    features = util.Counter()

    # Example to get the successor state like in the first project
    #successor = state.generateSuccessor(0, action)

    "*** YOUR CODE HERE ***"
    """
    Extracts strategic features for better decision-making in Pacman.
    """
    features = util.Counter()
    successor = state.generateSuccessor(0, action)
    pacman_pos = successor.getPacmanPosition()
    food = successor.getFood()
    ghosts = successor.getGhostPositions()
    capsules = successor.getCapsules()
    walls = successor.getWalls()

    # 1. Distance to the Closest Food
    def closest_food(pacman_pos, food, walls):
        from util import manhattanDistance, Queue

        queue = Queue()
        queue.push((pacman_pos, 0))
        visited = set()

        while not queue.isEmpty():
            position, dist = queue.pop()
            if position in visited:
                continue
            visited.add(position)

            x, y = position
            if food[x][y]:  # If food is found
                return dist

            # Explore neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (x + dx, y + dy)
                if not walls[next_pos[0]][next_pos[1]]:  # If not a wall
                    queue.push((next_pos, dist + 1))

        return 0  # No food found

    features["closest_food"] = closest_food(pacman_pos, food, walls)

    # 2. Distance to the Closest Ghost
    def closest_ghost(pacman_pos, ghosts):
        if not ghosts:
            return 0
        return min(util.manhattanDistance(pacman_pos, ghost) for ghost in ghosts)

    features["closest_ghost"] = closest_ghost(pacman_pos, ghosts)

    # 3. Number of Remaining Capsules
    features["capsule_count"] = len(capsules)

    # 4. Number of Scared Ghosts
    scared_ghosts = sum(1 for ghost_state in successor.getGhostStates() if ghost_state.scaredTimer > 0)
    features["scared_ghosts"] = scared_ghosts

    # 5. Wall Proximity (number of walls near Pacman)
    def wall_proximity(pacman_pos, walls):
        x, y = pacman_pos
        return sum(walls[x + dx][y + dy] for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)])

    features["wall_proximity"] = wall_proximity(pacman_pos, walls)

    # Normalize food distance to avoid high numbers
    if features["closest_food"] > 0:
        features["closest_food"] = 1.0 / features["closest_food"]

    # Normalize ghost distance (penalize being close to ghosts)
    if features["closest_ghost"] > 0:
        features["closest_ghost"] = -1.0 / features["closest_ghost"]

    return features

def contestFeatureExtractorDigit(datum):
    """
    Specify features to use for the minicontest
    """
    features =  basicFeatureExtractorDigit(datum)
    return features

def enhancedFeatureExtractorFace(datum):
    """
    Your feature extraction playground for faces.
    It is your choice to modify this.
    """
    features =  basicFeatureExtractorFace(datum)
    return features

def analysis(classifier, guesses, testLabels, testData, rawTestData, printImage):
    """
    This function is called after learning.
    Include any code that you want here to help you analyze your results.

    Use the printImage(<list of pixels>) function to visualize features.

    An example of use has been given to you.

    - classifier is the trained classifier
    - guesses is the list of labels predicted by your classifier on the test set
    - testLabels is the list of true labels
    - testData is the list of training datapoints (as util.Counter of features)
    - rawTestData is the list of training datapoints (as samples.Datum)
    - printImage is a method to visualize the features
    (see its use in the odds ratio part in runClassifier method)

    This code won't be evaluated. It is for your own optional use
    (and you can modify the signature if you want).
    """

    # Put any code here...
    # Example of use:
    # for i in range(len(guesses)):
    #     prediction = guesses[i]
    #     truth = testLabels[i]
    #     if (prediction != truth):
    #         print("===================================")
    #         print("Mistake on example %d" % i)
    #         print("Predicted %d; truth is %d" % (prediction, truth))
    #         print("Image: ")
    #         print(rawTestData[i])
    #         break


## =====================
## You don't have to modify any code below.
## =====================


class ImagePrinter:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def printImage(self, pixels):
        """
        Prints a Datum object that contains all pixels in the
        provided list of pixels.  This will serve as a helper function
        to the analysis function you write.

        Pixels should take the form
        [(2,2), (2, 3), ...]
        where each tuple represents a pixel.
        """
        image = samples.Datum(None,self.width,self.height)
        for pix in pixels:
            try:
            # This is so that new features that you could define which
            # which are not of the form of (x,y) will not break
            # this image printer...
                x,y = pix
                image.pixels[x][y] = 2
            except:
                print("new features:", pix)
                continue
        print(image)

def default(str):
    return str + ' [Default: %default]'

USAGE_STRING = """
  USAGE:      python dataClassifier.py <options>
  EXAMPLES:   (1) python dataClassifier.py
                  - trains the default mostFrequent classifier on the digit dataset
                  using the default 100 training examples and
                  then test the classifier on test data
              (2) python dataClassifier.py -c naiveBayes -d digits -t 1000 -f -o -1 3 -2 6 -k 2.5
                  - would run the naive Bayes classifier on 1000 training examples
                  using the enhancedFeatureExtractorDigits function to get the features
                  on the faces dataset, would use the smoothing parameter equals to 2.5, would
                  test the classifier on the test data and performs an odd ratio analysis
                  with label1=3 vs. label2=6
                 """


def readCommand( argv ):
    "Processes the command used to run from the command line."
    from optparse import OptionParser
    parser = OptionParser(USAGE_STRING)

    parser.add_option('-c', '--classifier', help=default('The type of classifier'), choices=['mostFrequent', 'nb', 'naiveBayes', 'perceptron', 'mira', 'minicontest'], default='mostFrequent')
    parser.add_option('-d', '--data', help=default('Dataset to use'), choices=['digits', 'faces', 'pacman'], default='digits')
    parser.add_option('-t', '--training', help=default('The size of the training set'), default=100, type="int")
    parser.add_option('-f', '--features', help=default('Whether to use enhanced features'), default=False, action="store_true")
    parser.add_option('-o', '--odds', help=default('Whether to compute odds ratios'), default=False, action="store_true")
    parser.add_option('-1', '--label1', help=default("First label in an odds ratio comparison"), default=0, type="int")
    parser.add_option('-2', '--label2', help=default("Second label in an odds ratio comparison"), default=1, type="int")
    parser.add_option('-w', '--weights', help=default('Whether to print weights'), default=False, action="store_true")
    parser.add_option('-k', '--smoothing', help=default("Smoothing parameter (ignored when using --autotune)"), type="float", default=2.0)
    parser.add_option('-a', '--autotune', help=default("Whether to automatically tune hyperparameters"), default=False, action="store_true")
    parser.add_option('-i', '--iterations', help=default("Maximum iterations to run training"), default=3, type="int")
    parser.add_option('-s', '--test', help=default("Amount of test data to use"), default=TEST_SET_SIZE, type="int")
    parser.add_option('-g', '--agentToClone', help=default("Pacman agent to copy"), default=None, type="str")

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0: raise Exception('Command line input not understood: ' + str(otherjunk))
    args = {}

    # Set up variables according to the command line input.
    print("Doing classification")
    print("--------------------")
    print("data:\t\t" + options.data)
    print("classifier:\t\t" + options.classifier)
    if not options.classifier == 'minicontest':
        print("using enhanced features?:\t" + str(options.features))
    else:
        print("using minicontest feature extractor")
    print("training set size:\t" + str(options.training))
    if(options.data=="digits"):
        printImage = ImagePrinter(DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT).printImage
        if (options.features):
            featureFunction = enhancedFeatureExtractorDigit
        else:
            featureFunction = basicFeatureExtractorDigit
        if (options.classifier == 'minicontest'):
            featureFunction = contestFeatureExtractorDigit
    elif(options.data=="faces"):
        printImage = ImagePrinter(FACE_DATUM_WIDTH, FACE_DATUM_HEIGHT).printImage
        if (options.features):
            featureFunction = enhancedFeatureExtractorFace
        else:
            featureFunction = basicFeatureExtractorFace
    elif(options.data=="pacman"):
        printImage = None
        if (options.features):
            featureFunction = enhancedFeatureExtractorPacman
        else:
            featureFunction = basicFeatureExtractorPacman
    else:
        print("Unknown dataset", options.data)
        print(USAGE_STRING)
        sys.exit(2)

    if(options.data=="digits"):
        legalLabels = range(10)
    else:
        legalLabels = ['Stop', 'West', 'East', 'North', 'South']

    if options.training <= 0:
        print("Training set size should be a positive integer (you provided: %d)" % options.training)
        print(USAGE_STRING)
        sys.exit(2)

    if options.smoothing <= 0:
        print("Please provide a positive number for smoothing (you provided: %f)" % options.smoothing)
        print(USAGE_STRING)
        sys.exit(2)

    if options.odds:
        if options.label1 not in legalLabels or options.label2 not in legalLabels:
            print("Didn't provide a legal labels for the odds ratio: (%d,%d)" % (options.label1, options.label2))
            print(USAGE_STRING)
            sys.exit(2)

    if(options.classifier == "mostFrequent"):
        classifier = mostFrequent.MostFrequentClassifier(legalLabels)
    elif(options.classifier == "naiveBayes" or options.classifier == "nb"):
        classifier = naiveBayes.NaiveBayesClassifier(legalLabels)
        classifier.setSmoothing(options.smoothing)
        if (options.autotune):
            print("using automatic tuning for naivebayes")
            classifier.automaticTuning = True
        else:
            print("using smoothing parameter k=%f for naivebayes" %  options.smoothing)
    elif(options.classifier == "perceptron"):
        if options.data != 'pacman':
            classifier = perceptron.PerceptronClassifier(legalLabels,options.iterations)
        else:
            classifier = perceptron_pacman.PerceptronClassifierPacman(legalLabels,options.iterations)
    elif(options.classifier == "mira"):
        if options.data != 'pacman':
            classifier = mira.MiraClassifier(legalLabels, options.iterations)
        if (options.autotune):
            print("using automatic tuning for MIRA")
            classifier.automaticTuning = True
        else:
            print("using default C=0.001 for MIRA")
    elif(options.classifier == 'minicontest'):
        import minicontest
        classifier = minicontest.contestClassifier(legalLabels)
    else:
        print("Unknown classifier:", options.classifier)
        print(USAGE_STRING)

        sys.exit(2)

    args['agentToClone'] = options.agentToClone

    args['classifier'] = classifier
    args['featureFunction'] = featureFunction
    args['printImage'] = printImage

    return args, options

# Dictionary containing full path to .pkl file that contains the agent's training, validation, and testing data.
MAP_AGENT_TO_PATH_OF_SAVED_GAMES = {
    'FoodAgent': ('pacmandata/food_training.pkl','pacmandata/food_validation.pkl','pacmandata/food_test.pkl' ),
    'StopAgent': ('pacmandata/stop_training.pkl','pacmandata/stop_validation.pkl','pacmandata/stop_test.pkl' ),
    'SuicideAgent': ('pacmandata/suicide_training.pkl','pacmandata/suicide_validation.pkl','pacmandata/suicide_test.pkl' ),
    'GoodReflexAgent': ('pacmandata/good_reflex_training.pkl','pacmandata/good_reflex_validation.pkl','pacmandata/good_reflex_test.pkl' ),
    'ContestAgent': ('pacmandata/contest_training.pkl','pacmandata/contest_validation.pkl', 'pacmandata/contest_test.pkl' )
}
# Main harness code



def runClassifier(args, options):
    featureFunction = args['featureFunction']
    classifier = args['classifier']
    printImage = args['printImage']
    
    # Load data
    numTraining = options.training
    numTest = options.test

    if(options.data=="pacman"):
        agentToClone = args.get('agentToClone', None)
        trainingData, validationData, testData = MAP_AGENT_TO_PATH_OF_SAVED_GAMES.get(agentToClone, (None, None, None))
        trainingData = trainingData or args.get('trainingData', False) or MAP_AGENT_TO_PATH_OF_SAVED_GAMES['ContestAgent'][0]
        validationData = validationData or args.get('validationData', False) or MAP_AGENT_TO_PATH_OF_SAVED_GAMES['ContestAgent'][1]
        testData = testData or MAP_AGENT_TO_PATH_OF_SAVED_GAMES['ContestAgent'][2]
        rawTrainingData, trainingLabels = samples.loadPacmanData(trainingData, numTraining)
        rawValidationData, validationLabels = samples.loadPacmanData(validationData, numTest)
        rawTestData, testLabels = samples.loadPacmanData(testData, numTest)
    else:
        rawTrainingData = samples.loadDataFile("digitdata/trainingimages", numTraining,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
        trainingLabels = samples.loadLabelsFile("digitdata/traininglabels", numTraining)
        rawValidationData = samples.loadDataFile("digitdata/validationimages", numTest,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
        validationLabels = samples.loadLabelsFile("digitdata/validationlabels", numTest)
        rawTestData = samples.loadDataFile("digitdata/testimages", numTest,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
        testLabels = samples.loadLabelsFile("digitdata/testlabels", numTest)


    # Extract features
    print("Extracting features...")
    trainingData = list(map(featureFunction, rawTrainingData))
    validationData = list(map(featureFunction, rawValidationData))
    testData = list(map(featureFunction, rawTestData))

    # Conduct training and testing
    print("Training...")
    classifier.train(trainingData, trainingLabels, validationData, validationLabels)
    print("Validating...")
    guesses = classifier.classify(validationData)
    correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
    print(str(correct), ("correct out of " + str(len(validationLabels)) + " (%.1f%%).") % (100.0 * correct / len(validationLabels)))
    print("Testing...")
    guesses = classifier.classify(testData)
    correct = [guesses[i] == testLabels[i] for i in range(len(testLabels))].count(True)
    print(str(correct), ("correct out of " + str(len(testLabels)) + " (%.1f%%).") % (100.0 * correct / len(testLabels)))
    analysis(classifier, guesses, testLabels, testData, rawTestData, printImage)

    # do odds ratio computation if specified at command line
    if((options.odds) & (options.classifier == "naiveBayes" or (options.classifier == "nb")) ):
        label1, label2 = options.label1, options.label2
        features_odds = classifier.findHighOddsFeatures(label1,label2)
        if(options.classifier == "naiveBayes" or options.classifier == "nb"):
            string3 = "=== Features with highest odd ratio of label %d over label %d ===" % (label1, label2)
        else:
            string3 = "=== Features for which weight(label %d)-weight(label %d) is biggest ===" % (label1, label2)

        print(string3)
        printImage(features_odds)

    if((options.weights) & (options.classifier == "perceptron")):
        for l in classifier.legalLabels:
            features_weights = classifier.findHighWeightFeatures(l)
            print(("=== Features with high weight for label %d ==="%l))
            printImage(features_weights)

if __name__ == '__main__':
    # Read input
    args, options = readCommand( sys.argv[1:] )
    # Run classifier
    runClassifier(args, options)
