def update_parameter(var_prev, message='message', increment=False, method='float', min=False, max=False, step=False):
    if increment:
        # Function parameter defines input
        # increment and var_prev should be numeric
        try:
            var_next = var_prev + increment
        except:
            print('CODE ERROR: Invalid increment supplied')
            return var_prev
    else:
        # Take input from user to set variable
        # Methods currently supported:
        # float
        # int
        print(message, end=': ')
        var_next_txt = input()

        if var_next_txt == '':
            print('No input value was specified. Using previous value of %s' % var_prev)
            return var_prev

        try:
            if method == 'float':
                var_next = float(var_next_txt)
            elif method == 'int':
                var_next = int(var_next_txt)
            else:
                print('CODE ERROR: Input method invalid')
                return var_prev
        except:
            print('Input value was invalid')
            return var_prev

    if method == 'float' or method == 'int':
        # Numeric values
        if min:
            if var_next < min:
                print('New value %s is smaller than %s' % (var_next, min))
                return var_prev
        if max:
            if var_next > max:
                print('New value %s is larger than %s' % (var_next, max))
                return var_prev
        if step:
            var_next = round(var_next / step) * step

    # print('Variable updated to %s' % var_next)

    return var_next
