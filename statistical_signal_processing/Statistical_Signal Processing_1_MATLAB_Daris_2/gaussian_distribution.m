% Set random seed for reproducibility
rng(42);

% Parameters
n_samples = 500;

% 1. Generate x column (500 samples from N(0, 1))
x = randn(n_samples, 1);

% 2. Generate y column (500 samples from N(0.5, 2))
y = sqrt(2) * randn(n_samples, 1) + 0.5;

% Combine x and y into matrix D
D = [x, y];

% 3. Compute z = x + y
z = x + y;

% Compute sample statistics of z
sample_mean_z = mean(z);
sample_var_z = var(z);

% 4. Compute theoretical statistics of z
theoretical_mean_z = 0 + 0.5;  % μₓ + μᵧ
theoretical_var_z = 1 + 2;     % σₓ² + σᵧ²

% 5. Display results
fprintf('Sample Mean of z: %.4f\n', sample_mean_z);
fprintf('Theoretical Mean of z: %.4f\n', theoretical_mean_z);
fprintf('Sample Variance of z: %.4f\n', sample_var_z);
fprintf('Theoretical Variance of z: %.4f\n', theoretical_var_z);

figure;
histogram(z, 'Normalization', 'pdf');
hold on;
x_range = linspace(min(z), max(z), 100);
plot(x_range, normpdf(x_range, theoretical_mean_z, sqrt(theoretical_var_z)), 'r-', 'LineWidth', 2);
xlabel('z');
ylabel('Probability Density');
title('Histogram of z with Theoretical PDF');
legend('Sample Distribution', 'Theoretical PDF');
hold off;