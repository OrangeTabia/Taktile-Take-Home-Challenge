def multiply(data):
    """Function that multiplies cols a & b"""

    data["sum"] = data["a"] * data["b"]

    return data


if __env:  # indicates we are running on Taktile
    data = multiply(data)
