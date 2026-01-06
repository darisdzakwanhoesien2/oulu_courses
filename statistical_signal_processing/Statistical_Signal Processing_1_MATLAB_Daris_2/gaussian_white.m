% 1. Create a 2x2 covariance matrix Σ
Sigma = [1.0 0.5; 0.5 2.0];

% 2. Generate a white Gaussian random vector w
n_samples = 1000;
w = randn(2, n_samples);

% 3. Perform Cholesky decomposition on Σ
L = chol(Sigma, 'lower');

% 4. Map w to a new Gaussian random vector x
x = L * w;

% 5. Compute and verify the sample covariance matrix
sample_cov = cov(x');

% Display results
disp('Original Covariance Matrix (Sigma):');
disp(Sigma);
disp('Sample Covariance Matrix:');
disp(sample_cov);
disp('Difference:');
disp(abs(Sigma - sample_cov));