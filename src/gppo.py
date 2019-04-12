# from get_progressive_pixel_order import get_progressive_pixel_order as gppo

import math
import time
# from numba import jit

verbose = False

# @jit
def gppo2(exp2):
    # 'Get Progressive Pixel Order, power of 2'

    # Provide a progressive pixel order for image power of 2
    # e.g. 1x1, 2x2, 4x4, 8x8, etc

    # Validate input
    exp2 = int(exp2)

    # Don't allow massive values through - will take too long!
    max_exp2 = 13      # 67 million pixels, 8192 x 8192 = 2^13 x 2^13
    if max_exp2 < exp2:
        raise Exception('For gppo2 function, image is square with size N x N, where N = 2^n, and max(n) = {}, however requested n = {}.'.format(max_exp2, exp2))
    if verbose:
        print('Function gppo2 running with 2-exponent {}'.format(exp2))


    # Base case for 1x1
    if exp2 <= 0:
        parent = [-1]
        x_pos = [0]
        y_pos = [0]
        x_size = [1]
        y_size = [1]
        return (parent, x_pos, y_pos, x_size, y_size)


    # Iterative case
    (parent_prev, x_pos_prev, y_pos_prev, x_size_prev, y_size_prev) = gppo2(exp2 - 1)

    len_prev = len(parent_prev)
    len_prev2 = 2 * len_prev
    len_this = 4 * len_prev

    range_prev = [*range(len_prev)]
    range_prev2 = [*range(len_prev2)]
    range_this = [*range(2 ** exp2)]

    parent_this = [*parent_prev, *range_prev, *range_prev2]

    x_pos_this = [*[2*z for z in x_pos_prev], *[2*z+1 for z in x_pos_prev]]
    x_pos_this = [*x_pos_this, *x_pos_this]

    y_pos_this = [*y_pos_prev, *y_pos_prev]
    y_pos_this = [*[2*z for z in y_pos_this], *[2*z+1 for z in y_pos_this]]

    x_size_this = [*[2*z for z in x_size_prev], *[1 for z in range_prev], *[1 for z in range_prev2]]
    y_size_this = [*[2*z for z in y_size_prev], *[2 for z in range_prev], *[1 for z in range_prev2]]

    return (parent_this, x_pos_this, y_pos_this, x_size_this, y_size_this)


# @jit
def gppo(x_px, y_px):
    # 'Get Progressive Pixel Order'

    # Get order of update of pixels for an x_px * y_px image
    # where some of the earlier pixels cover a larger size
    # (e.g. blocky updates)
    # starting with the pixels in the middle of the image

    start_time = time.time()

    # Validation
    x_px = int(x_px)
    y_px = int(y_px)
    if x_px < 1 or y_px < 1:
        raise Exception('Function gppo supplied with invalid size {} x {}'.format(x_px, y_px))
    if verbose:
        print('')
        print('Function gppo running with size {} x {}'.format(x_px, y_px))

    # Get basic pixel structure using power of 2
    px = max(x_px, y_px)
    exp2 = math.log2(px)
    exp2 = math.ceil(exp2)
    (parent, x_pos, y_pos, x_size, y_size) = gppo2(exp2)

    # Get output into a format it can be filtered and sorted
    the_len = len(parent)
    # row_index = [*range(the_len)]
    data = [[i, parent[i], x_pos[i], y_pos[i], x_size[i], y_size[i], 0] for i in range(the_len)]
    # data[0] is row index
    # data[6] is distance, which will be defined later
    if verbose:
        print('Original data length is {}'.format(the_len))
        # print(data)

    # Remove any pixels that start greater than x_px or y_px
    data_filter = lambda data_row: data_row[2] < x_px and data_row[3] < y_px
    data = list(filter(data_filter, data))
    the_len = len(data)
    if verbose:
        print('Filtered data length is {}'.format(the_len))
        # print(data)

    # # Update indices of this row and parent row, after filtering
    # # Indices for this row, data[i][0], are strictly ascending
    # # so can do binary search on them
    # @jit
    # def search_for_old_parent_index(s, i, j):
    #     # Searching data[i..j][0] for value s
    #     # if verbose:
    #     #     print('Searching for parent index {} in rows {} to {}'.format(s, i, j))
    #     if j < i:
    #         raise Exception('Parent index {} not found'.format(s))
    #     k = round(0.5 * (i + j))
    #     this_s = data[k][0]
    #     # if verbose:
    #     #     print('Midpoint is row {} with index {}'.format(k, this_s))
    #     if this_s == s:
    #         # if verbose:
    #         #     print('MATCH')
    #         return k
    #     elif s < this_s:
    #         # if verbose:
    #         #     print('{} < {}, search earlier rows'.format(s, this_s))
    #         return search_for_old_parent_index(s, i, k-1)
    #     else:
    #         # if verbose:
    #         #     print('{} > {}, search later rows'.format(s, this_s))
    #         return search_for_old_parent_index(s, k+1, j)

    if verbose:
        print('After filter, amending parent indices, then row indices, to take account of rows filtered out')
    for i in range(1, the_len):
        old_idx = data[i][1]

        # # O(n^2) way
        # for j in range(min(old_idx, the_len - 1), -1, -1):
        #     if data[j][0] == old_idx:
        #         new_idx = j
        #         break
        # else:
        #     raise Exception('Index {} not found, for parent of row {}'.format(old_idx, i))

        # Try another O(n log(n)) way
        start_search = 0
        end_search = the_len - 1
        mid_search = round(0.5 * (start_search + end_search))
        while True:
            idx_found = data[mid_search][0]
            if idx_found == old_idx:
                new_idx = mid_search
                break
            elif old_idx < idx_found:
                end_search = mid_search
            else:
                start_search = mid_search
            mid_search = round(0.5 * (start_search + end_search))
            if start_search == end_search:
                raise Exception('The old index value was not found')


        # # O(n log(n)) way
        # # but doesn't seem to work with numba.jit
        # new_idx = search_for_old_parent_index(old_idx, 0, the_len-1)

        # if verbose:
        #   print('Parent index: old {}, new {}'.format(old_idx, new_idx))
        #   print('')
        data[i][1] = new_idx

    for i in range(0, the_len):
        data[i][0] = i

    # Reduce the size of any pixels that range outside the bounds
    for i in range(the_len):
        x_size_max = x_px - data[i][2]
        y_size_max = y_px - data[i][3]
        if x_size_max < data[i][4]:
            data[i][4] = x_size_max
        if y_size_max < data[i][5]:
            data[i][5] = y_size_max
    if verbose:
        print('Pixel sizes reduced to be within image')
        # print(data)

    # Put in a distance function (with small wobble, for unique distances)
    x_image_centre = 0.5 * x_px + 0.127
    y_image_centre = 0.5 * y_px + 0.037
    for i in range(the_len):
        x_pixel_centre = data[i][2] + 0.5 * data[i][4]
        y_pixel_centre = data[i][3] + 0.5 * data[i][5]
        dist_squared = (x_pixel_centre - x_image_centre) ** 2 + (y_pixel_centre - y_image_centre) ** 2
        data[i][6] = int(dist_squared * 1000)
    if verbose:
        print('Distances from pixels to centre of image calculated')
        # print(data)

    # For each pixel, if its parent has a larger distance, then reduce the parent.
    # We will sort on distance, and this makes sure pixels draw in the right order.
    # Omit pixel 0, which has no parent
    for i in range(1, the_len):
        # i = 1, 2, 3... the_len -1
        j = the_len - i
        # j = the_len-1, the_len-2, ..., 2, 1
        this_dist = data[j][6]
        parent_idx = data[j][1]
        # if verbose:
        #   print('i={}, j={}, idx={}, parent_idx={}'.format(i, j, data[j][0], parent_idx))
        parent_dist = data[parent_idx][6]
        # Parent needs to have strictly lower distance.
        # If this isn't the case, then amend parent distance
        if this_dist <= parent_dist:
            data[parent_idx][6] = this_dist - 1
    if verbose:
        print('Parent distances changed so that parents will draw before children')
        # print(data)

    # Sort data by increasing distance
    data.sort(key=lambda data_row: data_row[6])
    if verbose:
        print('Data sorted by increasing distance from centre of image')
        # print(data)

    # # Print the list of pixels
    # for i in range(the_len):
    #     data_row = data[i]
    #     if verbose:
    #       print('({}, {}) is {} x {}   {}'.format(data_row[2], data_row[3], data_row[4], data_row[5], data_row[6]))

    end_time = time.time()
    time_elapsed_ms = round(1000 * (end_time - start_time))
    if verbose:
        print('')
        print('Pixel order for {} x {} image calculated in {} ms'.format(x_px, y_px, time_elapsed_ms))
        print('')

    return data
    # Return format is array (length N, for N pixels) of arrays, where inner array has this format:
    # 0: index of row (0 .. N-1)
    # 1: index of parent row (-1 for row 0)
    # 2: x index in image (0 .. x_px - 1)
    # 3: y index in image (0 .. y_px - 1)
    # 4: x size in image (1 = 1 pixel)
    # 5: y size in image (1 = 1 pixel)
    # 6: parameter used to sort, related to distance from centre of image
