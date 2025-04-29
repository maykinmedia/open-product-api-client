# import logging

# logger = logging.getLogger(__name__)


# def get_object_type_choices(client=None, use_uuids=False):
#     if client is None:
#         from .models import Configuration

#         config = Configuration.get_solo()
#         client = config.client

#     if not client:
#         return []

#     objecttypes = client.get_object_types()

#     return sorted(
#         [(item.uuid, item.name) for item in objecttypes],
#         key=lambda entry: entry[1],
#     )


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
