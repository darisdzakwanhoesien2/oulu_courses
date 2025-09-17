function [ output_args ] = SamplingWithoutReplacement( data, label, size )
%SAMPLINGWITHREPLACEMENT Summary of this function goes here
%   Detailed explanation goes here

r=randperm(1150,size);

figure;
scatter(data(r,1), data(r,2),25, label(r), 'filled');

end

