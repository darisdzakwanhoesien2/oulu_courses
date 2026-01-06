% Parameter initialization
N = 5;
A_true = 1;
sigma2 = 0.001;
fo_true = 1/4;
phi_true = pi/3;
MC = 100000;

% Arrays to store estimates
A_est = zeros(MC, 1);
fo_est = zeros(MC, 1);
phi_est = zeros(MC, 1);

% Time vector
n = 0:N-1;

% Monte Carlo simulation
for mc = 1:MC
    % Generate noisy signal
    w = sqrt(sigma2) * randn(1, N);
    x = A_true * cos(2*pi*fo_true*n + phi_true) + w;
    
    % Initial guess for optimization
    theta_init = [A_true*0.9; fo_true*1.1; phi_true*0.9];
    
    % Cost function
    cost_fun = @(theta) sum((x - theta(1)*cos(2*pi*theta(2)*n + theta(3))).^2);
    
    % Optimization
    options = optimset('Display', 'off');
    theta_est = fminsearch(cost_fun, theta_init, options);
    
    % Store estimates
    A_est(mc) = theta_est(1);
    fo_est(mc) = theta_est(2);
    phi_est(mc) = theta_est(3);
end

% Compute CRLB
t = n';
s = A_true * cos(2*pi*fo_true*t + phi_true);
ds_dA = cos(2*pi*fo_true*t + phi_true);
ds_dfo = -2*pi*A_true*t.*sin(2*pi*fo_true*t + phi_true);
ds_dphi = -A_true*sin(2*pi*fo_true*t + phi_true);

FIM = zeros(3,3);
FIM(1,1) = sum(ds_dA.^2)/sigma2;
FIM(1,2) = sum(ds_dA.*ds_dfo)/sigma2;
FIM(1,3) = sum(ds_dA.*ds_dphi)/sigma2;
FIM(2,1) = FIM(1,2);
FIM(2,2) = sum(ds_dfo.^2)/sigma2;
FIM(2,3) = sum(ds_dfo.*ds_dphi)/sigma2;
FIM(3,1) = FIM(1,3);
FIM(3,2) = FIM(2,3);
FIM(3,3) = sum(ds_dphi.^2)/sigma2;

CRLB = inv(FIM);

% Compute variances of estimates
var_A = var(A_est);
var_fo = var(fo_est);
var_phi = var(phi_est);

% Display results
fprintf('Parameter Variances vs CRLB:\n');
fprintf('A: Var = %.6f, CRLB = %.6f\n', var_A, CRLB(1,1));
fprintf('fo: Var = %.6f, CRLB = %.6f\n', var_fo, CRLB(2,2));
fprintf('phi: Var = %.6f, CRLB = %.6f\n', var_phi, CRLB(3,3));

% Plot histograms
figure;
subplot(3,1,1);
histogram(A_est, 50, 'Normalization', 'probability');
title('Histogram of A estimates');

subplot(3,1,2);
histogram(fo_est, 50, 'Normalization', 'probability');
title('Histogram of fo estimates');

subplot(3,1,3);
histogram(phi_est, 50, 'Normalization', 'probability');
title('Histogram of phi estimates');