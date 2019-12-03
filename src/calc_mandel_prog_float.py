from numba import jit

@jit
def calc_mandel_prog_float(x_curr_mx, y_curr_mx, iter_curr_mx, img_curr_mx, esc_mx, min_iter, max_iter, sum_iter, x_coords, y_coords, iteration_increment, ppo_data, pstart, pend):
    # Evaluate the Mandelbrot set progressively using a supplied pixel order

    # Accuracy of z = x + jy are floating point only, so 2^-46 < zoom,
    # after that you get pixellation


    the_len = len(ppo_data)
    for pix_idx in range(pstart, pend):
        pmod_idx = pix_idx % the_len    # Calculation wraps around

        # On first pass, draw squares for pixels
        # On subsequent pass, pixels are 1x1

        if pmod_idx == 0:
            # Reset min_iter, when restarting pixel sequence
            min_iter = 1000000000000

        # Unpack ppo_data
        first_pass = False
        x_size = 1
        y_size = 1
        x_idx = ppo_data[pmod_idx][2]
        y_idx = ppo_data[pmod_idx][3]
        if pmod_idx == pix_idx:
            # First pass - draw larger squares
            first_pass = True
            x_size = ppo_data[pmod_idx][4]
            y_size = ppo_data[pmod_idx][5]

        # Continue evaluating unescaped points
        if esc_mx[x_idx, y_idx] == 0:
            # This point hasn't escaped yet
            x_start = x_coords[x_idx]
            y_start = y_coords[y_idx]
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
            curr_iter = iter_curr_mx[x_idx, y_idx]
            if first_pass == False or x_size * y_size == 1:
                img_curr_mx[x_idx, y_idx] = curr_iter
            else:
                for x_img_idx in range(x_idx, x_idx + x_size):
                    for y_img_idx in range(y_idx, y_idx + y_size):
                        img_curr_mx[x_img_idx, y_img_idx] = curr_iter
                        if x_size*y_size<9:
                            print(x_idx, y_idx, x_size, y_size, x_img_idx, y_img_idx, curr_iter)
            min_iter = min(min_iter, curr_iter)
            max_iter = max(max_iter, curr_iter)
            sum_iter += iter_diff
    return (x_curr_mx, y_curr_mx, iter_curr_mx, img_curr_mx, esc_mx, min_iter, max_iter, sum_iter)
