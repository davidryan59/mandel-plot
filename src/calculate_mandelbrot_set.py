import numpy
from numba import jit

@jit
def mandelbrot_set_float(x_centre, y_centre, zoom_2exp, x_pixels, y_pixels, max_iterations):
    # Inputs for x_centre and y_centre are floating point.
    # Limited accuracy - a decimal version will have higher accuracy.

    x_width = 2 ** (-zoom_2exp)
    y_width = x_width * y_pixels / x_pixels

    x_wp5 = 0.5 * x_width
    x_min = x_centre - x_wp5
    x_max = x_centre + x_wp5

    y_wp5 = 0.5 * y_width
    y_min = y_centre - y_wp5
    y_max = y_centre + y_wp5

    x_coord_array = numpy.linspace(x_min, x_max, x_pixels)
    y_coord_array = numpy.linspace(y_min, y_max, y_pixels)
    iteration_count_array = numpy.empty((x_pixels, y_pixels))

    for x_idx in range(x_pixels):
        for y_idx in range(y_pixels):
            iteration_count_array[x_idx, y_idx] = 0
            x_start = x_coord_array[x_idx]
            y_start = y_coord_array[y_idx]
            x_current = x_start
            y_current = y_start
            for current_iterations in range(max_iterations):
                x2_current = x_current * x_current
                y2_current = y_current * y_current
                if x2_current + y2_current > 4:
                    iteration_count_array[x_idx, y_idx] = current_iterations
                    break
                x_next = x2_current - y2_current + x_start
                y_current = 2 * x_current * y_current + y_start
                x_current = x_next

    return iteration_count_array
