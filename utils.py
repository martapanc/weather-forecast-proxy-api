
def validate_latitude(latitude):
    return -90 < float(latitude) < 90


def validate_longitude(longitude):
    return -180 < float(longitude) < 180


def validate_units(units):
    return units == 'default' or units == 'metric' or units == 'imperial'
