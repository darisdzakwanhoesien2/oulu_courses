% Parameters
A = 2;
sigma2 = 0.5;
MC = 100000;
rho_values = [-1, 0, 0.5, 1];

% Results storage
simulated_means = zeros(1, length(rho_values));
theoretical_means = A * ones(1, length(rho_values));
simulated_variances = zeros(1, length(rho_values));
theoretical_variances = zeros(1, length(rho_values));

% Monte Carlo Simulations
for idx = 1:length(rho_values)
    rho = rho_values(idx);
    C = sigma2 * [1, rho; rho, 1];
    samples = zeros(1, MC);
    
    for k = 1:MC
        w = mvnrnd([0, 0], C);
        x = A + w';
        samples(k) = mean(x);
    end
    
    simulated_means(idx) = mean(samples);
    simulated_variances(idx) = var(samples);
    theoretical_variances(idx) = sigma2 * (1 + rho) / 2;
end

% Display Results
fprintf('Results:\n');
fprintf('rho\tSimulated Mean\tTheoretical Mean\tSimulated Variance\tTheoretical Variance\n');
for idx = 1:length(rho_values)
    fprintf('%1.1f\t%f\t%f\t%f\t%f\n', rho_values(idx), simulated_means(idx), theoretical_means(idx), simulated_variances(idx), theoretical_variances(idx));
end