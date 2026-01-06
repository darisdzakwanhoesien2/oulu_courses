% Set random seed for reproducibility
rng(42);

% Parameters
a = -1;
b = 5;
n_samples = 1000;

% Generate samples
samples = a + (b - a) * rand(n_samples, 1);

% Plot histogram
histogram(samples, 'Normalization', 'pdf');
xlabel('x');
ylabel('Probability Density');
title('Histogram of Uniform Distribution Samples');

% Add theoretical PDF line
hold on;
x = linspace(a, b, 100);
y = ones(size(x)) / (b - a);
plot(x, y, 'r-', 'LineWidth', 2);
legend('Sampled Data', 'Theoretical PDF');
hold off;

% Display sample statistics
fprintf('Sample Mean: %.4f (Expected: 2)\n', mean(samples));
fprintf('Sample Variance: %.4f (Expected: 3)\n', var(samples));