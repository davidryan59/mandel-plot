import numpy
from PIL import Image
import cv2

from get_monochrome_image import get_monochrome_image


def draw_image(window_name, iter_curr_mx, pR, pG, pB):
    # Save the fractal image to the output file
    image_component_R = get_monochrome_image(pR, iter_curr_mx)
    image_component_G = get_monochrome_image(pG, iter_curr_mx)
    image_component_B = get_monochrome_image(pB, iter_curr_mx)
    colour_image = Image.merge('RGB', (image_component_R, image_component_G, image_component_B))
    colour_image = colour_image.transpose(Image.TRANSPOSE)
    colour_image = colour_image.transpose(Image.FLIP_TOP_BOTTOM)

    # Convert Pillow image back to Numpy (CV2)
    open_cv_image = numpy.array(colour_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    # Display image using CV2
    cv2.imshow(window_name, open_cv_image)
    cv2.waitKey(1)
