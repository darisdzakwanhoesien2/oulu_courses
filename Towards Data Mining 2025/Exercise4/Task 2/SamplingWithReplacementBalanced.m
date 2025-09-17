function [ output_args ] = SamplingWithReplacementBalanced( data, label, size )
%SAMPLINGWITHREPLACEMENT Summary of this function goes here
%   Detailed explanation goes here

r1=randi([1 1000], 1, size);
r2=randi([1001 1050], 1, size);
r3=randi([1051 1150], 1, size);

figure;
scatter(data(r1,1), data(r1,2), 25, label(r1), 'filled');
hold on;
scatter(data(r2,1), data(r2,2), 25, label(r2), 'filled');
hold on;
scatter(data(r3,1), data(r3,2), 25, label(r3), 'filled');
hold off;
end

