from numba import jit

@jit
def calc_mandel_rect_float(x_current_array, y_current_array, iteration_count_array, start_iteration, end_iteration, x_coord_array, y_coord_array):
    # Evaluate the Mandelbrot set across a rectangular set of coordinates x_coord_array, y_coord_array
    # between a specified set of iterations start_iteration to end_iteration
    # Results to create image with are stored in iteration_count_array
    # (where a value of 0 means calculation is still in progress)
    # Temporary iterated positions of x, y are stored in x_current_array, y_current_array

    # Accuracy of z = x + jy are floating point only, so 2^-46 < zoom,
    # after that you get pixellation

    for x_idx, x_start in enumerate(x_coord_array):
        for y_idx, y_start in enumerate(y_coord_array):

            if start_iteration == 0:
                x_current = x_start
                y_current = y_start
                # -----
                # Only need to do this since numpy.empty(...) doesn't seem to initialise properly!
                x_current_array[x_idx, y_idx] = x_current
                y_current_array[x_idx, y_idx] = y_current
                iteration_count_array[x_idx, y_idx] = 0
                # -----
            else:
                x_current = x_current_array[x_idx, y_idx]
                y_current = y_current_array[x_idx, y_idx]

            if iteration_count_array[x_idx, y_idx] == 0:
                # This point hasn't escaped yet

                for current_iteration in range(start_iteration, end_iteration):
                    x2_current = x_current * x_current
                    y2_current = y_current * y_current
                    if x2_current + y2_current > 4:
                        # Escaped values ought to be greater than zero
                        iteration_count_array[x_idx, y_idx] = max(1, current_iteration)
                        break
                    # These three lines implement the Mandelbrot iteration function
                    # z -> z^2 + c
                    # splitting z into x + jy manually
                    # since numpy arrays can't take complex numbers
                    x_next = x2_current - y2_current + x_start
                    y_current = 2 * x_current * y_current + y_start
                    x_current = x_next

                x_current_array[x_idx, y_idx] = x_current
                y_current_array[x_idx, y_idx] = y_current

    return (x_current_array, y_current_array, iteration_count_array)
