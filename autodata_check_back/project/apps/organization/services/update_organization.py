from typing import Dict

from apps.helpers.services import AbstractService
from apps.organization.models import Organization, TypeOrganizationChoices


class UpdateOrganizationByDadataService(AbstractService):
    """Сервис обновления данных организации на основе данных из Dadata."""

    def __init__(self, organization: Organization, dadata_response: Dict):    # noqa: D107
        self.organization = organization
        self.dadata_response = dadata_response

    def process(self):
        if self.dadata_response[0]['data']['type'] == TypeOrganizationChoices.LEGAL.upper():  # noqa: WPS204
            self.organization.type = TypeOrganizationChoices.LEGAL
            self.organization.kpp = self.dadata_response[0]['data']['kpp']
            self.organization.ogrn = self.dadata_response[0]['data']['ogrn']
            self.organization.ogrnip = None
        elif self.dadata_response[0]['data']['type'] == TypeOrganizationChoices.INDIVIDUAL.upper():
            self.organization.type = TypeOrganizationChoices.INDIVIDUAL
            self.organization.ogrnip = self.dadata_response[0]['data']['ogrn']
            self.organization.kpp = self.organization.ogrn = None  # noqa: WPS429
        self.organization.legal_title = self.dadata_response[0]['data']['name']['short_with_opf']  # noqa: WPS219
        self.organization.address = self.dadata_response[0]['data']['address']['value']  # noqa: WPS219
        if not self.organization.title:
            title = self.dadata_response[0]['data']['name']['short_with_opf']  # noqa: WPS219
            title = title.replace('"', '').replace('ООО ', '').replace('ИП ', '')
            self.organization.title = title
