def multiply(data):
    """Function that summarized cols a & b"""

    data["sum"] = data["a"] * data["b"]

    return data


if __env:  # indicates we are running on Taktile
    data = multiply(data)
