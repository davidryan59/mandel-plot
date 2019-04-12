import numpy
import math

from PIL import Image

def get_monochrome_image(colour_period, iter_curr_mx):
    # Input is array of raw iteration counts
    # Output is array of numbers between 0 and 255
    image_result = iter_curr_mx % colour_period
    image_inverted = colour_period - image_result
    image_result = numpy.minimum(image_result, image_inverted)
    image_result *= 255.0 / math.ceil(colour_period * 0.5)
    image_result = Image.fromarray(image_result)
    image_result = image_result.convert('L')
    return image_result
