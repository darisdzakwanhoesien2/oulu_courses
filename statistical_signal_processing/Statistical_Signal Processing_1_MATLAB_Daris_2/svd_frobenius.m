% Set random seed for reproducibility
rng(42);

% Define matrix size and distribution parameters
n = 50;
mu = 1;
sigma = sqrt(0.5);

% 1. Create the random matrix A
A = mu + sigma * (randn(n) + 1i * randn(n));

% Verify the variance
actual_variance = var(A(:));
fprintf('Actual variance: %.4f\n', actual_variance);

% 2. Compute the SVD
[U, S, V] = svd(A);

% 3. Reconstruct A using SVD components
Asvd = U * S * V';

% 4. Verify reconstruction quality
frobenius_norm = norm(A - Asvd, 'fro')^2;
fprintf('Frobenius norm ||A - Asvd||^2: %.4e\n', frobenius_norm);