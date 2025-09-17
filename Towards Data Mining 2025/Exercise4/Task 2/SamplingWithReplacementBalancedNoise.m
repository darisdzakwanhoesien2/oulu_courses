function [ output_args ] = SamplingWithReplacementBalancedNoise( data, label, size )
%SAMPLINGWITHREPLACEMENT Summary of this function goes here
%   Detailed explanation goes here

r1=randi([1 1000], 1, size);
r2=randi([1001 1050], 1, size);
r3=randi([1051 1150], 1, size);

n1 = wgn2(size,1,-20);
n2 = wgn2(size,1,-20);
n3 = wgn2(size,1,-20);

n1y = wgn2(size,1,-20);
n2y = wgn2(size,1,-20);
n3y = wgn2(size,1,-20);

figure;
scatter(data(r1,1)+n1, data(r1,2)+n1y, 25, label(r1), 'filled');
hold on;
scatter(data(r2,1)+n2, data(r2,2)+n2y, 25, label(r2), 'filled');
hold on;
scatter(data(r3,1)+n3, data(r3,2)+n3y, 25, label(r3), 'filled');
hold off;
end

