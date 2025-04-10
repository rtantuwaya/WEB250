# lessons/lesson3.py
def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        'meters': 1,
        'kilometers': 1000,
        'miles': 1609.34
    }

    if from_unit == to_unit:
        return value

    # Convert the value to meters first
    value_in_meters = value * conversion_factors[from_unit]
    result = value_in_meters / conversion_factors[to_unit]
    return result

