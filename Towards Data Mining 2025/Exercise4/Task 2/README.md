# Code Explanations

## `cirrdnPJ.m`

This MATLAB function, `cirrdnPJ`, generates random coordinates (x, y) within a circle.

**Inputs:**
- `x1`: The x-coordinate of the center of the circle.
- `y1`: The y-coordinate of the center of the circle.
- `rc`: The radius of the circle.

**Outputs:**
- `x`: The randomly generated x-coordinate within the circle.
- `y`: The randomly generated y-coordinate within the circle.

**Functionality:**
1. `a = 2 * pi * rand`: Generates a random angle `a` in radians, uniformly distributed between 0 and 2π.
2. `r = sqrt(rand)`: Generates a random radius `r`. By taking the square root of a uniformly distributed random number between 0 and 1, this ensures a uniform distribution of points within the circle (otherwise, points would be denser near the center).
3. `x = (rc * r) * cos(a) + x1`: Calculates the x-coordinate using polar to Cartesian conversion, scaling by `rc * r` and offsetting by `x1`.
4. `y = (rc * r) * sin(a) + y1`: Calculates the y-coordinate similarly, scaling by `rc * r` and offsetting by `y1`.

This function is useful for simulating points randomly distributed within a circular region.

## `SamplingWithoutReplacement.m`

This MATLAB function, `SamplingWithoutReplacement`, performs random sampling without replacement from a dataset and visualizes the sampled data.

**Inputs:**
- `data`: A matrix where each row represents a data point and columns represent features.
- `label`: A vector of labels corresponding to each data point in `data`.
- `size`: The number of samples to draw from the dataset.

**Outputs:**
- `output_args`: This function does not explicitly return any output arguments, but it generates a scatter plot.

**Functionality:**
1. `r = randperm(1150, size)`: Generates a row vector `r` containing `size` unique random integers chosen from the range 1 to 1150. This is used to select `size` random indices from the dataset without replacement. The number `1150` likely represents the total number of data points available in the `data` and `label` matrices.
2. `figure;`: Creates a new figure window for the plot.
3. `scatter(data(r,1), data(r,2), 25, label(r), 'filled')`: Creates a 2D scatter plot.
    - `data(r,1)`: The x-coordinates of the sampled data points (first feature).
    - `data(r,2)`: The y-coordinates of the sampled data points (second feature).
    - `25`: The size of the markers in the scatter plot.
    - `label(r)`: The color of each marker, determined by the label of the sampled data point.
    - `'filled'`: Fills the markers.

This function is useful for creating a subset of data for analysis or visualization, ensuring that each data point is selected at most once.

## `SamplingWithReplacement.m`

This MATLAB function, `SamplingWithReplacement`, performs random sampling with replacement from a dataset and visualizes the sampled data.

**Inputs:**
- `data`: A matrix where each row represents a data point and columns represent features.
- `label`: A vector of labels corresponding to each data point in `data`.
- `size`: The number of samples to draw from the dataset.

**Outputs:**
- `output_args`: This function does not explicitly return any output arguments, but it generates a scatter plot.

**Functionality:**
1. `r = randi([1 1150], 1, size)`: Generates a 1-by-`size` row vector `r` containing random integers chosen with replacement from the range 1 to 1150. This is used to select `size` random indices from the dataset with replacement. The number `1150` likely represents the total number of data points available in the `data` and `label` matrices.
2. `figure;`: Creates a new figure window for the plot.
3. `scatter(data(r,1), data(r,2), 25, label(r), 'filled')`: Creates a 2D scatter plot, similar to `SamplingWithoutReplacement.m`.
    - `data(r,1)`: The x-coordinates of the sampled data points (first feature).
    - `data(r,2)`: The y-coordinates of the sampled data points (second feature).
    - `25`: The size of the markers in the scatter plot.
    - `label(r)`: The color of each marker, determined by the label of the sampled data point.
    - `'filled'`: Fills the markers.

This function is useful for bootstrapping or other statistical methods where data points can be selected multiple times.

## `SamplingWithReplacementBalanced.m`

This MATLAB function, `SamplingWithReplacementBalanced`, performs random sampling with replacement from a dataset, specifically designed to balance samples across different ranges (presumably representing different classes or groups), and visualizes the sampled data.

**Inputs:**
- `data`: A matrix where each row represents a data point and columns represent features.
- `label`: A vector of labels corresponding to each data point in `data`.
- `size`: The number of samples to draw from each specified range.

**Outputs:**
- `output_args`: This function does not explicitly return any output arguments, but it generates a scatter plot.

**Functionality:**
1. `r1 = randi([1 1000], 1, size)`: Generates `size` random indices with replacement from the range 1 to 1000. This likely corresponds to the first class/group.
2. `r2 = randi([1001 1050], 1, size)`: Generates `size` random indices with replacement from the range 1001 to 1050. This likely corresponds to a second, smaller class/group.
3. `r3 = randi([1051 1150], 1, size)`: Generates `size` random indices with replacement from the range 1051 to 1150. This likely corresponds to a third, also smaller class/group.
4. `figure;`: Creates a new figure window.
5. `scatter(data(r1,1), data(r1,2), 25, label(r1), 'filled');`: Plots the sampled data points from the first range.
6. `hold on;`: Holds the current plot so that subsequent plots are added to it.
7. `scatter(data(r2,1), data(r2,2), 25, label(r2), 'filled');`: Plots the sampled data points from the second range on the same figure.
8. `hold on;`: Holds the current plot.
9. `scatter(data(r3,1), data(r3,2), 25, label(r3), 'filled');`: Plots the sampled data points from the third range on the same figure.
10. `hold off;`: Releases the hold on the plot, so new plots will create new figures.

This function is particularly useful in scenarios with imbalanced datasets, where you want to ensure an equal number of samples from different classes or strata for training or visualization purposes.

## `SamplingWithReplacementBalancedNoise.m`

This MATLAB function, `SamplingWithReplacementBalancedNoise`, extends the balanced sampling with replacement by adding Gaussian noise to the sampled data points before visualization. This can be useful for data augmentation or to simulate noisy measurements.

**Inputs:**
- `data`: A matrix where each row represents a data point and columns represent features.
- `label`: A vector of labels corresponding to each data point in `data`.
- `size`: The number of samples to draw from each specified range.

**Outputs:**
- `output_args`: This function does not explicitly return any output arguments, but it generates a scatter plot.

**Functionality:**
1. `r1 = randi([1 1000], 1, size)`: Generates `size` random indices with replacement from the range 1 to 1000 (first class/group).
2. `r2 = randi([1001 1050], 1, size)`: Generates `size` random indices with replacement from the range 1001 to 1050 (second class/group).
3. `r3 = randi([1051 1150], 1, size)`: Generates `size` random indices with replacement from the range 1051 to 1150 (third class/group).
4. `n1 = wgn2(size,1,-20);`, `n2 = wgn2(size,1,-20);`, `n3 = wgn2(size,1,-20);`: Generates `size` samples of white Gaussian noise for the x-coordinates of each group. The `-20` likely refers to the power of the noise in dBW.
5. `n1y = wgn2(size,1,-20);`, `n2y = wgn2(size,1,-20);`, `n3y = wgn2(size,1,-20);`: Generates `size` samples of white Gaussian noise for the y-coordinates of each group.
6. `figure;`: Creates a new figure window.
7. `scatter(data(r1,1)+n1, data(r1,2)+n1y, 25, label(r1), 'filled');`: Plots the sampled data points from the first range with added noise to both x and y coordinates.
8. `hold on;`: Holds the current plot.
9. `scatter(data(r2,1)+n2, data(r2,2)+n2y, 25, label(r2), 'filled');`: Plots the sampled data points from the second range with added noise.
10. `hold on;`: Holds the current plot.
11. `scatter(data(r3,1)+n3, data(r3,2)+n3y, 25, label(r3), 'filled');`: Plots the sampled data points from the third range with added noise.
12. `hold off;`: Releases the hold on the plot.

This function is useful for augmenting datasets by introducing controlled noise, which can help in training more robust models, especially when dealing with limited data or simulating real-world sensor noise.

## `wgn2.m`

This MATLAB function, `wgn2`, is a custom implementation or a copy of MATLAB's built-in `wgn` function, which generates white Gaussian noise. It provides flexible options for controlling the dimensions, power, impedance, and type of noise.

**Inputs (variable arguments):**
- `M, N`: Dimensions of the output noise matrix (M-by-N).
- `P`: Power of the output noise. By default, in dBW.
- `IMP` (optional): Load impedance in Ohms (default is 1 Ohm).
- `S` (optional): Seed for the random number generator, either an integer or a `RandStream` object, to generate repeatable noise samples.
- `POWERTYPE` (optional string): Specifies the units of `P`. Can be `'dBW'`, `'dBm'`, or `'linear'` (Watts).
- `OUTPUTTYPE` (optional string): Specifies the output type. Can be `'real'` or `'complex'`. If complex, `P` is divided equally between real and imaginary components.

**Outputs:**
- `y`: An M-by-N matrix of white Gaussian noise.

**Functionality:**
The function parses its variable input arguments to determine the dimensions (`row`, `col`), power (`p`), impedance (`imp`), seed (`seed`), power mode (`pMode`), and complexity mode (`cplxMode`).

1.  **Argument Parsing and Validation**:
    *   It first checks the number of input arguments and identifies numeric and string arguments.
    *   It sets default values for `pMode` ('dbw'), `imp` (1 Ohm), `cplxMode` ('real'), and `seed` (empty).
    *   It then parses the numeric arguments for `row`, `col`, `p`, `imp`, and `seed`.
    *   String arguments are parsed for `POWERTYPE` and `OUTPUTTYPE`.
    *   Extensive validation is performed on all parameters to ensure they are of the correct type and within valid ranges (e.g., power cannot be negative in linear mode, dimensions must be positive integers, impedance must be positive).

2.  **Noise Power Calculation**:
    *   Based on `pMode`, the input power `p` is converted into linear noise power:
        *   `'linear'`: `noisePower = p`
        *   `'dbw'`: `noisePower = 10^(p/10)`
        *   `'dbm'`: `noisePower = 10^((p-30)/10)`

3.  **Noise Generation**:
    *   If a `seed` is provided, a `RandStream` is initialized (or used directly if `seed` is already a `RandStream` object) to ensure repeatable random numbers. Otherwise, the default `randn` function is used.
    *   If `cplxMode` is `'complex'`:
        *   `y = (sqrt(imp*noisePower/2))*(func(row, col)+1i*func(row, col))`: Generates complex noise where the total power `noisePower` is split equally between the real and imaginary parts.
    *   If `cplxMode` is `'real'`:
        *   `y = (sqrt(imp*noisePower))*func(row, col)`: Generates real noise.

This function is a fundamental tool for simulating noise in communication systems, signal processing, and other applications where random Gaussian noise is required.

## Explanation of `SamplingWithReplacement` Properties

Here are the correct statements regarding `SamplingWithReplacement`:

1.  **With SamplingWithReplacement same data point could be chosen to a sample multiple times**
    *   **Explanation:** This is the defining characteristic of sampling with replacement. After a data point is selected for the sample, it is "returned" to the original dataset, making it available for selection again in subsequent draws.

2.  **With SamplingWithReplacement sample size can be larger than amount of data points in the original data**
    *   **Explanation:** Because data points are replaced after each selection, the pool of available data points remains constant. This allows for drawing a sample of any desired size, even if that size exceeds the total number of data points in the original dataset.

3.  **With SamplingWithReplacement chance of being selected to a sample is constant**
    *   **Explanation:** In simple random sampling with replacement, every data point in the original dataset has an equal probability of being selected at each draw. This probability remains constant throughout the sampling process because each selected item is returned to the population.
