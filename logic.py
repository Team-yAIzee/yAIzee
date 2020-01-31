# logic.py
# In order to separate more complex program logic from the UI implementation.

from skimage import color, draw, util
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.filters import threshold_otsu
from skimage.filters import gaussian
import numpy as np
from scipy.spatial import distance
import cv2
import matplotlib.pyplot as plt


def mark_circles_in_image(img, low_radius=6, high_radius=10):
    # Deprecated
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


def circle_kernel(radius, border):
    """
    Return a numpy array containing a circle with the given radius filled with True pixels, and a border around
    it filled with False pixels.
    :param radius The radius of the circle
    :param border The size of the border around the circle
    """
    array = [[(i ** 2 + j ** 2) ** 0.5 <= radius
              for j in range(-radius-border, radius + 1 + border)] for i in range(-radius-border, radius + 1 + border)]
    return np.array(array).astype(np.float32)


def filter_dice_eyes(image, eye_kernel, match_thresh=0.6):
    # Apply threshold to image brightness in order to prevent unwanted color differences from appearing
    # in the resulting image
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    threshed = ((hsv[:, :, 2] < 140) * 255).astype(np.uint8)

    threshed = (threshed / 255.0).astype(np.float32)  # treshed/255.0 -> float -> float32

    matches = cv2.matchTemplate(threshed, eye_kernel, cv2.TM_SQDIFF_NORMED)

    threshed_matchings = matches < match_thresh

    found = np.where(threshed_matchings)
    found_arr = np.asarray([i for i in zip(*found)])

    fuse = True
    while fuse:
        fuse = False

        for p in found_arr:
            dist = distance.cdist(found_arr, [p])
            nearest_other = np.argsort(dist[:, 0])[1]
            if (abs(found_arr[nearest_other] - p) < 25).all() == True:
                found_arr = np.delete(found_arr, nearest_other, axis=0)
                fuse = True
                break  # In case some other code added below

    # debug
    figure = np.zeros(shape=threshed_matchings.shape)
    for i, p in enumerate(found_arr):
        figure[found_arr[i, 0]:found_arr[i, 0] + 10, found_arr[i, 1]:found_arr[i, 1] + 10] = 1.

    plt.figure(figsize=(20, 20))
    plt.imshow(figure, cmap='gray')
    plt.show()

    return figure  # TODO should be changed to found_arr later, but for testing purposes returns resulting image
