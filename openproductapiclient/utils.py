def get_filled_params(rawparams):
    """
    Takes in a functions 'raw params' (e.g. retrieved with 'locals()')
    and removes all the 'self' and None-valued entries.
    """

    return {
        key: value
        for key, value in rawparams.items()
        if key != "self" and value is not None
    }
