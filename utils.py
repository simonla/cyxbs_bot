def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_token():
    return "328109625:AAECcBvUoOr-J9rjt3x-L0MgFt4wfsG5XKM"
