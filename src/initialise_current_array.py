from numba import jit

@jit
def initialise_current_array(x_curr_mx, y_curr_mx, x_coords, y_coords):
    for x_idx, x_coord in enumerate(x_coords):
        for y_idx, y_coord in enumerate(y_coords):
            x_curr_mx[x_idx, y_idx] = x_coord
            y_curr_mx[x_idx, y_idx] = y_coord
    return (x_curr_mx, y_curr_mx)
