function [ output_args ] = SamplingWithReplacement( data, label, size )
%SAMPLINGWITHREPLACEMENT Summary of this function goes here
%   Detailed explanation goes here

r=randi([1 1150], 1, size);

figure;
scatter(data(r,1), data(r,2),25, label(r), 'filled');

end

