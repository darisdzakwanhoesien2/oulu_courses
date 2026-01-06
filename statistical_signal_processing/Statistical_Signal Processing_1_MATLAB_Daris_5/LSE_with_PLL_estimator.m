% Parameters
M = 2;
A = 1;
sigma2 = 0.001;
fo = 1/4;
phi = pi/3;
iterations = 10;

% Generate time vector
n = -M:M;

% Generate signal
w = sqrt(sigma2)*randn(size(n));
x = A*cos(2*pi*fo*n + phi) + w;

% Initial estimates
f_est = zeros(1,iterations+1);
phi_est = zeros(1,iterations+1);
f_est(1) = 0.2;  % Initial frequency guess
phi_est(1) = 0;  % Initial phase guess

% Step sizes
mu_f = 0.1;
mu_phi = 0.1;

% PLL iterations
for k = 1:iterations
    % Update frequency
    df = 0;
    for i = 1:length(n)
        df = df + n(i)*sin(2*pi*f_est(k)*n(i) + phi_est(k))*x(i);
    end
    f_est(k+1) = f_est(k) + mu_f*df;
    
    % Update phase
    dphi = 0;
    for i = 1:length(n)
        dphi = dphi + sin(2*pi*f_est(k+1)*n(i) + phi_est(k))*x(i);
    end
    phi_est(k+1) = phi_est(k) + mu_phi*dphi;
end

% Final estimated values
final_freq = f_est(end);
final_phase = phi_est(end);

% Calculate MSE for frequency and phase
mse_f = mean((f_est - fo).^2);
mse_phi = mean((phi_est - phi).^2);

% Display results
fprintf('Final Estimated Frequency: %.4f Hz\n', final_freq);
fprintf('Final Estimated Phase: %.4f rad\n', final_phase);
fprintf('MSE of Frequency: %.5f\n', mse_f);
fprintf('MSE of Phase: %.5f\n', mse_phi);

% Plot estimated values over iterations
figure;
subplot(2, 1, 1);
plot(0:iterations, f_est, '-o', 'MarkerSize', 5);
hold on;
yline(fo, '--r', 'True f_o');
title('Frequency Convergence');
xlabel('Iteration');
ylabel('Frequency (Hz)');
grid on;

subplot(2, 1, 2);
plot(0:iterations, phi_est, '-o', 'MarkerSize', 5);
hold on;
yline(phi, '--r', 'True \phi');
title('Phase Convergence');
xlabel('Iteration');
ylabel('Phase (rad)');
grid on;

sgtitle('Convergence of LSE with PLL Estimator');