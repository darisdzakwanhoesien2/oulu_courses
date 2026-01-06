% Parameters
MC = 100000;  % Number of Monte Carlo simulations
N = 100;      % Number of samples per simulation
theta = 1;    % True value of θ

% Initialize arrays to store estimates
theta_MLE = zeros(MC, 1);
A_est_mean = zeros(MC, 1);

% Monte Carlo simulation
for i = 1:MC
    % Generate N random variables from U[0, θ]
    X = theta * rand(N, 1);
    
    % MLE estimator
    theta_MLE(i) = max(X);
    
    % A_est_mean estimator
    A_est_mean(i) = mean(X) * 2;
end

% Calculate means of estimators
mean_MLE = mean(theta_MLE);
mean_A_est = mean(A_est_mean);

% Display results
fprintf('True θ: %f\n', theta);
fprintf('Mean of MLE estimator: %f\n', mean_MLE);
fprintf('Mean of A_est_mean estimator: %f\n', mean_A_est);