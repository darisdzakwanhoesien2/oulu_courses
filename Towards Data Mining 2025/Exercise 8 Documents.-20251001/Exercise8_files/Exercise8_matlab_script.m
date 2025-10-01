%% Human Activity Classification based on Smartphone Sensor Signals
% 
% These examples are modified from Matlab Webinar: 
% Signal Processing and Machine Learning Techniques for Sensor Data Analytics
% Gabriele Bunkheila, MathWorks
% https://se.mathworks.com/videos/signal-processing-and-machine-learning-techniques-for-sensor-data-analytics-107549.html

%% Introduction
% This example describes an analysis approach on accelerometer signals
% captured with a smartphone. The smartphone is worn by a subject during 6
% different types of physical activity. 
% The goal of the analysis is to build an algorithm that automatically
% identifies the activity type given the sensor measurements. 
%
% The example uses data from a recorded dataset, courtesy of:
%  Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra and Jorge L.
%  Reyes-Ortiz. Human Activity Recognition on Smartphones using a
%  Multiclass Hardware-Friendly Support Vector Machine. International
%  Workshop of Ambient Assisted Living (IWAAL 2012). Vitoria-Gasteiz,
%  Spain. Dec 2012
%
% The original dataset is available from
% <http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones>

%% Open a "recording" for participant #1 (gravitational acceleration filtered out )
% Take a look at the data. Given the data:
% 
% * We would like to be able to tell the difference between the different
%   activities, just based on the content of the signal. 
% * Note in this case the coloring is based on existing knowledge (actid)
% * Labeled data can be used to "train" a classification algorithm so it
%   can later predict the class of new (unlabeled) data. 

load('participant_1_raw_data.mat');

% Visualize the signal using a custom plotting function, which also
% uses the information in actid
figure
plotAccelerationColouredByActivity(t, acc, actid, {'Vertical acceleration'})

%% Walking
% Take a closer look at a single activity first: select Walking signal

% Assume we know the activity id for Walking is 1
walking = 1;

% Select only desired array segments for time vector
% and acceleration signal
t_walking = t(actid == walking);
acc_walking = acc(actid == walking);

% Plot walking-only signal segment. 
% Use interactive plot tools to zoom in (magnifying class with + sign)
% and explore the signal. Note the quasi-periodic behavior.
figure
plotAccelerationColouredByActivity(t_walking, acc_walking, [],'Walking')

%% Features

% Let's skip calculating features from the data in this excercise and use 
% a pre-computed feature dataset.

% Altogether 66 features in time and frequency domain were calculated from 
% the raw data on sliding windows of 2.56 sec and 50% overlap 
% (128 readings/window). 

load('participant_1_feature_data.mat');

%% Training and test sets

% Reset random number generators
rng(1,'twister');

% c = cvpartition(group,'HoldOut',p) randomly partitions observations into
% a training set and a test set with stratification, using the class 
% information in group; that is, both training and test sets have roughly 
% the same class proportions as in group.  When 0 < p < 1, cvpartition 
% randomly selects approximately p*n observations for the test set. When p 
% is an integer, cvpartition randomly selects p observations for the test 
% set. The default value of p is 1/10.
cvp = cvpartition(categorical(actid_p1), 'Holdout', 0.25);

% Use this partition of the dataset to divide it into training and testing
featTrain = features_p1(cvp.training,:);
actidTrain = actid_p1(cvp.training,:);
featTest = features_p1(cvp.test,:);
actidTest = actid_p1(cvp.test,:);


%% Train model Neural Network 1: 
% Let's now create, train and test a neural network using the Neural Network 
% Toolbox

% Initialize a Neural Network with 18 nodes in hidden layer
% (assume the choice of the number 18 here is arbitrary)
net = patternnet(18);

% Reset random number generators
rng(1,'twister');

% Train network
% For details about customizing the training function refer to the
% following:
% web(fullfile(docroot, 'nnet/ug/choose-a-multilayer-neural-network-training-function.html'))
net = train(net, featTrain', dummyvar(actidTrain)');


%% Test model Neural Network 1:
% Predict activity ID from test portion of dataset
predActidNN = net(featTest');

% Display accuracy of results as confusion matrix
figure
plotconfusion(dummyvar(actidTest)',predActidNN)

%% 3-Nearest Neighbors classifier 1: 

% Alternatively, you can use the 3NN classifier

Mdl = fitcknn(featTrain,actidTrain,'NumNeighbors',3);
predActidkNN = predict(Mdl,featTest);
figure
plotconfusion(dummyvar(actidTest)',dummyvar(predActidkNN)')

%% Training and test sets 2

% Let's divide the training and test sets a bit differently.
featTrain = [];
actidTrain = [];
featTest = [];
actidTest = [];

% Assign the first 75% of the feature data from each activity into training 
% and the last 25% of each activity into testing
classes = unique(actid_p1);
for i=1:length(classes)
    
    features_class_i = features_p1(actid_p1 == i,:);
    len_training = round(0.75*size(features_class_i,1));
    featTrain = [featTrain; features_class_i(1:len_training,:)];
    featTest = [featTest; features_class_i(len_training+1:end,:)];
    actidTrain = [actidTrain; classes(i)*ones(len_training,1)];
    actidTest = [actidTest; classes(i)*ones(size(features_class_i,1)-len_training,1)];
    
end

%% Train model Neural Network 2

% Initialize a Neural Network with 18 nodes in hidden layer
% (assume the choice of the number 18 here is arbitrary)
net = patternnet(18);

% Reset random number generators
rng(1,'twister');

% Train network
net = train(net, featTrain', dummyvar(actidTrain)');

%% Test model Neural Network 2:
% Predict activity ID from test portion of dataset
predActidNN = net(featTest');

% Display accuracy of results as confusion matrix
figure
plotconfusion(dummyvar(actidTest)',predActidNN)

%% 3-Nearest Neighbors classifier 2: 

% Alternatively, you can use the 3NN classifier

Mdl = fitcknn(featTrain,actidTrain,'NumNeighbors',3);
predActidkNN = predict(Mdl,featTest);
figure
plotconfusion(dummyvar(actidTest)',dummyvar(predActidkNN)')

%% A separate test set

% Finally, let's load participant 1's data again, this time with all the
% activities done twice (at least).

load('participant_1_data_v2.mat');

% Visualize the signal 
figure
plotAccelerationColouredByActivity(t, acc, actid, {'Vertical acceleration'})

% Let's now train the neural network using the first part of the
% measurement and test it with the second part.

% The feature values and activity id's for the second part of the data can 
% be found in variables "features_p1_test" and "actid_p1_test".

% Training and test sets
featTrain = features_p1;
actidTrain = actid_p1;
featTest = features_p1_test;
actidTest = actid_p1_test;

%% Train model Neural Network 3:

% Initialize a Neural Network with 18 nodes in hidden layer
% (assume the choice of the number 18 here is arbitrary)
net = patternnet(18);

% Reset random number generators
rng(1,'twister');

% Train network
net = train(net, featTrain', dummyvar(actidTrain)');

%% Test model Neural Network 3:
% Predict activity ID from test portion of dataset
predActidNN = net(featTest');

% Display accuracy of results as confusion matrix
figure
plotconfusion(dummyvar(actidTest)',predActidNN)

%% 3-Nearest Neighbors classifier 3: 

% Alternatively, you can use the 3NN classifier

Mdl = fitcknn(featTrain,actidTrain,'NumNeighbors',3);
predActidkNN = predict(Mdl,featTest);
figure
plotconfusion(dummyvar(actidTest)',dummyvar(predActidkNN)')

%% 






