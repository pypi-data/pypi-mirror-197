import re  # Import re lib to find the integers in the string pass from 'value'

''' To use 'func' function you need to use a specific format
    Examples: func('5x+10')   func('5x-10')   func('-5x+10')   func('-5x-10') '''


def func(value):
    values = [int(s) for s in re.findall(r'[+-]?\d+', value)]  # Separate integers from string

    value_a = int(values[0])  # value_a receiving the first integers from the values list
    value_b = int(values[1])  # value_b receiving the second integers from the values list

    value_b *= -1  # value_b has been multiplied for -1 to passing from negative or positive, depending on the 'value'

    operation = value_b / value_a  # Here the division is used to discover the X value of the function

    return operation
