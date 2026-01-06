% Parameters
MC = 10000;  % Number of Monte Carlo loops
N = 20;      % Number of samples
sigma_squared = 1.5;  % Noise variance
theta = 10;  % True parameter value

% Initialize arrays
theta_est = zeros(MC, 1);
n = 0:N-1;

% Cramer-Rao Lower Bound (CRLB)
CRLB = sigma_squared / sum(n.^2);

% Monte Carlo simulation
for i = 1:MC
    % Generate noisy data
    w = sqrt(sigma_squared) * randn(1, N);
    x = theta * n + w;

    % Estimate theta
    theta_est(i) = sum(x .* n) / sum(n.^2);
end

% Calculate mean and variance of the estimator
theta_mean = mean(theta_est);
theta_var = var(theta_est);

% Plot histogram and theoretical PDF
figure;
histogram(theta_est, 'Normalization', 'pdf');
hold on;

x_range = linspace(min(theta_est), max(theta_est), 100);
y_pdf = normpdf(x_range, theta, sqrt(CRLB));
plot(x_range, y_pdf, 'r-', 'LineWidth', 2);

xlabel('Estimated \theta');
ylabel('Probability Density');
title('Histogram of Estimated \theta and Theoretical PDF');
legend('Simulated', 'Theoretical');

% Display results
fprintf('True theta: %.4f\n', theta);
fprintf('Estimated theta (mean): %.4f\n', theta_mean);
fprintf('Variance of estimator: %.6f\n', theta_var);
fprintf('CRLB: %.6f\n', CRLB);
fprintf('Efficiency: %.4f%%\n', 100 * CRLB / theta_var);

% Analysis for N = 1 and N → ∞
N_values = [1, 10, 100, 1000, 10000];
CRLB_N = zeros(size(N_values));

for i = 1:length(N_values)
    n_i = 0:N_values(i)-1;
    CRLB_N(i) = sigma_squared / sum(n_i.^2);
end

figure;
semilogx(N_values, CRLB_N, 'bo-', 'LineWidth', 2);
xlabel('N (log scale)');
ylabel('CRLB');
title('CRLB vs. N');
grid on;