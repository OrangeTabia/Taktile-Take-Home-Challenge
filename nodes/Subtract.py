def subtract(data):
    """Function that summarized cols a & b"""

    data["difference"] = data["a"] - data["b"]

    return data


if __env:  # indicates we are running on Taktile
    data = subtract(data)
