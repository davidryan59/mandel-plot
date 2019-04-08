import time
from PIL import Image

from calculate_mandelbrot_set import mandelbrot_set_float
from get_monochrome_image import get_monochrome_image
from update_parameter import update_parameter


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
iter_2exp_default = 8
iter_2exp_max = 24

x_res_2exp_min = 4
x_res_2exp_default = 8
x_res_2exp_max = 13.4

y_res_2exp_min = 3.6
y_res_2exp_default = 8
y_res_2exp_max = 13

increment_2exp = 0.5
step_2exp = 0.1

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

regen_image = True
resave_image = True
while True:
    # MAIN CONTROL LOOP

    if regen_image == True:
        # Regenerate the fractal image
        start_time = time.time()
        max_iteration = round(2 ** iter_2exp)
        x_pixels = round(2 ** x_res_2exp)
        y_pixels = round(2 ** y_res_2exp)
        x_width = 2 ** (-zoom_2exp)
        move_increment = x_width * 0.125

        start_iteration = 0
        end_iteration = max_iteration

        iteration_count_array = mandelbrot_set_float(x_centre, y_centre, zoom_2exp, x_pixels, y_pixels, start_iteration, end_iteration)[2]

        end_time = time.time()
        image_time_ms = (end_time - start_time) * 1000
        regen_image = False

    if resave_image == True:
        # Save the fractal image to the output file
        image_component_R = get_monochrome_image(period_R, iteration_count_array)
        image_component_G = get_monochrome_image(period_G, iteration_count_array)
        image_component_B = get_monochrome_image(period_B, iteration_count_array)
        colour_image = Image.merge('RGB', (image_component_R, image_component_G, image_component_B))
        colour_image = colour_image.transpose(Image.TRANSPOSE)
        colour_image = colour_image.transpose(Image.FLIP_TOP_BOTTOM)
        colour_image.save(output_image_filename)
        resave_image = False

    # Get next user command - should be a single character
    print('', end='> ')
    the_input = input()

    regen_image = True
    resave_image = True

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
    elif the_input == 't':
        x_res_2exp = update_parameter(x_res_2exp, increment=-increment_2exp, min=x_res_2exp_min, max=x_res_2exp_max, step=step_2exp)
        y_res_2exp = update_parameter(y_res_2exp, increment=-increment_2exp, min=y_res_2exp_min, max=y_res_2exp_max, step=step_2exp)

    elif the_input == 'R':
        print('')
        print('Updating resolution parameters')
        print('')
        print('Image currently %s x %s' % (x_pixels, y_pixels))
        print('x, y resolutions (log 2) are: %s, %s' % (x_res_2exp, y_res_2exp))
        x_res_2exp = update_parameter(x_res_2exp, message='Update x res (log 2)', min=x_res_2exp_min, max=x_res_2exp_max, step=step_2exp)
        y_res_2exp = update_parameter(y_res_2exp, message='Update y res (log 2)', min=y_res_2exp_min, max=y_res_2exp_max, step=step_2exp)
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
        print('Max iterations (effort): %s (%s)' % (max_iteration, iter_2exp))
        print('Zoom factor: %s' % zoom_2exp)
        print('Resolution = %s x %s' % (x_pixels, y_pixels))
        print('Colour scheme (B, R, G) = (%s, %s, %s)' % (period_B, period_R, period_G))
        print('Last image took {0:.0f} ms to generate'.format(image_time_ms))
        print('')
        regen_image = False
        resave_image = False

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
        resave_image = False

    elif the_input == 'q':
        print('Exiting program. Goodbye!')
        break

    else:
        print("Input %s not recognised. Use 'h' for help" % the_input)
        regen_image = False
        resave_image = False
