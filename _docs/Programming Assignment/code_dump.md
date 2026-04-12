# 📦 Full Code Dump — `Programming Assignment`

> Source path: `/Users/darisdzakwanhoesien/Documents/project_documentation/codebase/education/oulu_courses/machine_vision/Programming Assignment`

> Auto-generated snapshot of the entire codebase

---

## 📁 `A1-Imaging_Daris_2406778/MV_A1.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 1 – Imaging

## Personal details

* **Name:** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Introduction

In this assignment, you will read and display images in Python, use a depth map to simulate shallow depth of field (Bokeh effect), and simulate vignetting to create brightness fall-off near image edges. Please study __[`Lecture 2`](https://moodle.oulu.fi/mod/page/view.php?id=1705510)__ and the sample code in __[`Imaging.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Imaging.ipynb)__ before starting. The figure below shows the expected final outcome.

<img src="fig1.jpg">

### 📝 Markdown Cell 2

## Task 1 – Read and display images (0.5 points)

In this task, you will practice basic image reading and visualization. You will load a color image and a depth map, then display them side by side. The depth map was generated using __[`DepthAnything-V2`](https://github.com/DepthAnything/Depth-Anything-V2)__, a state-of-the-art monocular depth estimation method that predicts relative depth from a single image. The depth map has been manually adjusted to approximate metric depth and is stored as a 16-bit image with depth values in millimeters.

### Instructions
- **Read** `image.jpg` and `depth.png` using the OpenCV library. Use the flag `cv2.IMREAD_UNCHANGED` to properly read the 16-bit depth map.
- **Convert** the color image from BGR to RGB as this is the order of color channels expected by Matplotlib.
- **Display** both images side by side using Matplotlib.

### 💻 Code Cell 3

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```

### 💻 Code Cell 4

```python
# ---------- YOUR CODE STARTS HERE -----------
# Step 1: Read the images
# Read the color image
color_image = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)

# Read the depth map
depth_map = cv2.imread('depth.png', cv2.IMREAD_UNCHANGED)

# Step 2: Convert the color image from BGR to RGB
color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

# Step 3: Display the images side by side using Matplotlib
plt.figure(figsize=(12, 6))

# Display the color image
plt.subplot(1, 2, 1)
plt.imshow(color_image_rgb)
plt.title('Color Image')
plt.axis('off')

# Display the depth map
plt.subplot(1, 2, 2)
plt.imshow(depth_map, cmap='gray')
plt.title('Depth Map')
plt.axis('off')

# Show the plot
plt.tight_layout()
plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 5

## Task 2 – Synthetic Bokeh (0.5 points)

In this task, you will simulate a shallow depth-of-field effect, commonly referred to as the **Bokeh effect**. This effect is achieved by blurring parts of the image that are not in focus, mimicking the behavior of a lens with a wide aperture (small F-number). Smartphones typically have small sensors and large depth of field, resulting in images where both foreground and background are sharp. By artificially simulating defocus blur, we can create the Bokeh effect, selectively emphasizing the object in focus (e.g., the dog in the provided image).

### Background
The **thin-lens equation** is the foundation of defocus blur simulation:

$$\frac{1}{f} = \frac{1}{z_o} + \frac{1}{z_i}$$

- $f$ is the focal length of the lens (in mm).
- $z_o$ is the distance to the object being photographed (in mm).
- $z_i$ is the distance to the image plane (in mm).

Points outside the focus plane appear as small blurred circles, referred to as the circle of confusion (CoC). The size of the CoC depends on the distance of the point from the focus plane and is given by:
$$c = D \cdot \frac{|z_f - z_i|}{z_i}$$
where:
- $D$ is the aperture diameter (in mm), calculated as $D = \frac{f}{N}$, where $N$ is the F-number.
- $z_f$ is the image distance for the focus plane (in mm).
- $z_i$ is the image distance for a given depth (in mm).

The size of the CoC, converted to pixels using a sensor-specific scaling factor, determines the extent of blur applied to each pixel. The scaling factor, `pixels_per_mm`, is calculated based on the physical size of the sensor (e.g., 36 mm) and the resolution of the image, linking real-world measurements to pixel dimensions.

The function `defocus_blur` below (adapted from __[`Imaging.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Imaging.ipynb)__) uses this model to simulate defocus blur by applying a Gaussian blur proportional to the CoC size. While Gaussian blur is simple and efficient, a more physically accurate approach would involve using a disk-shaped kernel to mimic the shape of an aperture.

### 💻 Code Cell 6

```python
def defocus_blur(img, depth, f, D, fdist, pixels_per_mm):
    """
    Apply a synthetic defocus blur based on the thin-lens model.

    Parameters
    ----------
    img : Color image (H x W x 3)
    depth : Depth map in mm (H x W)
    f : Focal length in mm
    D : Aperture diameter in mm
    fdist : Focus distance (mm)
    pixels_per_mm : Conversion factor from mm to pixels

    Returns
    -------
    blurred : The blurred image
    """

    depth = depth.astype(np.float32)
    zf = 1.0 / (1.0/f - 1.0/fdist)  # image distance for the focus plane
    zi = 1.0 / (1.0/f - 1.0/depth)  # image distance for each pixel

    dz = np.abs(zf - zi)
    c = D * (dz / zi)          # circle of confusion in mm
    c *= pixels_per_mm         # convert mm -> pixels
    c = np.clip(c, 0.0, 150.0) # limit the maximum size for safety

    ci = np.linspace(c.min(), c.max(), 20)
    dc = np.digitize(c, ci)
    blurred = np.zeros_like(img)

    for i in range(20):
        sigma = ci[i]/2 + 0.01
        gblur = cv2.GaussianBlur(img, (0,0), sigma)
        mask = (dc == i+1).astype(np.uint8)
        blurred += cv2.bitwise_and(gblur, gblur, mask=mask)

    return blurred
```

### 📝 Markdown Cell 7

### Instructions
- **Use** the provided `defocus_blur` function to apply synthetic Bokeh to the image.
- **Assume** the dog is approximately 10 meters away (10 000 mm).
- **Set** the focal length $f = 200$ mm and the F-number $N = 2.0$.
- **Compute** `pixels_per_mm` by dividing the image width by 36 (mm). 
- **Display** the resulting image with Bokeh effect.

### 💻 Code Cell 8

```python
# ---------- YOUR CODE STARTS HERE -----------
# Convert the image to RGB
image = cv2.imread('image.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Parameters for the thin-lens model
focal_length = 200  # in mm
f_number = 2.0
aperture_diameter = focal_length / f_number
focus_distance = 10000  # in mm (dog distance)

# Calculate pixels_per_mm based on image width (assume sensor width = 36 mm)
image_width = image.shape[1]
pixels_per_mm = image_width / 36.0

# Apply the synthetic Bokeh effect
bokeh_image = defocus_blur(image_rgb, depth_map, focal_length, aperture_diameter, focus_distance, pixels_per_mm)

# Display the original and blurred images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(bokeh_image)
plt.title("Bokeh Effect")
plt.axis("off")

plt.tight_layout()
plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 9

## Task 3 – Vignetting (1.0 point)

Vignetting refers to the reduction of brightness near the edges of an image, which is a common effect in photography. This phenomenon is often modeled by the cosine fourth law (refer to __[`Imaging.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Imaging.ipynb)__ for an example). However, in this task, you will create an artistic vignetting effect using an exponential falloff model:

$$ I'(x, y) = I(x, y) \times \exp\left(-\frac{d^2}{\sigma^2}\right) $$

where:
- $I'(x, y)$: the modified pixel intensity.
- $I(x, y)$: the original pixel intensity.
- $d$: the distance from a pixel to the image center.
- $\sigma$: a parameter controlling the vignetting strength.

### Instructions
- **Set** $\sigma = \mathrm{width} / 2$, where $\mathrm{width}$ is the width of the input image.
- **Compute** the distance $d$ from each pixel to the image center (see __[`Imaging.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Imaging.ipynb)__).
- **Apply** the exponential brightness falloff to the image from the previous task.
- **Visualize** the final result with Bokeh and vignetting effects.

### 💻 Code Cell 10

```python
# ---------- YOUR CODE STARTS HERE -----------
# Function to apply vignetting effect
def apply_vignetting(img, sigma):
    """
    Apply vignetting effect to an image using exponential falloff.

    Parameters
    ----------
    img : ndarray
        Input image (H x W x 3).
    sigma : float
        Parameter controlling the strength of vignetting.

    Returns
    -------
    vignetted_img : ndarray
        Image with vignetting effect applied.
    """
    height, width = img.shape[:2]
    center_x, center_y = width // 2, height // 2

    # Create distance map
    y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    d = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    # Apply exponential brightness falloff
    falloff = np.exp(-d ** 2 / sigma ** 2)
    vignetted_img = (img * falloff[..., np.newaxis]).astype(np.uint8)

    return vignetted_img

# Parameters
sigma = image.shape[1] / 2  # Set sigma to half the width of the image

# Apply vignetting effect
vignetted_img = apply_vignetting(bokeh_image, sigma)

# Display the result
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Bokeh Effect")
plt.imshow(cv2.cvtColor(bokeh_image, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Bokeh + Vignetting Effect")
plt.imshow(cv2.cvtColor(vignetted_img, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.tight_layout()
plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 11

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

12 hours (runtime task: 0.4, 2.6, 0.5)

**2. Did you experience any issues or find anything particularly confusing?**

So far not, just need to get familiar on the CV library

### 📝 Markdown Cell 12

# References

`List any references here (optional).`

### 📝 Markdown Cell 13

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A1.ipynb`) into `MV_A1.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 19.01.2025**


## 📁 `A2-Color_Daris_2406778/MV_A2.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 2 – Color

## Personal details

* **Name:** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Introduction

In this assignment, you will explore the concepts of white balance (WB), color transformations, and 2D scatter plots. The assignment is centered around two images from the [**Rendered WB dataset**](https://yorkucvil.github.io/projects/public_html/sRGB_WB_correction/dataset.html). 
The first image, `incorrect_wb.jpg` (Figure 1a), exhibits an incorrect white balance with a noticeable blue color cast. In contrast, the second image, `ideal_wb.jpg` (Figure 1b) has been perfectly white-balanced using a color chart included in the scene. The third image (Figure 1c) shows the result of applying the gray world assumption for white balancing. Your goal is to implement this basic white balancing method. You will also visualize the effect of white balancing using 2D scatter plots in the CIELAB color space.

Before starting, please study [**Lecture 3**](https://moodle.oulu.fi/mod/page/view.php?id=1705511) (Light and color) and the example code in [**`Color.ipynb`**](https://github.com/jtheikkila/mvis/blob/master/jupyter/Color.ipynb).

<img src="fig1.jpg">

Let us start by reading and visualizing the images:

### 💻 Code Cell 2

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Read images
img_ideal = cv2.imread('ideal_wb.jpg')
img_incorrect = cv2.imread('incorrect_wb.jpg')

# Convert from BGR to RGB
img_ideal = cv2.cvtColor(img_ideal, cv2.COLOR_BGR2RGB)
img_incorrect = cv2.cvtColor(img_incorrect, cv2.COLOR_BGR2RGB)

# Display both images side by side
plt.figure(figsize=(10,8))
plt.subplot(1,2,1)
plt.imshow(img_ideal)
plt.title('Ideal white balance')
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(img_incorrect)
plt.title('Incorrect white balance')
plt.axis('off')
plt.show()
```

### 📝 Markdown Cell 3

## Task 1 – White balancing (1.0 point)

White balance (WB) ensures that objects in an image appear with consistent colors, regardless of the lighting conditions. It aims to normalize the effects of illumination, making objects appear as if they were under ideal “white light”. WB is performed by the camera’s integrated signal processor (ISP) on the raw-RGB image. This involves estimating the illumination in the scene and scaling each color channel to normalize the effect of the light source. After this, the ISP applies additional steps, such as a nonlinear gamma correction, to produce the final sRGB image.

In this task, we aim to correct the white balance of the image `incorrect_wb.jpg`. Since the raw-RGB image is not available, we perform the white balancing in the sRGB color space. Your task is to implement a basic WB method based on the **gray world assumption**, which assumes that the average intensity of each color channel (red, green, and blue) in a well-balanced image should be approximately equal. This is typically a reasonable assumption if we have a good distribution of colors in the image.

The aim is to multiply each color channel by a scaling factor to white balance the image. Mathematically, the correction can be defined as
$$
I'_c(x, y) = I_c(x, y) \cdot \frac{\mu}{\mu_c}, \quad \text{for } c \in \{R, G, B\}
$$
where:
- $I_c(x, y)$ is the intensity of channel $c$ at pixel $(x, y)$,
- $I'_c(x, y)$ is the corrected intensity,
- $\mu_c$ is the average intensity of channel $c$,
- $\mu = \frac{1}{3} (\mu_R + \mu_G + \mu_B)$ is the overall average intensity across all channels.

### Instructions
Complete the function `white_balance(img)` shown below. Your implementation should:
1. Compute the average intensity of each color channel $\mu_R$, $\mu_G$, and $\mu_B$.
2. Compute the overall average intensity $\mu$.
3. Calculate the scaling factor for each channel $\frac{\mu}{\mu_c}$.
4. Apply the scaling factors to the corresponding channels.
5. Ensure that all pixel values are clipped to the range [0, 255].

### 💻 Code Cell 4

```python
def white_balance(img):

    img_corrected = img.copy()
    img_corrected = img_corrected.astype(np.float32)

    # ---------- YOUR CODE STARTS HERE -----------
    # Compute the average intensity of each channel
    mu_r = np.mean(img_corrected[:, :, 0])  # Red channel
    mu_g = np.mean(img_corrected[:, :, 1])  # Green channel
    mu_b = np.mean(img_corrected[:, :, 2])  # Blue channel

    # Compute the overall average intensity
    mu = (mu_r + mu_g + mu_b) / 3.0

    # Calculate the scaling factors for each channel
    scale_r = mu / mu_r
    scale_g = mu / mu_g
    scale_b = mu / mu_b

    # Apply the scaling factors to the corresponding channels
    img_corrected[:, :, 0] *= scale_r  # Red channel
    img_corrected[:, :, 1] *= scale_g  # Green channel
    img_corrected[:, :, 2] *= scale_b  # Blue channel    
    # ----------- YOUR CODE ENDS HERE ------------

    # Clip and convert to uint8
    img_corrected = np.clip(img_corrected, 0, 255)
    img_corrected = img_corrected.astype(np.uint8)

    return img_corrected

img_wb = white_balance(img_incorrect)

# Display both images side by side
plt.figure(figsize=(12,8))
plt.subplot(1,2,1)
plt.imshow(img_ideal)
plt.title('Ideal white balance')
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(img_wb)
plt.title('Gray world assumption')
plt.axis('off')
```

### 📝 Markdown Cell 5

## Task 2 – Scatter Plots (1.0 points)

In this task, you will visualize the effect of white balancing on the color distribution of an image in the CIELAB color space. The goal is to compare the 2D scatter plots of the incorrectly white-balanced image `img_incorrect`, gray-world white-balanced image `img_wb`, and ideally white-balanced image `img_ideal`. The 2D scatter plot should depict the distribution of pixel colors in the a* (green-red) and b* (blue-yellow) channels of the CIELAB color space. The example code in [**`Color.ipynb`**](https://github.com/jtheikkila/mvis/blob/master/jupyter/Color.ipynb) will help you to complete this task.

By creating these scatter plots, you will observe how the gray-world white balancing modifies the color distribution. Ideally, the scatter plot for the white-balanced image should closely resemble that of the ideal white-balanced image.

### Instructions
Implement the function `scatter_plot(img_rgb)` to generate 2D scatter plots. 
1. Resize the input image by a factor of 4 to reduce computational overhead.
2. Convert the RGB image to the CIELAB color space using OpenCV.
3. Extract the `a*` and `b*` channels for the 2D scatter plot.
4. Use the RGB colors of the pixels to color the scatter plot markers.
5. Run the code cell to create and compare the scatter plots for `img_incorrect`, `img_ideal`, and `img_wb`. The resulting scatter plots should be similar (not identical) to those shown in Figure 1.

### 💻 Code Cell 6

```python
def scatter_plot(img_rgb):
    
    # ---------- YOUR CODE STARTS HERE -----------
    """
    Generate a 2D scatter plot of pixel colors in the a* (green-red) and b* (blue-yellow) 
    channels of the CIELAB color space.

    Parameters
    ----------
    img_rgb : ndarray
        Input image in RGB format (H x W x 3).
    """
    # Step 1: Resize the image to reduce computational overhead
    scale_factor = 0.25
    img_resized = cv2.resize(img_rgb, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

    # Step 2: Convert the RGB image to the CIELAB color space
    img_lab = cv2.cvtColor(img_resized, cv2.COLOR_RGB2Lab)

    # Step 3: Extract the a* and b* channels
    a_channel = img_lab[:, :, 1].flatten()  # Green-red axis
    b_channel = img_lab[:, :, 2].flatten()  # Blue-yellow axis

    # Step 4: Extract the corresponding RGB colors for scatter plot markers
    colors = img_resized.reshape((-1, 3)) / 255.0  # Normalize RGB to [0, 1] for Matplotlib

    # Step 5: Create the 2D scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(a_channel, b_channel, c=colors, s=1, alpha=0.7)
    plt.title('2D Scatter Plot in CIELAB (a*, b*)')
    plt.xlabel('a* (green-red)')
    plt.ylabel('b* (blue-yellow)')
    plt.grid(True)
    plt.show()    
    # ----------- YOUR CODE ENDS HERE ------------

scatter_plot(img_incorrect)
scatter_plot(img_ideal)
scatter_plot(img_wb)
```

### 📝 Markdown Cell 7

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`2 days`

**2. Did you experience any issues or find anything particularly confusing?**

`No, but need to retrieve the content from slides and read documentations`

### 📝 Markdown Cell 9

# References

`List any references here (optional).`

### 📝 Markdown Cell 10

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A2.ipynb`) into `MV_A2.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 26.01.2025**


## 📁 `A3-Segmentation_Daris_2406778/MV_A3.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 3 - Binary image analysis

## Personal details

* **Name:** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Introduction

In this assignment, you will implement a segmentation method to separate puzzle pieces from the background in an image of a jigsaw puzzle. The segmentation will use Otsu's method to automatically determine a threshold based on the grayscale histogram, dividing the image into dark and light regions. Once segmented, you will apply post-processing techniques to refine the binary image and improve the final result.

<img src="fig1.jpg">

Let us start by displaying the test image and the corresponding grayscale histogram.

### 💻 Code Cell 2

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

img = cv2.imread('puzzle.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.figure(figsize=(15,5))
plt.subplot(121)
plt.title('Image (gray)')
plt.imshow(gray, cmap='gray')
plt.axis('off')
plt.subplot(122)
plt.title('Grayscale histogram')
h = plt.hist(gray.ravel(),256, density=True)
```

### 📝 Markdown Cell 3

Notice that the image is quite noisy. This will make the segmentation more challenging. Before we continue with the segmentation, we want to reduce the noise. We will use the bilateral filter as it has the property of preserving edges and details.

### 💻 Code Cell 4

```python
filt = cv2.bilateralFilter(gray,9,30,30)

plt.figure(figsize=(15,6))
plt.subplot(121)
plt.title('Image (filtered)')
plt.imshow(filt, cmap='gray')
plt.axis('off')
plt.subplot(122)
plt.title('Histogram (filtered)')
h2 = plt.hist(filt.ravel(),256, density=True)
```

### 📝 Markdown Cell 5

## Manual segmentation

Now that we have filtered the image, we continue with the segmentation. A pixel should be classified as foreground if its intensity is less than a threshold value. We can see from the histogram that a good threshold value is somewhere between the peaks (in the valley). Let us pick a threshold $t=125$ and segment the image. We use the OpenCV function __[`threshold`](https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#threshold)__.

### 💻 Code Cell 6

```python
t = 125
ret,thresh = cv2.threshold(filt,t,255,cv2.THRESH_BINARY_INV)

plt.figure(figsize=(15,6))
plt.subplot(121)
plt.imshow(filt, cmap='gray')
plt.title('Image (gray)')
plt.axis('off')
plt.subplot(122)
plt.imshow(thresh, cmap='gray')
plt.title('Thresholded')
plt.axis('off')
```

### 📝 Markdown Cell 7

## Task 1 - Otsu's method (2 points)

In the previous task, we chose the threshold manually. Otsu's method automates this process by looking at the histogram $P(i)$. It choses the threshold $t$ that minimizes the within-group variance defined as

$$
\sigma_w^2(t) = q_1(t) \sigma_1^2(t) + q_2(t) \sigma_2^2(t),\qquad (1)
$$

where $q_1(t)$ and $q_2(t)$ are the sums of histogram values

$$
q_1(t) = \sum_{i=0}^{t-1} P(i) \qquad q_2(t) = \sum_{i=t}^{I-1} P(i) \qquad (2)
$$

and $\sigma_1^2(t)$ and $\sigma_2^2(t)$ are variances

$$
\sigma_1^2(t) = \sum_{i=0}^{t-1} [i - \mu_1(t)]^2 \frac{P(i)}{q_1(t)}  \qquad \sigma_2^2(t) = \sum_{i=t}^{I-1} [i - \mu_2(t)]^2 \frac{P(i)}{q_2(t)}. \qquad (3)
$$

The mean values of the two distributions are

$$
\mu_1(t) = \sum_{i=0}^{t-1} \frac{i P(i)}{q_1(t)}  \qquad \mu_2(t) = \sum_{i=t}^{I-1} \frac{i P(i)}{q_2(t)}. \qquad (4)
$$

To implement Otsu's method, compute $\sigma_w^2(t)$ (Eq.1 ) for all possible threshold values $t$. After that, choose the threshold that gives the smallest within-group variance $\sigma_w^2(t)$.

### Instructions

Complete the function `computeGroupVariance` to calculate the within-group variance $\sigma_w^2(t)$ for a given threshold $t$.

1. Calculate $q_1(t)$ and $q_2(t)$ from the histogram $P(i)$ using Eq. 2.
2. Calculate $\mu_1(t)$, $\mu_2(t)$ (Eq. 4), and the variances $\sigma_1^2(t)$, $\sigma_2^2(t)$ (Eq. 3).
3. Return the within-group variance $\sigma_w^2(t)$ (Eq. 1).

**Tips!** Verify that your implementation works for all $t$ in the range $[0, 255]$. Add a small constant (e.g., $1 \times 10^{-9}$) to $q_1(t)$ and $q_2(t)$ to avoid division by zero. Test the function with $t = 125$. The expected results are $\sigma_w^2(t) \approx 176.7$, $\mu_1 \approx 63.3$, and $\mu_2 \approx 181.9$. Run the provided code to confirm your implementation.

### 💻 Code Cell 8

```python
# INPUTS
# P : Histogram probabilities (255x1 vector)
# t : Threshold value (scalar between [0,255])
#
# OUTPUT
# varw  : Within-group variance (scalar)
#
def computeGroupVariance(P, t):
    
    # The following line can be removed
    varw = 0
      
    # ---------- YOUR CODE STARTS HERE -----------
    
    # Compute q1 and q2 for a given threshold (Eq. 2)
    q1 = np.sum(P[:t])  # Sum of histogram values from 0 to t-1
    q2 = np.sum(P[t:])  # Sum of histogram values from t to 255
    # Add small constants to avoid division by zero
    q1 = max(q1, 1e-9)
    q2 = max(q2, 1e-9)

    # Compute mean values (Eq. 4)
    μ1 = np.sum(np.arange(0, t) * P[:t]) / q1  # Weighted average for class 1
    μ2 = np.sum(np.arange(t, len(P)) * P[t:]) / q2  # Weighted average for class 2
    
    # Compute variances (Eq. 3)
    σ1_sq = np.sum(((np.arange(0, t) - μ1)**2) * P[:t]) / q1
    σ2_sq = np.sum(((np.arange(t, len(P)) - μ2)**2) * P[t:]) / q2

    # Compute within-group variance (Eq. 1)
    varw = q1 * σ1_sq + q2 * σ2_sq

    # ----------- YOUR CODE ENDS HERE ------------
    
    return varw


bins = np.arange(0,256,1)
P = np.histogram(filt.ravel(),bins,density=True)[0]

t = 125 # Threshold
varw = computeGroupVariance(P,t)
print("Within-group variance = %f (threshold %d)" %(varw,t))
```

### 💻 Code Cell 9

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 10

### Segmentation

Next we are going to use the function to compute within-group variances for all thresholds. Then, we will choose the threshold that gives the smallest within-group variance. The threshold found using Otsu's method should be close to the threshold we picked manually.

### 💻 Code Cell 11

```python
thresholds = np.arange(256)
varws = np.zeros(256, dtype=np.float32)

for idx, t in enumerate(thresholds):
    varw = computeGroupVariance(P,t)
    varws[idx] = varw
    
t = np.argmin(varws)
print("Threshold = %d (within-group variance %f)" %(t,varws[t]))

ret, otsu = cv2.threshold(filt,t,255,cv2.THRESH_BINARY_INV)
plt.figure(figsize=(15,6))
plt.subplot(121)
plt.imshow(filt, cmap='gray')
plt.title('Image (gray)')
plt.axis('off')
plt.subplot(122)
plt.imshow(otsu, cmap='gray')
plt.title("Otsu's method")
plt.axis('off')
```

### 📝 Markdown Cell 12

## Post-processing (optional)

The remaining steps of this notebook are optional and focus on refining the segmentation result. At this stage, the segmentation should be fairly accurate, but closer inspection reveals small holes, noise, and unwanted objects in the segmented image. To address these issues, we will refine the segmentation using morphological operations. 

**Morphological operations**

The following code performs morphological closing to fill small holes in the segmented regions. This operation involves dilation followed by erosion and is effective in closing gaps within objects. Then, we will apply morphological opening to remove small noise and isolated regions. This operation consists of erosion followed by dilation.

While these steps improve the segmentation, some larger unwanted objects remain. These will be addressed in the following sections.

### 💻 Code Cell 13

```python
sel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
closing = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, sel1)

plt.figure(figsize=(8,8))
plt.imshow(closing, cmap='gray')
plt.title('Morphological closing')
plt.axis('off')

sel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, sel2)

plt.figure(figsize=(8,8))
plt.imshow(opening, cmap='gray')
plt.title('Morphological opening')
plt.axis('off')
```

### 📝 Markdown Cell 14

**Connected component labeling**

The following code gives an unique label to each connected component in the binary image. It also extracts the contours of the objects. Notice that we still have more objects than we have puzzle pieces.

### 💻 Code Cell 15

```python
ret, labels = cv2.connectedComponents(opening)
cnt,_ = cv2.findContours(opening, 1, 1)
# _,cnt,_ = cv2.findContours(opening, 1, 1) # For older OpenCV versions

plt.figure(figsize=(15,5))
plt.subplot(121)
plt.imshow(labels)
plt.title('Labeled image')
plt.axis('off')
plt.subplot(122)
for i in range(len(cnt)):
    plt.plot(cnt[i][:,0,0],cnt[i][:,0,1])
plt.gca().invert_yaxis()
plt.title('Contours')
plt.axis('equal')
```

### 📝 Markdown Cell 16

**Removing small ojects**

As a final step, we remove those unwanted round objects. Luckily, they are much smaller than the puzzle pieces. We will compute the area of each contour using __[`contourArea`](https://docs.opencv.org/4.2.0/d3/dc0/group\_\_imgproc\_\_shape.html#ga2c759ed9f497d4a618048a2f56dc97f1)__ and keep objects, which area is more than 500. In the end, there are 36 objects in total (each jigsaw piece represents an object).

### 💻 Code Cell 17

```python
# This will be the final result (binary image)
final = np.zeros_like(otsu)

for i in range(len(cnt)):
    area = cv2.contourArea(cnt[i])
    if (area > 500):
        cv2.drawContours(final, cnt, i, 255, thickness=-1)

ret, labels_final = cv2.connectedComponents(final)
cnt_final,_ = cv2.findContours(final, 1, 1)
#_,cnt_final,_ = cv2.findContours(final, 1, 1) # For older OpenCV versions

plt.figure(figsize=(15,5))
plt.subplot(121)
plt.imshow(labels_final)
plt.title('Labeled image')
plt.title("Labeled image (objects = %d)" %len(cnt_final))
plt.axis('off')
plt.subplot(122)
plt.imshow(final, cmap='gray')
plt.title('Final segmentation')
plt.axis('off')
```

### 📝 Markdown Cell 18

**More advanced methods**

Our test image was relatively easy to segment. This was mainly because the background was much brighter compared to the puzzle pieces. If the background was different color, the segmentation might not work anymore. In such case, one could utilize some color-based segmentation method. If the puzzle pieces were touching each other, it would cause another challenge. We might be able to separate the pieces from the background but the individual pieces would be difficult to extract (connected component labeling) as the segmented regions might be overlapping. The __[`watershed`](https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#watershed)__ algorithm is a classical method that is often used to segment overlapping objects. Furthermore, OpenCV also offers __[`grabCut`](https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#grabcut)__ segmentation method, which is based on graph cuts.

### 📝 Markdown Cell 19

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`3 hours`

**2. Did you experience any issues or find anything particularly confusing?**

`No, so far`

### 📝 Markdown Cell 20

# References
`List any references here (optional).`

### 📝 Markdown Cell 21

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A3.ipynb`) into `MV_A3.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 2.2.2025**


## 📁 `A4-Texture_Daris_2406778/MV_A4.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 4 - Texture

## Personal details

* **Name(s):** `PUT YOUR NAME(S) HERE.`
* **Student ID(s):** `PUT YOUR STUDENT ID(S) HERE.`

## Introduction

This assignment explores the use of filter banks and local binary patterns (LBP) for face recognition. There are a variety of use-cases for face recognition, including identity verification, human-computer interaction, desktop login and parental control. The goal is to create a classifier that can determine to which of the training classes a given face belongs (Figure 1).

![figure1.jpg](attachment:figure1.jpg)

The folder `images/train/` contains five different face images that will be used to train the classifier. We will first visualize these faces and compute their grayscale histograms, storing them in a $5 \times 256$ matrix $H$ for later use. later use.

### 💻 Code Cell 2

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
%matplotlib inline

# Get file paths to training images
fnames_train = sorted(glob.glob('images/train/*.jpg'))

# Number of different training faces
N = len(fnames_train) 

# We will store grayscale histograms
H = np.zeros((N,256),dtype=float)

plt.figure(figsize=(12,5))

for i in range(0,N):
    
    img = cv2.imread(fnames_train[i])
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Display training faces (class labels: 0,1,2,3,4)
    plt.subplot(1,N,i+1)
    plt.imshow(rgb)
    plt.title('Face %d' %(i+1))
    plt.axis('off')
    
    # Compute grayscale histogram for later use
    H[i,:] = np.histogram(gray.ravel(),256,density=True)[0]
```

### 📝 Markdown Cell 3

The folder `images/test/` contains 50 face images that will be used to test the classifier. Let's display the first five test images.

### 💻 Code Cell 4

```python
# Get file paths to test images
fnames_test = sorted(glob.glob('images/test/*.jpg'))

plt.figure(figsize=(12,5))

for i in range(0,5):
    
    img = cv2.imread(fnames_test[i])
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Display five test faces
    plt.subplot(1,5,i+1)
    plt.imshow(rgb)
    plt.title('Test image %d' %(i+1))
    plt.axis('off')
```

### 📝 Markdown Cell 5

All of these faces correspond to Face 1. Notice that the face color varies greatly depending on the lighting conditions. Instead of relying on the color information, we will perform the classification using grayscale and texture histograms. 

## Histogram-based distance

To classify a face, we need to determine the distance to each of the training histograms stored in `H`. Let's pick one test image and compute its grayscale histogram `h`.

### 💻 Code Cell 6

```python
img = cv2.imread(fnames_test[4])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.figure(figsize=(10,4))
plt.subplot(121)
plt.imshow(gray,cmap='gray')
plt.title('Test image 5 (gray)')
plt.axis('off')
plt.subplot(122)
h = plt.hist(gray.ravel(),256,density=True)[0]
plt.title('Grayscale histogram')
```

### 📝 Markdown Cell 7

**Computing $L_1$ distances**

To measure the similarity between two histograms, $H_i$ and $h$, we can use various distance metrics. In this assignment, we will use the $L_1$ distance, defined as:

$$
L_1(H_i,h) = \sum_{m=1}^{K} |H_i(m) - h(m)|, \qquad \qquad (1)
$$

where $K$ is the number of bins. 

The function `histogramDistance` computes the $L_1$ distance between a test histogram `h` and each training histogram `H[i, :]`. The test face will be classified based on these histogram distances.

### 💻 Code Cell 8

```python
# INPUT   
# H : Training histograms (5xK matrix)
# h : Test histogram (1xK vector)
#
# OUTPUT  
# dists: L1 distances between a test histogram
#        and each training histogram (5x1 vector)
#
def histogramDistances(H,h):
    dists = np.abs(H - h)
    dists = np.sum(dists,axis=1)
    return dists

# Compute L1 distances
dists = histogramDistances(H,h)
print('L1 distances:')
print(dists)

# Predict class (face)
pred = np.argmin(dists)
dist = dists[pred]
print('\nPredicted face: %d (dist = %f)' %(pred+1,dist))
```

### 📝 Markdown Cell 9

The first training histogram is the most similar to `h`, leading us to conclude that the given face corresponds to Face 1. While the classification is correct, the distance to the third training histogram (Face 3) was also small, meaning the face was close to being misclassified.

### 📝 Markdown Cell 10

## Task 1 - Confusion matrix (0.50 points)

In the previous section, we classified a single face by comparing grayscale histograms. Next, we will classify all test images. We will also build a confusion matrix $C$ to report the classification results. In the confusion matrix, the entry $C(i,j)$ shows how many times a face was classified as class $j$ when the true class was $i$. Run the following code cell and answer the questions below.

### 💻 Code Cell 11

```python
# Confusion matrix
C = np.zeros((N,N),dtype=int)

for fname in fnames_test:

    # Extract the true class from the file name
    i = int(fname[-8]) - 1
    
    # Read test face
    img = cv2.imread(fname)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute histogram
    h = np.histogram(gray.ravel(),256,density=True)[0]
    
    # Compute L1 distances
    dists = histogramDistances(H,h)
    
    # Predict class (face)
    j = np.argmin(dists)
    
    # Record the result to the confusion matrix
    C[i,j] = C[i,j] + 1
    
print('Confusion matrix:')
print(C)

res = np.trace(C) / np.sum(C)
print('Score =', res)
```

### 📝 Markdown Cell 12

**Which one of the faces was easiest to classify based on the confusion matrix? What two classes were most often confused?**

### 📝 Markdown Cell 13

Face 3 (8 correct), as it's the highest correct classification. Also two classed with the most often confused one are Face 5 → Face 1: 6 instances misclassified, and Face 4 → Face 3: 5 instances misclassified, which is defined from max(non-diagonal)

### 📝 Markdown Cell 14

## Task 2 - Face recognition using filter banks  (1.0 points)

Face classification using grayscale histograms performed poorly. To improve accuracy, we will use filter banks. First, study the filter banks from the example notebook __[`Texture.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Texture.ipynb)__. 

### Instructions
Complete the function `histogramGabor`, which should follow these steps:
1. Define four Gabor filters (code provided).
2. Apply filters to the image. Normalize the image to range [0, 1] before using `cv2.filter2D`.
3. Binarize the filtered images. Pixels greater than 0 are set to 1, and others are set to 0.
4. Construct a texture map by summing the binary images with different weights (1, 2, 4, 8).
5. Calculate a histogram with 16 bins from the texture map.

After you have completed the function, proceed to the next step for testing.

### 💻 Code Cell 15

```python
# INPUT   
# img : Grayscale image
#
# OUTPUT  
# h : Histogram (1x16 vector)
#
def histogramGabor(img):

    kern1 = cv2.getGaborKernel((11, 11),3,np.pi/4,11,1)
    kern2 = cv2.getGaborKernel((11, 11),3,-np.pi/4,11,1)
    kern3 = cv2.getGaborKernel((11, 11),2,np.pi/4,5,1)
    kern4 = cv2.getGaborKernel((11, 11),2,-np.pi/4,5,1)
    
    # ---------- YOUR CODE STARTS HERE -----------
    filters = [kern1, kern2, kern3, kern4]
    img = img / 255.0
    binary_maps = [(cv2.filter2D(img, cv2.CV_32F, k) > 0).astype(np.uint8) for k in filters]
    texture_map = sum(b * (2**i) for i, b in enumerate(binary_maps))
    h = np.histogram(texture_map.ravel(), bins=16, range=(0, 16), density=True)[0]    
    # ----------- YOUR CODE ENDS HERE ------------
    
    return h
```

### 📝 Markdown Cell 16

Next, we will repeat the classification experiment. The only difference is that we use the histograms from `histogramGabor` instead of grayscale histograms. Run the following code cell. The classification score should improve from 0.4 to 0.82.

### 💻 Code Cell 17

```python
# Compute histograms of training faces
H_gabor = np.zeros((N,16),dtype=float)

for i in range(0,N):
    
    img = cv2.imread(fnames_train[i])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H_gabor[i,:] = histogramGabor(gray)
    
# Confusion matrix
C = np.zeros((N,N),dtype=int)

for fname in fnames_test:

    # Extract the true class from the file name
    i = int(fname[-8]) - 1
    
    # Read test face
    img = cv2.imread(fname)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute histogram
    h = histogramGabor(gray)
    
    # Compute L1 distances
    dists = histogramDistances(H_gabor,h)
    
    # Predict class (face)
    j = np.argmin(dists)
    
    # Record the result to the confusion matrix
    C[i,j] = C[i,j] + 1
    
print('Confusion matrix:')
print(C)

res = np.trace(C) / np.sum(C)
print('Score =', res)
```

### 💻 Code Cell 18

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 19

## Face recognition using LBP histograms

Local Binary Patters (LBP) have been successfully applied to many computer vision problems. One reason they are so popular is that they are very fast and easy to compute. The LBP concept was originally conceived here in the University of Oulu. Computing the LBP for a pixel involves the 8 neighbours around it. Consider the neighbourhood around pixel $x$ as presented in Figure 2.

![figure2.jpg](attachment:figure2.jpg)

We threshold the values using $x$ as a threshold $(a_{th} = 1$ if $a \geq x)$, and then assign a bit to each neighbour. The final LBP for $x$ is

$$
L_x = 2^0a_{th} + 2^1b_{th} + 2^2c_{th} + 2^3d_{th} + 2^4e_{th} + 2^5f_{th} + 2^6g_{th} + 2^7h_{th},
$$

which is an 8 bit number. The LBP transform gives us a value for each pixel. To characterize a face we can compute the histogram of LBP values. This gives us a 1 x 256 feature vector that describes the face in a given image or patch. The following function computes the LBP transform of a given image. The function also returns the LBP histogram.

### 💻 Code Cell 20

```python
# INPUT   
# img : Input image (grayscale)
#
# OUTPUT  
# hist : LBP histogram (1x256 vector)
# out  : LBP transform of the input image
#
def histogramLBP(img):
    m,n = img.shape
    out = np.zeros((m-2, n-2, 8), dtype=np.uint8)
    disp = ((-1, -1),(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    center = img[1:-1, 1:-1]
    for i, d in enumerate(disp):
        out[:,:,i] = img[d[0] + 1 : d[0] + m - 1, d[1] + 1 : d[1] + n - 1] >= center
        out[:,:,i] = 2**i * out[:,:,i]
    out = np.sum(out, axis = 2)
    hist = np.histogram(out, 256, density=True)[0]
    return hist, out

img = cv2.imread(fnames_test[4])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h_lbp, img_lbp = histogramLBP(gray)

plt.figure(figsize=(10,4))
plt.subplot(121)
plt.imshow(gray,cmap='gray')
plt.title('Test image 5')
plt.axis('off')
plt.subplot(122)
plt.imshow(img_lbp)
plt.title('LBP transform')
plt.axis('off')
```

### 📝 Markdown Cell 21

Let's classify the test faces using LBP histograms and report the classification results.

### 💻 Code Cell 22

```python
# Compute histograms of training faces
H_lbp = np.zeros((N,256),dtype=float)

for i in range(0,N):
    
    img = cv2.imread(fnames_train[i])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H_lbp[i,:] = histogramLBP(gray)[0]
    
# Confusion matrix
C = np.zeros((N,N),dtype=int)

for fname in fnames_test:

    # Extract the true class from the file name
    i = int(fname[-8]) - 1
    
    # Read test face
    img = cv2.imread(fname)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute histogram
    h = histogramLBP(gray)[0]
    
    # Compute L1 distances
    dists = histogramDistances(H_lbp,h)
    
    # Predict class (face)
    j = np.argmin(dists)
    
    # Record the result to the confusion matrix
    C[i,j] = C[i,j] + 1
    
print('Confusion matrix:')
print(C)

res = np.trace(C) / np.sum(C)
print('Score =', res)
```

### 📝 Markdown Cell 23

Although the LBP-based approach worked better compared to grayscale histograms, the classification results are still far from perfect.

### 📝 Markdown Cell 24

## Task 3 - Patch-based LBP (0.50 points)

Previously, we computed a single LBP histogram for the whole image. An alternative approach is to divide the image into smaller patches (32 x 32 pixels), compute an LBP histogram of each patch, and concatenate them into a single histogram. Since the image size is 256 x 256 pixels, this gives us exactly 64 patches as shown in Figure 3.

![figure3.jpg](attachment:figure3.jpg)

### Instructions

Complete the function `histogramPatchLBP`. You should compute the LBP histogram of each patch and concatenate them into a single histogram. The length of the histogram should be 16384 (64 x 256). Note that you can reuse the code from the function `histogramLBP`.

After you have completed the function, proceed to the next step for testing.

### 💻 Code Cell 25

```python
# INPUT   
# img   : Input image (grayscale)
# psize : Patch size (32 pixels)
#
# OUTPUT  
# hist : LBP histogram formed by concatenating
#        the histograms of individual patches (1x16384 vector)
#
def histogramPatchLBP(img, psize=32):
    
    # ---------- YOUR CODE STARTS HERE -----------
    m, n = img.shape
    hist = np.zeros((64, 256), dtype=float)
    idx = 0
    
    for i in range(0, m, psize):
        for j in range(0, n, psize):
            patch = img[i:i+psize, j:j+psize]
            if patch.shape == (psize, psize):
                hist[idx, :] = histogramLBP(patch)[0]
                idx += 1
    
    hist = hist.flatten()
    
    # ----------- YOUR CODE ENDS HERE ------------
    
    return hist
```

### 📝 Markdown Cell 26

Again, we repeat the classification experiment. The process of detecting faces is the same as before: (1) Compute patch-based LBP histograms of the training images `H_patch`. (2) Compute histogram distances between the training histograms `H_patch`and the test histogram `h_patch`. Your implementation should be correct if you got a perfect score of 1.0 (or close).

### 💻 Code Cell 27

```python
# Compute patch-based LBP histograms of training faces
H_patch = np.zeros((N,64*256),dtype=float)

for i in range(0,N):
    
    img = cv2.imread(fnames_train[i])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H_patch[i,:] = histogramPatchLBP(gray)
    
# Confusion matrix
C = np.zeros((N,N),dtype=int)

for fname in fnames_test:

    # Extract the true class from the file name
    i = int(fname[-8]) - 1
    
    # Read test face
    img = cv2.imread(fname)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute histogram
    h = histogramPatchLBP(gray)
    
    # Compute L1 distances
    dists = histogramDistances(H_patch,h)
    
    # Predict class (face)
    j = np.argmin(dists)
    
    # Record the result to the confusion matrix
    C[i,j] = C[i,j] + 1
    
print('Confusion matrix:')
print(C)

res = np.trace(C) / np.sum(C)
print('Score =', res)
```

### 💻 Code Cell 28

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 29

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`REPLACE THIS TEXT WITH YOUR ANSWER.`

**2. Did you experience any issues or find anything particularly confusing?**

`REPLACE THIS TEXT WITH YOUR ANSWER.`

### 📝 Markdown Cell 30

# References

`List any references here (optional).`

### 📝 Markdown Cell 31

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A4.ipynb`) into `MV_A4.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 09.02.2025**


## 📁 `A5-Recognition_Daris_2406778/MV_A5.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 5 - Recognition

## Personal details

* **Name(s):** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Introduction

In this assignment, your goal is to classify apples and pears using shape and color features. The figure below shows examples from both classes. There is a slight color difference between the apples and pears. Therefore, we will use the hue of the fruit as our first feature $x_1$. Depending on the viewpoint, the apples are generally more round compared to pears. To represent the roundness, we will use the eccentricity as our second feature $x_2$. The eccentricity will vary between 0 and 1 (the eccentricity of a circe is zero). The features can be combined into a feature vector $\mathbf{x} = [x_1, x_2]^\top$.

![classes.png](attachment:classes.png)

We can utilize techniques from the previous assignments to compute features (such as the eccentricity and hue) from the images. However, this assignment focuses on the classification so the features and class labels have been precomputed and saved to `class_data.npz` file. Let's first read and visualize the samples.

**Note!** The package *scikit-learn* is needed. If you encounter an error, type `pip install -U scikit-learn` to the terminal.

### 💻 Code Cell 2

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

from sklearn.neighbors import NearestCentroid

# Load data
data=np.load('class_data.npz')
X_train = data['arr_0'] # Nx2 matrix
y_train = data['arr_1'] # 1xN vector
X_test = data['arr_2']  # Mx2 matrix
y_test = data['arr_3']  # 1xM vector

# Print few feature vectors and 
# corresponding true classes
print(X_train[:4,:])
print(y_train[:4])

# Visualize training data
yp = y_train == 'pear'
ya = y_train == 'apple'
X1 = X_train[yp,:]
X2 = X_train[ya,:]

fig, ax = plt.subplots()
ax.scatter(X1[:,0], X1[:,1], c='r', label='pear')
ax.scatter(X2[:,0], X2[:,1], c='b', label='apple')
ax.set_xlabel('$x_1$ (hue)')
ax.set_ylabel('$x_2$ (eccentricity)')
ax.set_title('Training data')
ax.legend()
```

### 📝 Markdown Cell 3

## Task 1 - Nearest centroid classifier (0.5 points)

Complete the following code cell to classify the test samples using the __[`nearest centroid classifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html)__.  See the example notebook __[`Recognition.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Recognition.ipynb)__ before continuing.

**Instructions**
1. Train the classifier using the training samples `X_train` and `y_train` with the `fit()` method. Use **Euclidean distance** as the distance metric.
2. Evaluate the performance of the classifier using the `score()` method on the independent test data `X_test` and true labels `y_test`
3. Print the mean accuracy of the classifier. Your code should be correct if the mean accuracy is 0.70.

### 💻 Code Cell 4

```python
# ---------- YOUR CODE STARTS HERE -----------
# Train the Nearest Centroid Classifier
clf = NearestCentroid(metric='euclidean')
clf.fit(X_train, y_train)

# Evaluate classifier
accuracy = clf.score(X_test, y_test)
print(f"Nearest Centroid Classifier Accuracy: {accuracy:.2f}")
# ----------- YOUR CODE ENDS HERE ------------
```

### 💻 Code Cell 5

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 6

## Task 2 - Visualization (0.5 points)

Complete the following code cell to visualize the test data (`X_test`, `y_test`). Your plot should:
1. Display test samples (`X_test`, `y_test`) using different colors (same way we plotted the training data).
2. Display the **class centroids** and the **decision boundary** between the classes.

Refer to the sample code in __[`Recognition.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/Recognition.ipynb)__ for guidance. It is optional to display the true positives (TP), true negatives (TN), false positives (FP) and false negatives (FN) as in the sample code. Note that Euclidean distance does not work well in this case. Therefore, the decision boundary will appear as a vertical line.

### 💻 Code Cell 7

```python
# ---------- YOUR CODE STARTS HERE -----------
# Visualize test data classification
y_pred = clf.predict(X_test)

yp_test = y_test == 'pear'
ya_test = y_test == 'apple'
X1_test = X_test[yp_test, :]
X2_test = X_test[ya_test, :]

# Plot test data
fig, ax = plt.subplots()
ax.scatter(X1_test[:, 0], X1_test[:, 1], c='r', label='Pear (Test)')
ax.scatter(X2_test[:, 0], X2_test[:, 1], c='b', label='Apple (Test)')

# Plot class centroids
ax.scatter(clf.centroids_[:, 0], clf.centroids_[:, 1], c='black', marker='x', label='Centroids')

# Plot decision boundary (vertical line at centroid midpoint)
x_boundary = (clf.centroids_[0, 0] + clf.centroids_[1, 0]) / 2
ax.axvline(x=x_boundary, color='k', linestyle='--', label='Decision Boundary')

ax.set_xlabel('$x_1$ (hue)')
ax.set_ylabel('$x_2$ (eccentricity)')
ax.set_title('Test Data Classification')
ax.legend()
plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 8

## Classification using Mahalanobis distance

Notice that features (eccentricity and hue) are not measured in the same units. The drawback with Euclidean distance is that it gives equal weights to all dimensions. The clusters that we are trying to model are not spherical so the Euclidean distance does not give an accurate distance. We can model both clusters as multivariate Gaussian distributions with a mean $\mu$ and covariance matrix $\sum$. This implicitly represents the region as an ellipsoid centered at $\mu$ with the axes aligned with the eigenvectors of $\sum$.

The Mahalanobis distance provides an adequate distance in this case, weighting each dimension according to the observed variance and taking into account the covariance of different dimensions. The equation for the Mahalanobis distance is:

$$
d_M^i = \sqrt{(\mathbf{x}-\mathbf{\mu}_i)^\top \sum{}{}_{i}^{-1} (\mathbf{x}-\mathbf{\mu}_i)} \qquad \qquad (1).
$$

In this case, the inverse covariance matrix $\sum^{-1}$ is a 2 x 2 matrix as we have two features.

### Task 3 - Means and covariances (0.25 points)

Complete the following code cell to compute the **means** ($\mathbf{\mu}_1$ and $\mathbf{\mu}_2$) and **covariance matrices** ($\Sigma_1$ and $\Sigma_2$) for the training samples `X1` and `X2`.

**Instructions**
1. Use the function [`np.mean`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html) to compute the centroids of `X1` and `X2`. Name them `mean1` and `mean2`.
2. Use the function [`np.cov`](https://numpy.org/doc/stable/reference/generated/numpy.cov.html) to compute the covariance matrices of `X1` and `X2`. Name them `cov1` and `cov2`. These should be 2 x 2 matrices (see the *rowvar* parameter).
3. Print the means and covariance matrices.

### 💻 Code Cell 9

```python
# ---------- YOUR CODE STARTS HERE -----------

# Compute means (mean1, mean2)
mean1 = np.mean(X1, axis=0)
mean2 = np.mean(X2, axis=0)

# Compute covariance matrices (cov1, cov2)
cov1 = np.cov(X1.T)
cov2 = np.cov(X2.T)

# Display results
print("Mean (Pear):", mean1)
print("Mean (Apple):", mean2)
print("\nCovariance Matrix (Pear):\n", cov1)
print("\nCovariance Matrix (Apple):\n", cov2)
# ----------- YOUR CODE ENDS HERE ------------
```

### 💻 Code Cell 10

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 11

### Task 4 - Mahalanobis distances (0.75 points)

Complete the function `mahalanobisDistances` to compute the Mahalanobis distances between the test samples `X` and a class centroid `mean` using Equation 1. Use __[`np.linalg.inv`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html)__ to compute the inverse of the covariance matrix `cov`.

After completing the function, run the code cell. This will calculate the distances for both class centroids (`mean1` and `mean2`), classify the test samples, and compute the mean accuracy. Your code is likely correct if the mean accuracy is 0.92.

### 💻 Code Cell 12

```python
# INPUT   
# X    : Feature vectors of the test samples (Mx2 matrix)
# mean : The mean feature (centroid) of the class (1x2 vector)
# cov  : Covariance matrix of the class (2x2 matrix)
#
# OUTPUT  
# dists : Mahalanobis distances between the test samples 'X'
#         and the centroid 'mean' (1xM vector)
#

from scipy.spatial.distance import mahalanobis

def mahalanobisDistances(X, mean, cov):
    
    # ---------- YOUR CODE STARTS HERE -----------
    cov_inv = np.linalg.inv(cov)  # Compute inverse covariance matrix
    dists = np.array([mahalanobis(x, mean, cov_inv) for x in X])  # Compute distance for each sample
    # ----------- YOUR CODE ENDS HERE ------------

    return dists

# Calculate the distances
D1 = mahalanobisDistances(X_test, mean1, cov1)
D2 = mahalanobisDistances(X_test, mean2, cov2)

# Produce class labels based on the distances
idx = D1 < D2
y_pred = np.array(D1.shape[0]*['apple'])
y_pred[idx == True] = 'pear'

# Compute mean accuracy
score = np.sum(y_test == y_pred) / y_test.shape[0]
print('Score = %f' %score)
```

### 💻 Code Cell 13

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 14

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`6 hours.`

**2. Did you experience any issues or find anything particularly confusing?**

`No, I'm trying to implement the Exercise 4 slides, as the logical process `

### 📝 Markdown Cell 15

# References

`List any references here (optional).`

### 📝 Markdown Cell 16

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A5.ipynb`) into `MV_A5.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 16.02.2025**


## 📁 `A6-Motion/MV_A6.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 6 - Motion

## Personal details

* **Name(s):** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Background subtraction

In this assignment, we use a background subtraction technique to detect moving objects in a video. We use a dynamic background model that is continuously updated and threshold every frame of the video to detect new objects.

![detection.jpg](attachment:detection.jpg)

Our approach follows the method described in the lecture notes and works with grayscale images. The background is a dynamic model where each pixel is described by a Gaussian (i.e. mean and variance). The background model for each pixel is updated after each frame according to the equations:

$$
\mu_{t+1} = \alpha \mu_t + (1-\alpha) z_{t+1} \qquad \qquad \qquad \qquad \qquad \qquad (1)
$$
$$
\sigma_{t+1}^2 = \alpha [\sigma_t^2 + (\mu_{t+1} - \mu_t)^2] + (1-\alpha)(z_{t+1} - \mu_{t+1})^2 \qquad \ \   (2)
$$

where $\alpha$ controls the rate of adaptation $(0 < \alpha < 1)$ and $z_{t+1}$ is the current pixel value. With this model we can decide whether a pixel contains an object of interest with the formula

$$
| z_t - \mu_t | > K \cdot \, \text{max}(\sigma_t, \sigma_{rcam}) \qquad \qquad (3)
$$

where $\sigma_{rcam}$ represents the standard deviation of the camera noise. Before proceeding, let’s display a few frames from the test video.

### 💻 Code Cell 2

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

cap = cv2.VideoCapture('test.mp4')

# Read the first frame
ret, img0_color = cap.read()

# We work with grayscale images (range [0,1])
img0 = cv2.cvtColor(img0_color, cv2.COLOR_BGR2GRAY)/255
height, width = img0.shape

# Display and store a few frames
plt.figure(figsize=(15,10))
images = np.zeros((height,width,9), dtype=np.float32)

for i in range(9):
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 20*i)
    ret, img_color = cap.read()
    if ret == False:
        break
        
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)/255
    images[:,:,i] = img
    
    plt.subplot(3,3,i+1)
    plt.imshow(img, cmap='gray')
    plt.title('Frame %d' %(20*i))
    plt.axis('off')

cap.release()
```

### 📝 Markdown Cell 3

## Initialization

Next we initialize the mean and variance images. For the mean image, we compute the median of the frames. This will give us the background without the moving objects. The camera noise can be estimated from any two frames. Here we assume that $\sigma_{rcam} = 0.005$.

### 💻 Code Cell 4

```python
sigma_cam = 0.005
mean_img = np.median(images, axis=2)
var_img = sigma_cam * np.ones_like(img0)

# The current state is stored in a dictionary
state_initial = {"alpha": 0.99,
                 "sigma_cam": sigma_cam,
                 "mean_img": mean_img,
                 "var_img": var_img,
                 "K" : 2.0}

# You can access the values by
alpha = state_initial["alpha"] # Or: state_initial.get("alpha")

# And you can change the values by
state_initial["alpha"] = 0.99

# Show the mean image
plt.figure(figsize=(8,5))
plt.imshow(mean_img, cmap='gray')
plt.title('Mean image (initial)')
plt.axis('off')
```

### 📝 Markdown Cell 5

## Task 1 - Update background model (1.0 points)

Implement the function `updateBackgroundModel` to update the mean and variance of the dynamic background model. The mean background image `state["mean_img"]` should be updated using Equation 1, and the variance `state["var_img"]` should be updated using Equation 2. Compute $\mu_{t+1}$ first, as Equation 2 requires both the previous mean $\mu_t$ and the updated mean $\mu_{t+1}$.

### Instructions
- Use **Equation 1** to update `state["mean_img"]`.
- Use **Equation 2** to update `state["var_img"]`.
- There is no need to use for-loops. Approximately 2-5 lines of code required.

### 💻 Code Cell 6

```python
# INPUT   
# img   : The current grayscale image
# state : The current state (as define before)
#
# OUTPUT  
# state : Updated state, where state["mean_img"] and
#         state["var_img"] have been updated.
#
def updateBackgroundModel(img, state):
    
    # ---------- YOUR CODE STARTS HERE -----------
    """
    Update the mean and variance of the background model.
    
    Parameters:
        img (numpy array): The current grayscale image.
        state (dict): The current state containing "mean_img" and "var_img".
    
    Returns:
        state (dict): Updated state dictionary.
    """
    # Extract required parameters
    alpha = state["alpha"]
    mean_t = state["mean_img"]
    var_t = state["var_img"]

    # Compute updated mean (μ_t+1)
    mean_t1 = alpha * mean_t + (1 - alpha) * img
    
    # Compute updated variance (σ²_t+1)
    var_t1 = alpha * var_t + (1 - alpha) * (mean_t1 - img) ** 2
    
    # Update state dictionary
    state["mean_img"] = mean_t1
    state["var_img"] = var_t1        
    # ----------- YOUR CODE ENDS HERE ------------
    return state


# A sanity check. You are probably on the right track
# if the following prints approx. 0.505294 and 0.004984
state_test = state_initial.copy()
state_test = updateBackgroundModel(img0, state_test)
print(state_test["mean_img"][100,100])
print(state_test["var_img"][100,100])
```

### 💻 Code Cell 7

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 8

## Task 2 - Threshold frame (1.0 points)

Implement the function `thresholdFrame` to detect new objects in a frame using background subtraction. The function should apply Equation 3, which classifies pixels as foreground if they deviate significantly from the background model.

### Instructions
- Compute **$\sigma_t$** as the square root of the variance (`state["var_img"]`).
- Use **Equation 3** to determine which pixels belong to moving objects.
- Utilize the element-wise maximum operation __[`np.maximum`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.maximum.html)__.
- There is no need to use for-loops. Only a few lines of code required.

### 💻 Code Cell 9

```python
# INPUT   
# img   : The current grayscale image
# state : The current state
#
# OUTPUT  
# thresh : Thresholded image
#
def thresholdFrame(img, state):
    
    # ---------- YOUR CODE STARTS HERE -----------
    """
    Detects moving objects using background subtraction.
    
    Parameters:
        img (numpy array): The current grayscale image.
        state (dict): The current state containing "mean_img", "var_img", and "K".
    
    Returns:
        thresh (numpy array): Binary image where foreground pixels are 1 and background pixels are 0.
    """
    # Extract background mean and variance
    mean_t = state["mean_img"]
    var_t = state["var_img"]
    K = state["K"]

    # Compute standard deviation (σ_t)
    sigma_t = np.sqrt(var_t)

    # Apply thresholding using Equation 3
    thresh = np.abs(img - mean_t) > K * sigma_t

    # Convert to binary format (0 or 1)
    thresh = thresh.astype(np.uint8)    
    # ----------- YOUR CODE ENDS HERE ------------

    return thresh
```

### 📝 Markdown Cell 10

## Testing

Once you have completed the two functions, perform background subtraction on the provided video using the following code. The code will process the first N frames and display the result for the last frame. The output should look like Figure 1.

### 💻 Code Cell 11

```python
cap = cv2.VideoCapture('test.mp4')

N = 50
i = 0

state = state_initial.copy()

while i < N:

    ret, img_color = cap.read()
    if ret == False:
        break
        
    # Convert to grayscale
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)/255
    
    # Update
    state = updateBackgroundModel(img, state);
    
    i += 1
     
cap.release()

# Threshold
thresh = thresholdFrame(img, state);

# Overlay thresholded image on the frame
overlayed = np.stack((img,)*3, axis=-1)
red = img.copy()
red[thresh.astype("bool")] = 1
overlayed[:,:,0] = red

# Display
plt.figure(figsize=(10,7))
plt.imshow(overlayed)
plt.title('Detected motion')
plt.axis('off')
```

### 💻 Code Cell 12

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 13

**Generating output video (optional)**

In the following code cell, you can set `generate_video = True` to generate an output video showing the detected regions. Before submitting the assignment, please set `generate_video = False`.

### 💻 Code Cell 14

```python
generate_video = False

if generate_video:

    cap = cv2.VideoCapture('test.mp4')

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))

    N = 500
    i = 0

    state = state_initial.copy()

    while i < N:

        ret, img_color = cap.read()
        if ret == False:
            break

        # Convert to grayscale
        img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)/255
    
        # Threshold
        thresh = thresholdFrame(img, state);
    
        # Update
        state = updateBackgroundModel(img, state);
    
        # Write output frame
        red = img_color[:,:,2]
        red[thresh.astype("bool")] = 255
        img_color[:,:,2] = red
        out.write(img_color)
    
        i += 1
     
    cap.release()
    out.release()
```

### 📝 Markdown Cell 15

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`2 days`

**2. Did you experience any issues or find anything particularly confusing?**

`No so far`

### 📝 Markdown Cell 16

# References

`List any references here (optional).`

### 📝 Markdown Cell 17

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A6.ipynb`) into `MV_A6.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 23.02.2025**


## 📁 `A7-Hough/MV_A7.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 7 - Hough transform

## Personal details

* **Name(s):** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Introduction

In this assignment, we will use the Hough transform to detect circles in images. Specifically, we aim to extract 10-cent coins, as shown in Figure 1. The Hough transform consists of four basic steps: detecting edge pixels, building accumulator, filtering the accumulator, and extracting objects. We will implement these steps in the following sections. 

Refer to the __[`lecture notes`](https://moodle.oulu.fi/mod/page/view.php?id=1705517)__ for more details on the Hough transform.  

![hough_steps.jpg](attachment:hough_steps.jpg)

## Task 1 - Detect edge pixels (0.5 points)

Implement the first step of the Hough transform by extracting edge pixels using the Canny edge detector. The goal is to detect only the edges of the 10-cent coins, similar to Figure 1.

### Instructions
- Use [`cv2.Canny`](https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html) to extract edges from the image.
- Name the output **`edges`** and visualize the result.
- Experiment with different Canny parameters and select the ones that you think work best.
- Refer to the sample code in [`2DModels.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/2DModels.ipynb) for guidance on using the Canny edge detector.

### 💻 Code Cell 2

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

img = cv2.imread('coins.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ---------- YOUR CODE STARTS HERE -----------
# Read the grayscale image
img = cv2.imread('coins.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Gaussian Blur to reduce noise
blurred = cv2.GaussianBlur(img, (5, 5), 1)

# Apply Canny edge detection
low_threshold = 50  # Experiment with this value
high_threshold = 150  # Experiment with this value
edges = cv2.Canny(blurred, low_threshold, high_threshold)

# Display the original and edge-detected images
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Grayscale Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(edges, cmap='gray')
plt.title('Canny Edge Detection')
plt.axis('off')

plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 💻 Code Cell 3

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 4

## Hough parameter space

A circle has three parameters: the radius $d$, the row-coordinate of the center $r_0$ and the column-coordinate of the center $c_0$. Circles are represented by the equations:

$$
r = r_0 + d \, \text{sin} \theta \qquad \qquad (1)
$$
$$
c = c_0 + d \, \text{cos} \theta \qquad \qquad (2)
$$

Let us first consider the case when radius $d$ is fixed. In this case, we only need to find the center of the circle:

$$
r_0 = r - d \, \text{sin} \theta \qquad \qquad (3)
$$
$$
c_0 = c - d \, \text{cos} \theta \qquad \qquad (4)
$$

In the previous section, we detected edge pixels that hopefully belong to a circle. Let $(c, r)$ be one of those edge points. By varying $\theta$ from $0$ to $2\pi$ we can compute all possible circles $(c_0, r_0)$ that this point may belong. The following code illustrates this given three points. In this case, each of the points actually belongs to the same circle. Run the code and observe how each point generates a circle to the Hough parameter space.

### 💻 Code Cell 5

```python
d = 50 # Radius is fixed (10 cent coin)

# Three points that belong to a circle
pts = np.array([[170, 210],  # Point 1
                [190, 120],  # Point 2
                [250, 180]]) # Point 3

# Initialize accumulator
height, width = img.shape
A = np.zeros((height, width), dtype=np.float_)

# Theta goes from 0 to 2*pi
thetas = np.linspace(0, 2*np.pi, 360, endpoint=False)

for c, r in pts:
    for theta in thetas:
        # Compute circle center coordinates
        r0 = int(r - d * np.sin(theta))  # Eq. 3
        c0 = int(c - d * np.cos(theta))  # Eq. 4
        
        # Accumulate votes while ensuring indices are within bounds
        if 0 <= r0 < height and 0 <= c0 < width:
            A[r0, c0] += 1

plt.figure(figsize=(16,8))
plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.plot(pts[:,0], pts[:,1], 'ro')
plt.axis('off')
plt.title('Image space')
plt.subplot(122)
plt.imshow(A, cmap='gray')
plt.axis('off')
plt.title('Hough space (accumulator A)')
```

### 📝 Markdown Cell 6

Take a look at the accumulator `A` that was generated from the three points. Notice that all circles intersect at the same point (more or less). This point will have the most votes in the accumulator. If we extract the coordinates of that point, we find the most voted circle. The following code extracts the most voted circle.

### 💻 Code Cell 7

```python
# Find a circle that has most votes
idx = np.argsort(-A, axis=None) # Descending order: -A
r0, c0 = np.unravel_index(idx, A.shape)

# Use OpenCV to draw the first circle
circles = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.circle(circles, (c0[0],r0[0]), d, (0,0,255), 2)

plt.figure(figsize=(8,8))
plt.imshow(circles, cmap='gray')
plt.axis('off')
plt.title('A circle with most votes')
```

### 📝 Markdown Cell 8

## Task 2 - Hough accumulator (0.5 points)

Build the Hough accumulator using the edge points detected in Task 1. This step will accumulate votes for potential circle centers based on the detected edges. Use the sample code above as a reference — only minor modifications are needed.

### Instructions
- Initialize a new accumulator
- Extract row and column coordinates of edge points using **[`cv2.findNonZero`](https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html#find-non-zero-pixels)**. See the sample code __[`2DModels.ipynb`](https://github.com/jtheikkila/mvis/blob/master/jupyter/2DModels.ipynb)__.
- Accumulate votes for potential circle centers.
- Display the accumulator. It should resemble the Hough accumulator in Figure 1.

### 💻 Code Cell 9

```python
# ---------- YOUR CODE STARTS HERE -----------
# Initialize the Hough accumulator
height, width = img.shape
A = np.zeros((height, width), dtype=np.float_)

# Fixed radius assumption for 10-cent coins
d = 50  

# Find edge points (non-zero pixels)
edge_points = cv2.findNonZero(edges)  # Returns (x, y) tuples

# Define theta values (0 to 2π)
thetas = np.linspace(0, 2*np.pi, 360, endpoint=False)

# Iterate through edge points and accumulate votes
for point in edge_points:
    c, r = point[0]  # Extract (column, row) coordinates
    
    for theta in thetas:
        # Compute possible circle center coordinates
        r0 = int(r - d * np.sin(theta))  # Eq. 3
        c0 = int(c - d * np.cos(theta))  # Eq. 4

        # Check if indices are within bounds before accumulating votes
        if 0 <= r0 < height and 0 <= c0 < width:
            A[r0, c0] += 1  # Accumulate votes

# Visualization of the accumulator space
plt.figure(figsize=(16,8))

# Show detected edges
plt.subplot(121)
plt.imshow(edges, cmap='gray')
plt.title('Detected Edge Pixels')
plt.axis('off')

# Show Hough accumulator space
plt.subplot(122)
plt.imshow(A, cmap='hot')
plt.title('Hough Accumulator (Potential Circle Centers)')
plt.axis('off')

plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 10

## Task 3 - Extract circles (0.5 points)

Complete the following code cell. Extract 3 most voted circles from the accumulator you build in Task 2. The sample code shown earlier will help you complete this task. Use different colors when drawing the circles. You will notice that two of the circles are pretty much the same but slightly shifted.

### 💻 Code Cell 11

```python
# ---------- YOUR CODE STARTS HERE -----------
# Load grayscale image
img = cv2.imread('coins.jpg', cv2.IMREAD_GRAYSCALE)
color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert to color for visualization

# Initialize the Hough accumulator
height, width = img.shape
A = np.zeros((height, width), dtype=np.float_)

# Find edge points
edge_points = cv2.findNonZero(edges)

# Define theta values (0 to 2π)
thetas = np.linspace(0, 2*np.pi, 360, endpoint=False)

# Accumulate votes for potential circle centers
for point in edge_points:
    c, r = point[0]
    
    for theta in thetas:
        # Compute circle center
        r0 = int(r - d * np.sin(theta))
        c0 = int(c - d * np.cos(theta))

        if 0 <= r0 < height and 0 <= c0 < width:
            A[r0, c0] += 1  # Accumulate votes

# Step 1: Find the 3 most voted circle centers
num_circles = 3
flat_indices = np.argsort(A.ravel())[::-1]  # Sort in descending order
circle_centers = np.column_stack(np.unravel_index(flat_indices[:num_circles], A.shape))

# Step 2: Draw the detected circles
output_img = color_img.copy()

# Define colors for visualization
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

for i, (r0, c0) in enumerate(circle_centers):
    cv2.circle(output_img, (c0, r0), d, colors[i], 2)  # Draw circle

# Step 3: Visualize results
plt.figure(figsize=(16,8))

# Original image with circles overlaid
plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
plt.title("Detected Circles (Top 3)")
plt.axis("off")

plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 12

## Task 4 - Filter the accumulator (0.5 points)

The accumulator from Task 2 contains neighboring bins with high votes, leading to duplicate detections. Apply non-maxima suppression (NMS) to refine the accumulator and remove redundant peaks. Use the provided `nms()` function to produce a filtered accumulator.

### Instructions
- Apply non-maxima suppression using the function `nms()`.
- Display the filtered accumulator to visualize the effect of suppression.
- Extract the three most voted circles from the filtered accumulator, just as in Task 3.
- The final result should successfully detect each 10-cent coin as shown in Figure 1.

### 💻 Code Cell 13

```python
# Non-maxima suppression. This simple approach
# works in this case. Values that are not local maxima
# are set to zero.
# Step 1: Apply Non-Maxima Suppression (NMS)

def nms(accum):
    accum_filt = accum.copy()
    mi = accum.min()
    dil = cv2.dilate(accum_filt, None)
    accum_filt[accum_filt < dil] = mi
    return(accum_filt)

# ---------- YOUR CODE STARTS HERE -----------
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load grayscale image
img = cv2.imread('coins.jpg', cv2.IMREAD_GRAYSCALE)
color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert to color for visualization

# Initialize the Hough accumulator
height, width = img.shape
A = np.zeros((height, width), dtype=np.float_)

# Find edge points
edge_points = cv2.findNonZero(edges)

# Define theta values (0 to 2π)
thetas = np.linspace(0, 2*np.pi, 360, endpoint=False)

# Accumulate votes for potential circle centers
for point in edge_points:
    c, r = point[0]
    
    for theta in thetas:
        # Compute circle center
        r0 = int(r - d * np.sin(theta))
        c0 = int(c - d * np.cos(theta))

        if 0 <= r0 < height and 0 <= c0 < width:
            A[r0, c0] += 1  # Accumulate votes


A_filtered = nms(A)  # Apply NMS

# Step 2: Find the 3 most voted circle centers from filtered accumulator
num_circles = 3
flat_indices = np.argsort(A_filtered.ravel())[::-1]  # Sort in descending order
circle_centers = np.column_stack(np.unravel_index(flat_indices[:num_circles], A.shape))

# Step 3: Draw the detected circles
output_img = color_img.copy()

# Define colors for visualization
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

for i, (r0, c0) in enumerate(circle_centers):
    cv2.circle(output_img, (c0, r0), d, colors[i], 2)  # Draw circle

# Step 4: Visualize results
plt.figure(figsize=(16, 8))

# Show the filtered accumulator
plt.subplot(1, 2, 1)
plt.imshow(A_filtered, cmap='gray')
plt.title("Filtered Hough Accumulator (NMS Applied)")
plt.axis("off")

# Show detected circles on original image
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
plt.title("Final Detected Circles after NMS")
plt.axis("off")

plt.show()
# ----------- YOUR CODE ENDS HERE ------------
```

### 📝 Markdown Cell 14

## Finding circles with unknown radius

It is also possible to find circles with unknown radius by using a three dimensional accumulation matrix. We could specify a range of radius values (e.g. $d = [1,200]$ pixels). When building the accumulator, we could loop through all possible radius values. The maximum value in the 3D accumulator would correspond to the most voted circle. A direct implementation of such approach would be very slow. Let us use the OpenCV implementation instead to find all coins from the image.

### 💻 Code Cell 15

```python
filtered = cv2.medianBlur(img, 5)
circles = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

C = cv2.HoughCircles(filtered, cv2.HOUGH_GRADIENT, 1, 30,
                     param1=400, param2=30, minRadius=1, maxRadius=200)
C = np.uint16(np.around(C))

# Draw circles with most votes
for i in C[0,:]:
    cv2.circle(circles, (i[0],i[1]), i[2], (0,255,0), 2)

plt.figure(figsize=(8,8))
plt.imshow(circles)
plt.axis('off')
plt.title('OpenCV (HoughCircles)')
```

### 📝 Markdown Cell 16

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`3 days`

**2. Did you experience any issues or find anything particularly confusing?**

`Not in particular`

### 📝 Markdown Cell 17

# References
`LIST YOUR POSSIBLE REFERENCES HERE!`

### 📝 Markdown Cell 18

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A7.ipynb`) into `MV_A7.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 2.3.2025**


## 📁 `A8-Triangulation/MV_A8.ipynb`


### 📝 Markdown Cell 1

# Machine Vision
## Assignment 8 - Triangulation

## Personal details

* **Name(s):** `Daris Dzakwan Hoesien`
* **Student ID:** `2406778`

## Introduction

In this assignment, we will first project known 3D points onto a pair of stereo images using camera projection matrices. Then, we will triangulate 3D points from 2D correspondences. Let's first display the test images and the 2D point correspondences. We also load the 3D points. The data is from __http://www.robots.ox.ac.uk/~vgg/data/mview__.

### 💻 Code Cell 2

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
%matplotlib inline

# Load image pair and convert to RGB
left = cv2.imread('left.jpg')
right = cv2.imread('right.jpg')
left = cv2.cvtColor(left, cv2.COLOR_BGR2RGB)
right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB)

# Load 2D points (2xN matrices)
pts1 = np.load('pts1.npy')
pts2 = np.load('pts2.npy')

# Load 3D points (3xN matrix)
pts3D = np.load('pts3D.npy')

# Display 2D point correspondences
plt.figure(figsize=(14,8))
plt.subplot(121)
plt.imshow(left)
plt.plot(pts1[0,:], pts1[1,:], '.r')
plt.title('Left image')
plt.axis('off')
plt.subplot(122)
plt.imshow(right)
plt.plot(pts2[0,:], pts2[1,:], '.r')
plt.title('Right image')
plt.axis('off')
```

### 📝 Markdown Cell 3

The camera projection matrices $\mathbf{C}$ and $\mathbf{C}'$ are also provided for both views.

### 💻 Code Cell 4

```python
# Load 3x4 camera projection matrices
C1 = np.load('C1.npy')
C2 = np.load('C2.npy')
```

### 📝 Markdown Cell 5

## Task 1 - Project 3D points (0.5 points)

Project the given 3D points onto the image plane using the camera projection matrix $\mathbf{C} = \mathbf{K}[\mathbf{R} | \mathbf{t}]$. This involves transforming the 3D Euclidean coordinates into 2D image coordinates using the equation:

$$
s \begin{pmatrix}u \\ v \\ 1 \end{pmatrix} = \mathbf{C} \begin{pmatrix} X \\ Y \\ Z \\ 1 \end{pmatrix} \qquad \qquad (1)
$$

where homogeneous coordinates are used. Complete the function `projectPts` by following the instructions below. The result should look like the previous figure.

### Instructions
1. Convert the 3D points `pts3D` from Euclidean to homogeneous coordinates.
2. Apply Equation 1 to project the points onto the image plane.
3. Convert the projected 2D homogeneous coordinates back to Euclidean coordinates.

### 💻 Code Cell 6

```python
# INPUT   
# pts3D : 3D points (X,Y,Z) (3xN matrix)
# C     : Camera projection matrix (3x4 matrix)
#
# OUTPUT  
# pts2D : 2D points (x,y) (2xN matrix)
#
def projectPts(pts3D, C):
    
    N = pts3D.shape[1] # Number of points
    
    # ---------- YOUR CODE STARTS HERE -----------
    # Convert 3D Euclidean coordinates to homogeneous coordinates (add a row of ones)
    pts3D_hom = np.vstack((pts3D, np.ones((1, N))))  # (4xN matrix)

    # Apply the projection matrix: P = C * X (where X is in homogeneous coordinates)
    pts2D_hom = np.dot(C, pts3D_hom)  # Resulting shape is (3xN)

    # Convert back from homogeneous coordinates to Euclidean by dividing by the last row
    pts2D = pts2D_hom[:2, :] / pts2D_hom[2, :]  # Normalize (2xN matrix)    
    # ----------- YOUR CODE ENDS HERE ------------

    return pts2D


# Project 3D points and visualize the result
points1 = projectPts(pts3D, C1)
points2 = projectPts(pts3D, C2)

plt.figure(figsize=(14,8))
plt.subplot(121)
plt.imshow(left)
plt.plot(points1[0,:], points1[1,:], '.r')
plt.title('Left image')
plt.axis('off')
plt.subplot(122)
plt.imshow(right)
plt.plot(points2[0,:], points2[1,:], '.r')
plt.title('Right image')
plt.axis('off')
```

### 💻 Code Cell 7

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 8

## Task 2 - Triangulation (1.5 points)

A linear method for triangulating a point observed in two cameras is described in **Exercise 7, Question 6**. 

Given a point $\mathbf{X} = (X,Y,Z)^{\top}$ the projection equations are:

$$
\begin{pmatrix}
s u \\ 
s v \\
s \end{pmatrix} = 
\begin{pmatrix}
c_{11} & c_{12} & c_{13} & c_{14} \\ 
c_{21} & c_{22} & c_{23} & c_{24} \\
c_{31} & c_{32} & c_{33} & c_{34} \end{pmatrix}
\begin{pmatrix}
X \\ 
Y \\
Z \\
1 \end{pmatrix}
$$

$$
\begin{pmatrix}
t u' \\ 
t v' \\
t \end{pmatrix} = 
\begin{pmatrix}
c_{11}' & c_{12}' & c_{13}' & c_{14}' \\ 
c_{21}' & c_{22}' & c_{23}' & c_{24}' \\
c_{31}' & c_{32}' & c_{33}' & c_{34}' \end{pmatrix}
\begin{pmatrix}
X \\ 
Y \\
Z \\
1 \end{pmatrix}
$$

Here we have used the same notation as in the exercise. Eliminating $s$ and $t$ we obtain the system of equations:

$$
(c_{31} u - c_{11}) X + (c_{32} u - c_{12}) Y + (c_{33} u - c_{13}) Z = c_{14} - c_{34} u
$$
$$
(c_{31} v - c_{21}) X + (c_{32} v - c_{22}) Y + (c_{33} v - c_{23}) Z = c_{24} - c_{34} v
$$
$$
(c_{31}' u' - c_{11}') X + (c_{32}' u' - c_{12}') Y + (c_{33}' u' - c_{13}') Z = c_{14}' - c_{34}' u'
$$
$$
(c_{31}' v' - c_{21}') X + (c_{32}' v' - c_{22}') Y + (c_{33}' v' - c_{23}') Z = c_{24}' - c_{34}' v'
$$

which can be expressed in a linear system of the form $\mathbf{Ax} = \mathbf{b}$ and solved using the least squares method.

### Instructions
- Implement the function `triangulatePts` to estimate 3D points given 2D points `pts1` and `pts2` and projection matrices `C1` and `C2`.
- For each point, form the linear system $\mathbf{Ax} = \mathbf{b}$, where $\mathbf{A}$ is a $4 \times 3$ matrix and $\mathbf{b}$ is a $4 \times 1$ vector.
- Solve for $\hat{\mathbf{x}}$ using the least-squares method $\hat{\mathbf{x}} = (\mathbf{A}^{\top} \mathbf{A})^{-1} \mathbf{A}^{\top} \mathbf{b}$, , where $\hat{\mathbf{x}}$ contains the coordinates of the 3D point $(X,Y,Z)$.
- Run the code cell to verify your implementation. The function is correct if the estimated 3D points `pts3D_tri` align with the given 3D points `pts3D`.

### 💻 Code Cell 9

```python
# INPUT   
# pts1 : 2D points from the first image (2xN matrix)
# pts2 : 2D points from the second image (2xN matrix)
# C1   : Camera matrix for the first image (3x4 matrix)
# C2   : Camera matrix for the second image (3x4 matrix)
#
# OUTPUT  
# pts3D_tri : Triangulated 3D points (X,Y,Z) (3xN matrix)
#
def triangulatePts(pts1, pts2, C1, C2):
    
    N = pts1.shape[1] # Number of points
    pts3D_tri = np.zeros((3,N), dtype=np.float_)
    
    # ---------- YOUR CODE STARTS HERE -----------
    for i in range(N):  # Iterate over each point
        
        # Extract 2D coordinates from both images
        u, v = pts1[:, i]  # Point in first image
        u_prime, v_prime = pts2[:, i]  # Point in second image

        # Form the A matrix (4x3) and b vector (4x1) from projection equations
        A = np.array([
            [C1[2, 0] * u - C1[0, 0], C1[2, 1] * u - C1[0, 1], C1[2, 2] * u - C1[0, 2]],
            [C1[2, 0] * v - C1[1, 0], C1[2, 1] * v - C1[1, 1], C1[2, 2] * v - C1[1, 2]],
            [C2[2, 0] * u_prime - C2[0, 0], C2[2, 1] * u_prime - C2[0, 1], C2[2, 2] * u_prime - C2[0, 2]],
            [C2[2, 0] * v_prime - C2[1, 0], C2[2, 1] * v_prime - C2[1, 1], C2[2, 2] * v_prime - C2[1, 2]]
        ])

        b = np.array([
            C1[0, 3] - C1[2, 3] * u,
            C1[1, 3] - C1[2, 3] * v,
            C2[0, 3] - C2[2, 3] * u_prime,
            C2[1, 3] - C2[2, 3] * v_prime
        ])

        # Solve for X using least squares: X = (A^T A)^-1 A^T b
        X, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Store the computed 3D point
        pts3D_tri[:, i] = X    
    # ----------- YOUR CODE ENDS HERE ------------

    return pts3D_tri


# Triangulate points and compare to given 3D points
pts3D_tri = triangulatePts(pts1, pts2, C1, C2)

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(-pts3D[1,:], pts3D[2,:], -pts3D[0,:], 
           color='blue', label='Given 3D points')
ax.scatter(-pts3D_tri[1,:], pts3D_tri[2,:], -pts3D_tri[0,:], 
           color='red', label='Estimated 3D points')
ax.set_xlabel('Y')
ax.set_ylabel('Z')
ax.set_zlabel('X')
ax.set_title('Comparison of 3D points')
ax.legend()
```

### 💻 Code Cell 10

```python
# LEAVE EMPTY
```

### 📝 Markdown Cell 11

# Aftermath

Please provide short answers to the following questions:

**1. How much time did you need to complete this exercise?**

`2 days`

**2. Did you experience any issues or find anything particularly confusing?**

`No particular questions`

### 📝 Markdown Cell 12

# References
`LIST YOUR POSSIBLE REFERENCES HERE!`

### 📝 Markdown Cell 13

# Submission

1. Go to `Kernel -> Restart & Clear Output` to remove all outputs.
2. Compress this notebook (`MV_A8.ipynb`) into `MV_A8.zip`.
3. Submit the **zip** file on Moodle.

**Deadline: 12.3.2025**

