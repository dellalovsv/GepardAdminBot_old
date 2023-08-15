def check_int(data) -> bool:
    try:
        int(data)
        return True
    except ValueError:
        return False


def check_float(data) -> bool:
    try:
        float(data)
        return True
    except Exception as e:
        return False
