# logic.py
# In order to separate more complex program logic from the UI implementation.

from skimage import color, draw, util
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.filters import threshold_otsu
from skimage.filters import gaussian
import numpy as np


def mark_circles_in_image(img, low_radius=6, high_radius=10):
    """
    Detect circles in an image and mark all detected circles within with red lines.
    Marking the circle lines is only 'stub' functionality to check whether the algorithm works at all.
    :param img: The image to search for circles in
    :param low_radius: Specify the smallest possible radius for a circle
    :param high_radius: Specify the highest possible radius for a circle
    :return: (stub) The image all found circles marked red
    """
    image = gaussian(img, multichannel=True)
    image = color.rgb2gray(image)  # Convert image to grayscale; necessary for edge detection
    image = util.img_as_ubyte(image)  # Convert pixel format to 0 - 255 uint8

    thresh = threshold_otsu(image)
    image = image > thresh

    print(np.max(image))

    edges = canny(image)  # , sigma=3.)  # Canny algorithm edge detection

    # Radius range can either be set by passing arguments to the function or by setting the default arguments.
    hough_radii = np.arange(low_radius, high_radius)
    hough_res = hough_circle(edges, hough_radii)  # Detect circles

    # Get the most relevant circles (filter incorrectly detected); total_num_peaks = 5 * 6 -> Maximum number of points
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=30)

    circles = zip(cy, cx, radii)  # Associate the coordinates and radii belonging to the same circle with each other.

    # The following is stub code for the actual image processing
    edges = util.img_as_ubyte(color.gray2rgb(edges))
    for center_x, center_y, radius in circles:
        # Return the points of the circle line in the image
        circy, circx = draw.circle_perimeter(center_x, center_y, radius, shape=edges.shape)
        edges[circy, circx] = (220, 20, 20)  # Draw circle line red in image

    print(hough_res.shape)

    return edges
