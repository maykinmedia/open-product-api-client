def get_filled_params(rawparams):
    """
    Takes in a functions 'raw params' (e.g. retrieved with 'locals()')
    and removes all the 'self' and None-valued entries. Also converts
    lists into a format understood by the API.
    """

    # i = []
    # for key, value in rawparams.items():
    #     if isinstance(value, list[str]):
    #         value = ', '.join(value)

    return {
        key: ", ".join(value) if isinstance(value, list) else value
        for key, value in rawparams.items()
        if key != "self" and value is not None
    }
