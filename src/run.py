import time

import numpy
import cv2

from initialise_current_array import initialise_current_array
from calc_mandel_rect_float import calc_mandel_rect_float
from draw_image import draw_image
from update_parameter import update_parameter
from get_ms_since import get_ms_since
from ppo import ppo

# Open a window to display the image
window_name = 'image'
cv2.namedWindow(window_name)
cv2.moveWindow(window_name, 0, 0)

# Tell user what's going on, in the terminal
print('')
print('')
print('')
print('***** MANDELBROT SET PLOTTER, by David Ryan *****')
print('')
print("Press 'h' for help with keyboard commands")
print("Press 's' to display current statistics")
print('')

# User variables
output_image_filename = 'src/temp_output_image.png'
iteration_increment = 50
image_redraw_ms = 200

x_centre_min = -2.1
x_centre_default = -0.75
x_centre_max = 0.5

y_centre_min = -1.25
y_centre_default = 0
y_centre_max = 1.25

zoom_2exp_min = -3
zoom_2exp_default = -2
zoom_2exp_max = 48
zoom_2exp_increment = 1

iter_2exp_min = 4
iter_2exp_default = 9
iter_2exp_max = 24

x_res_2exp_min = 5
x_res_2exp_default = 8
x_res_2exp_max = 9

y_res_2exp_min = 5
y_res_2exp_default = 8
y_res_2exp_max = 9

increment_2exp = 0.5
step_2exp = 0.01

period_B_default = 19
period_R_default = 49
period_G_default = 127

period_max = 1000000

x_centre = x_centre_default
y_centre = y_centre_default
zoom_2exp = zoom_2exp_default
iter_2exp = iter_2exp_default
x_res_2exp = x_res_2exp_default
y_res_2exp = y_res_2exp_default
period_B = period_B_default
period_R = period_R_default
period_G = period_G_default

# Initialise blank resolution parameters
x_pixels = None
y_pixels = None
ppo_data = None
# Function to recalculate them
def recalc_ppo(xr2, yr2):
    global x_pixels, y_pixels, ppo_data
    x_pixels = round(2 ** xr2)
    y_pixels = round(2 ** yr2)
    # # Logging this operation to the console, since it's slow!
    # # Want the user to know the cost of changing resolution
    # print('')
    # print('Creating PPO (Progressive Pixel Ordering) data for {} x {} image...'.format(x_pixels, y_pixels))
    # start_time = time.time()
    # ppo_data = ppo(x_pixels, y_pixels)
    # print('...PPO data with length {} was created in {} ms'.format(len(ppo_data), get_ms_since(start_time)))
    # print('')
# Call the function to initialise the right values
recalc_ppo(x_res_2exp, y_res_2exp)

regen_image = True
redraw_image = True
while True:
    # MAIN CONTROL LOOP

    if regen_image == True:
        # Regenerate the fractal image

        sum_iter = 0
        max_iter = 0

        start_time = time.time()
        iterations_limit = round(2 ** iter_2exp)
        x_width = 2 ** (-zoom_2exp)
        move_increment = x_width * 0.125

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

        x_coords = numpy.linspace(x_min, x_max, x_pixels)
        y_coords = numpy.linspace(y_min, y_max, y_pixels)
        iter_curr_mx = numpy.zeros((x_pixels, y_pixels))
        esc_mx = numpy.zeros((x_pixels, y_pixels))
        x_curr_mx = numpy.empty((x_pixels, y_pixels))
        y_curr_mx = numpy.empty((x_pixels, y_pixels))
        (x_curr_mx, y_curr_mx) = initialise_current_array(x_curr_mx, y_curr_mx, x_coords, y_coords)

        reset_time = time.time()
        calculate_more_iterations = True
        while calculate_more_iterations:
            prev_sum = sum_iter
            (x_curr_mx, y_curr_mx, iter_curr_mx, esc_mx, max_iter, sum_iter) = calc_mandel_rect_float(x_curr_mx, y_curr_mx, iter_curr_mx, esc_mx, max_iter, sum_iter, x_coords, y_coords, iteration_increment)
            calculate_more_iterations = max_iter < iterations_limit and prev_sum < sum_iter
            if calculate_more_iterations and image_redraw_ms < get_ms_since(reset_time):
                # Need incremental update on image
                draw_image(window_name, iter_curr_mx, period_R, period_G, period_B)
                reset_time = time.time()

        max_iter = int(max_iter)               # Array it derives from is a float
        iter_curr_mx = iter_curr_mx * esc_mx   # Mask non-escaped points in the image to black
        image_time_ms = get_ms_since(start_time)
        regen_image = False

    if redraw_image == True:
        draw_image(window_name, iter_curr_mx, period_R, period_G, period_B)
        redraw_image = False

    # Get next user command - should be a single character
    print('', end='> ')
    the_input = input()

    regen_image = True
    redraw_image = True

    # Deal with all different user commands
    if the_input == 'a':
        x_centre = update_parameter(x_centre, increment=-move_increment, min=x_centre_min, max=x_centre_max)
    elif the_input == 'd':
        x_centre = update_parameter(x_centre, increment=move_increment, min=x_centre_min, max=x_centre_max)
    elif the_input == 'x':
        y_centre = update_parameter(y_centre, increment=-move_increment, min=y_centre_min, max=y_centre_max)
    elif the_input == 'w':
        y_centre = update_parameter(y_centre, increment=+move_increment, min=y_centre_min, max=y_centre_max)

    elif the_input == 'i':
        zoom_2exp = update_parameter(zoom_2exp, increment=zoom_2exp_increment, min=zoom_2exp_min, max=zoom_2exp_max, step=step_2exp)
    elif the_input == 'o':
        zoom_2exp = update_parameter(zoom_2exp, increment=-zoom_2exp_increment, min=zoom_2exp_min, max=zoom_2exp_max, step=step_2exp)

    elif the_input == 'u':
        iter_2exp = update_parameter(iter_2exp, increment=increment_2exp, min=iter_2exp_min, max=iter_2exp_max, step=step_2exp)
    elif the_input == 'y':
        iter_2exp = update_parameter(iter_2exp, increment=-increment_2exp, min=iter_2exp_min, max=iter_2exp_max, step=step_2exp)

    elif the_input == 'r':
        x_res_2exp = update_parameter(x_res_2exp, increment=increment_2exp, min=x_res_2exp_min, max=x_res_2exp_max, step=step_2exp)
        y_res_2exp = update_parameter(y_res_2exp, increment=increment_2exp, min=y_res_2exp_min, max=y_res_2exp_max, step=step_2exp)
        recalc_ppo(x_res_2exp, y_res_2exp)
    elif the_input == 't':
        x_res_2exp = update_parameter(x_res_2exp, increment=-increment_2exp, min=x_res_2exp_min, max=x_res_2exp_max, step=step_2exp)
        y_res_2exp = update_parameter(y_res_2exp, increment=-increment_2exp, min=y_res_2exp_min, max=y_res_2exp_max, step=step_2exp)
        recalc_ppo(x_res_2exp, y_res_2exp)

    elif the_input == 'R':
        print('')
        print('Updating resolution parameters')
        print('')
        print('Image currently %s x %s' % (x_pixels, y_pixels))
        print('x, y resolutions (log 2) are: %s, %s' % (x_res_2exp, y_res_2exp))
        x_res_2exp = update_parameter(x_res_2exp, message='Update x res (log 2)', min=x_res_2exp_min, max=x_res_2exp_max, step=step_2exp)
        y_res_2exp = update_parameter(y_res_2exp, message='Update y res (log 2)', min=y_res_2exp_min, max=y_res_2exp_max, step=step_2exp)
        recalc_ppo(x_res_2exp, y_res_2exp)
        print('x, y resolutions (log 2) are: %s, %s' % (x_res_2exp, y_res_2exp))
        print('Image will be %s x %s' % (round(2**x_res_2exp), round(2**y_res_2exp)))

    elif the_input == 'P':
        print('')
        print('Updating location parameters')
        print('x, y, zoom, effort are: %s, %s, %s, %s' % (x_centre, y_centre, zoom_2exp, iter_2exp))
        x_centre = update_parameter(x_centre, message='Update x', min=x_centre_min, max=x_centre_max)
        y_centre = update_parameter(y_centre, message='Update y', min=y_centre_min, max=y_centre_max)
        zoom_2exp = update_parameter(zoom_2exp, message='Update zoom', min=zoom_2exp_min, max=zoom_2exp_max, step=step_2exp)
        iter_2exp = update_parameter(iter_2exp, message='Update effort', min=iter_2exp_min, max=iter_2exp_max, step=step_2exp)
        print('x, y, zoom, effort are: %s, %s, %s, %s' % (x_centre, y_centre, zoom_2exp, iter_2exp))

    elif the_input == 'Z':
        x_centre = x_centre_default
        y_centre = y_centre_default
        zoom_2exp = zoom_2exp_default
        iter_2exp = iter_2exp_default
        x_res_2exp = x_res_2exp_default
        y_res_2exp = y_res_2exp_default
        period_B = period_B_default
        period_R = period_R_default
        period_G = period_G_default

    elif the_input == 'c':
        print('')
        print('Updating colour parameters')
        print('Periods of blue, red, green are %s, %s, %s' % (period_B, period_R, period_G))
        period_B = update_parameter(period_B, message='New blue', method='int', min=1, max=period_max)
        period_R = update_parameter(period_R, message='New red', method='int', min=1, max=period_max)
        period_G = update_parameter(period_G, message='New green', method='int', min=1, max=period_max)
        print('Periods of blue, red, green are %s, %s, %s' % (period_B, period_R, period_G))
        regen_image = False

    elif the_input == 's':
        print('')
        print('CURRENT STATISTICS')
        print('')
        print('(x, y) = (%s, %s)' % (x_centre, y_centre))
        print('Max iterations (effort): %s (%s)' % (iterations_limit, iter_2exp))
        print('Zoom factor: %s' % zoom_2exp)
        print('Resolution = %s x %s (which is %s, %s log 2)' % (x_pixels, y_pixels, x_res_2exp, y_res_2exp))
        print('Colour scheme (B, R, G) = (%s, %s, %s)' % (period_B, period_R, period_G))
        print('Last image took {0:.0f} ms to generate, max iteration depth {1:,}, total iteration count {2:,}'.format(image_time_ms, max_iter, sum_iter))
        print('')
        regen_image = False
        redraw_image = False

    elif the_input == 'h':
        print('')
        print('HELP FUNCTION (h) - Keyboard Commands')
        print('')
        print('Display current stats (s)')
        print('Adjust: position (adwx), zoom (io), effort (yu), resolution (rt)')
        print('Set: colours (c), position (P), resolution (R)')
        print('RESET all parameters (Z)')
        print('QUIT (q)')
        print('')
        regen_image = False
        redraw_image = False

    elif the_input == 'q':
        print('Exiting program. Goodbye!')
        cv2.destroyAllWindows()
        break

    else:
        print("Input %s not recognised. Use 'h' for help" % the_input)
        regen_image = False
        redraw_image = False
