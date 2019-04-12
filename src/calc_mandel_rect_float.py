from numba import jit

@jit
def calc_mandel_rect_float(x_curr_mx, y_curr_mx, iter_curr_mx, esc_mx, max_iter, sum_iter, x_coords, y_coords, iteration_increment):
    # Evaluate the Mandelbrot set across a rectangular set of coordinates x_coords, y_coords
    # between a specified set of iterations iter_start to iter_end
    # Results to create image with are stored in iter_curr_mx
    # (where a value of 0 means calculation is still in progress)
    # Temporary iterated positions of x, y are stored in x_curr_mx, y_curr_mx

    # Accuracy of z = x + jy are floating point only, so 2^-46 < zoom,
    # after that you get pixellation

    for x_idx, x_start in enumerate(x_coords):
        for y_idx, y_start in enumerate(y_coords):
            if esc_mx[x_idx, y_idx] == 0:
                # This point hasn't escaped yet
                x_current = x_curr_mx[x_idx, y_idx]
                y_current = y_curr_mx[x_idx, y_idx]
                for iter_diff in range(1, iteration_increment + 1):
                    x2_current = x_current * x_current
                    y2_current = y_current * y_current
                    if x2_current + y2_current > 4:
                        # Escaped values ought to be greater than zero
                        esc_mx[x_idx, y_idx] = 1
                        break
                    # These three lines implement the Mandelbrot iteration function
                    # z -> z^2 + c
                    # splitting z into x + jy manually
                    # since numpy arrays can't take complex numbers
                    x_next = x2_current - y2_current + x_start
                    y_current = 2 * x_current * y_current + y_start
                    x_current = x_next
                x_curr_mx[x_idx, y_idx] = x_current
                y_curr_mx[x_idx, y_idx] = y_current
                iter_curr_mx[x_idx, y_idx] += iter_diff
                max_iter = max(max_iter, iter_curr_mx[x_idx, y_idx])
                sum_iter += iter_diff
    return (x_curr_mx, y_curr_mx, iter_curr_mx, esc_mx, max_iter, sum_iter)
