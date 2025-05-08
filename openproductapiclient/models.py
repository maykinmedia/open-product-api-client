import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel

from .client import OpenProductClient

logger = logging.getLogger(__name__)


class Configuration(SingletonModel):
    """
    The Open Product API configuration to retrieve and render Open Product data.
    """

    open_product_api_service = models.ForeignKey(
        "zgw_consumers.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="open_product_api_service",
    )

    open_product_types_api_service = models.ForeignKey(
        "zgw_consumers.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="open_product_types_api_service",
    )

    class Meta:
        verbose_name = _("Open Product API client configuration")

    def __str__(self):
        return "Open Product API client configuration"

    @property
    def client(self):
        if not self.open_product_api_service and self.open_product_types_api_service:
            return None
        return OpenProductClient(
            self.open_product_api_service, self.open_product_types_api_service
        )
