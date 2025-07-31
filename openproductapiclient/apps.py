from django.apps import AppConfig


class OpenProductAPIClientConfig(AppConfig):
    name = "openproductapiclient"

    # The amount of days before an indicator is shown
    #  that the product/document is about to expire.
    EXPIRATION_WARNING_TIME_SLOT = 14
