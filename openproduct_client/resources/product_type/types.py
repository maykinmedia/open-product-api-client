from collections.abc import Mapping, Sequence
from typing import Literal

import msgspec

from ...typing import PaginationParams, ResourceMeta

#
# Input
#


class ProductTypeParams(PaginationParams):
    # these are some of the available query parameters, append when/if needed
    aanmaak_datum: str | None = (
        None  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    )
    code: str | None = None
    gepubliceerd: bool | None = None
    keywords: Sequence[str] | None = None
    naam: str | None = None
    themas__naam: str | None = None
    themas__uuid: str | None = None
    toegestane_statussen: Sequence[str] | None = None


class ThemeParams(PaginationParams):
    # these are some of the available query parameters, append when/if needed
    aanmaak_datum: str | None = (
        None  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    )
    gepubliceerd: bool | None = None
    naam: str | None = None
    producttypen__uuid: str | None = None
    update_datum: str | None = (
        None  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    )


class ContentParams(PaginationParams):
    exclude_labels: Sequence[str] | None = None
    labels: Sequence[str] | None = None


class ContentThemeParams(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str


class PriceParams(msgspec.Struct, metaclass=ResourceMeta):
    # these are some of the available query parameters, append when/if needed
    actief_vanaf: str | None = None
    actief_vanaf__gte: str | None = None  # a date string (2019-09-24)
    actief_vanaf__lte: str | None = None  # a date string (2019-09-24)
    producttype__uuid: str | None = None


#
# Output
#

PRODUCT_TYPE_ALLOWED_STATES = Literal[
    "in_aanvraag",
    "gereed",
    "actief",
    "ingetrokken",
    "geweigerd",
    "verlopen",
]
TARGET_GROUP_OPTIONS = Literal[
    "burgers",
    "interne_organisatie",
    "samenwerkingspartners",
    "bedrijven_en_instellingen",
]


class ContentLabels(msgspec.Struct, metaclass=ResourceMeta):
    naam: str


class ProductTypeContent(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    taal: str
    content: str
    aanvullende_informatie: str | None = None
    labels: Sequence[str] | None = None


class NestedProductType(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    code: str
    naam: str
    uniforme_product_naam: str
    toegestane_statussen: Sequence[PRODUCT_TYPE_ALLOWED_STATES] | None = None
    gepubliceerd: bool
    aanmaak_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    update_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    taal: str
    keywords: Sequence[str] | None = None
    publicatie_start_datum: str | None = None  # a date string (2019-09-24)
    publicatie_eind_datum: str | None = None  # a date string (2019-09-24)


class Theme(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    naam: str
    beschrijving: str | None = None
    gepubliceerd: bool | None = None
    aanmaak_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    update_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    hoofd_thema: str | None = None
    producttypen: Sequence[NestedProductType]


class NestedTheme(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    naam: str
    beschrijving: str | None = None
    gepubliceerd: bool | None = None
    aanmaak_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    update_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    hoofd_thema: str


class Location(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    naam: str
    email: str | None = None
    telefoonnummer: str | None = None
    straat: str | None = None
    huisnummer: str | None = None
    postcode: str | None = None
    stad: str | None = None


class Organization(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    naam: str
    code: str
    email: str | None = None
    telefoonnummer: str | None = None
    straat: str | None = None
    huisnummer: str | None = None
    postcode: str | None = None
    stad: str | None = None


class Contact(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    organisatie: Organization | None = None
    naam: str
    email: str | None = None
    telefoonnummer: str | None = None
    rol: str | None = None


class PriceOption(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str | None = None
    bedrag: str  # a decimal
    beschrijving: str


class PriceRule(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str | None = None
    url: str  # uri and read-only
    beschrijving: str
    mapping: Mapping | None = (
        None  # mapping between the fields in Open Product & DMN variable
    )


class Price(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    producttype_uuid: str
    prijsopties: Sequence[PriceOption] | None = None
    prijsregels: Sequence[PriceRule] | None = None
    actief_vanaf: str  # a date string (2019-09-24)


class NestedPrice(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    prijsopties: Sequence[PriceOption] | None = None
    prijsregels: Sequence[PriceRule] | None = None
    actief_vanaf: str  # a date string (2019-09-24)


class NestedLink(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    naam: str
    url: str  # uri


class NestedAction(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    naam: str
    url: str  # uri
    mapping: Mapping | None = (
        None  # mapping between the fields in Open Product & DMN variable
    )


class NestedFile(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    bestand: str  # uri


class NestedExternalCode(msgspec.Struct, metaclass=ResourceMeta):
    naam: str
    code: str


class NestedParameters(msgspec.Struct, metaclass=ResourceMeta):
    naam: str
    waarde: str


class ConsumableSchema(msgspec.Struct, metaclass=ResourceMeta):
    naam: str
    schema: Mapping


class DataObjectSchema(msgspec.Struct, metaclass=ResourceMeta):
    naam: str
    schema: Mapping


class NestedCaseType(msgspec.Struct, metaclass=ResourceMeta):
    urn: str | None = None
    url: str | None = None  # uri


class NestedRequestType(msgspec.Struct, metaclass=ResourceMeta):
    urn: str | None = None
    url: str | None = None  # uri


class NestedProcess(msgspec.Struct, metaclass=ResourceMeta):
    urn: str | None = None
    url: str | None = None  # uri


class ProductType(msgspec.Struct, metaclass=ResourceMeta):
    uuid: str
    uniforme_product_naam: str | None = None
    doelgroep: TARGET_GROUP_OPTIONS
    themas: Sequence[NestedTheme]
    locaties: Sequence[Location]
    organisaties: Sequence[Organization]
    eigenaar: str | None = None
    contacten: Sequence[Contact]
    prijzen: Sequence[NestedPrice]
    links: Sequence[NestedLink]
    acties: Sequence[NestedAction]
    bestanden: Sequence[NestedFile]
    naam: str
    samenvatting: str
    taal: str
    externe_codes: Sequence[NestedExternalCode] | None = None
    parameters: Sequence[NestedParameters] | None = None
    verbruiksobject_schema: ConsumableSchema | None
    dataobject_schema: DataObjectSchema | None
    gepubliceerd: bool
    publicatie_start_datum: str | None = None  # a date string (2019-09-24)
    publicatie_eind_datum: str | None = None  # a date string (2019-09-24)
    aanmaak_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    update_datum: str  # a date-time ISO 8601 string (2019-08-24T14:15:22Z)
    code: str
    toegestane_statussen: Sequence[PRODUCT_TYPE_ALLOWED_STATES] | None = None
    keywords: Sequence[str] | None = None
    interne_opmerkingen: str | None = None
    zaaktypen: Sequence[NestedCaseType] | None = None
    verzoektypen: Sequence[NestedRequestType] | None = None
    processen: Sequence[NestedProcess] | None = None
