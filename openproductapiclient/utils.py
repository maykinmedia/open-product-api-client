from typing import TypedDict


def format_list_params(rawparams):
    """
    Converts lists into a format understood by the API.
    """

    return {
        key: ", ".join(value) if isinstance(value, list) else value
        for key, value in rawparams.items()
    }


class ListProductsParams(TypedDict, total=False):
    aanmaak_datum: str
    aanmaak_datum__gte: str
    aanmaak_datum__lte: str
    dataobject_attr: str
    documenten__uuid: str
    eigenaren__bsn: str
    eigenaren__klantnummer: str
    eigenaren__kvk_nummer: str
    eigenaren__uuid: str
    eigenaren__vestigingsnummer: str
    eind_datum: str
    eind_datum__gte: str
    eind_datum__lte: str
    frequentie: str
    gepubliceerd: bool
    page: int
    page_size: int
    prijs: float
    prijs_gte: float
    prijs_lte: float
    producttype__code: str
    producttype__code__in: list[str]
    producttype__naam: str
    producttype__naam__in: list[str]
    producttype__uuid: str
    producttype__uuid__in: list[str]
    start_datum: str
    start_datum_gte: str
    start_datum_lte: str
    status: str
    uniforme_product_naam: str
    update_datum: str
    update_datum__gte: str
    update_datum__lte: str
    verbruiksobject_attr: str


class ListProductTypesParams(TypedDict, total=False):
    aanmaak_datum: str
    aanmaak_datum_gte: str
    aanmaak_datum_lte: str
    code: str
    externe_code: str
    gepubliceerd: bool
    keywords: list[str]
    letter: str
    page: int
    page_size: int
    parameter: str
    processen__uuid: str
    themas__naam: str
    themas__naam__in: list[str]
    themas__uuid: str
    themas__uuid__in: list[str]
    toegestane_statussen: list[str]
    uniforme_product_naam: str
    update_datum: str
    update_datum__gte: str
    update_datum__lte: str
    verbruiksobject_schema_naam: str
    verzoektypen__uuid: str
    zaaktypen__uuid: str


class ListThemesParams(TypedDict, total=False):
    aanmaak_datum: str
    aanmaak_datum__gte: str
    aanmaak_datum__lte: str
    gepubliceerd: bool
    hoofd_thema__naam: str
    hoofd_thema__uuid: str
    naam: str
    page: int
    page_size: int
    update_datum: str
    update_datum__gte: str
    update_datum__lte: str


class ListOrganizationsParams(TypedDict, total=False):
    code: str
    email__iexact: str
    huisnummer__iexact: str
    naam__iexact: str
    page: int
    page_size: int
    postcode: str
    stad: str
    straat__iexact: str
    telefoonnummer__contains: str
