import os
from secrets import token_urlsafe
from django.test import override_settings
import pytest

from apps.file.models import File
from apps.template.models.template_choices import TemplateFieldChoices
from apps.zone.models import Zone
from apps.project.tasks.import_zones import ImportZonesService

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_import_zones(project, templates_factory, files_factory):
    dirpath = f'apps/project/tests/'
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    filepath = f'{dirpath}FORTEST_{token_urlsafe(4)}.txt'
    dbfile = files_factory(count=1, file=filepath)

    with open(filepath, 'w', encoding='windows-1251') as ofile:
        with open('apps/project/tests/import_zones.txt', 'r') as ifile:
            ofile.writelines(ifile.readlines())

    template = templates_factory(
        count=1,
        field_separator=';',
        decimal_separator=',',
        fields=[
            TemplateFieldChoices.ZONE_CODE,
            TemplateFieldChoices.ZONE_NAME,
            # TemplateFieldChoices.VENDOR_CODE,
            # TemplateFieldChoices.TITLE,
            # TemplateFieldChoices.PIN_NOT_DOWNLOAD,
            # TemplateFieldChoices.BARCODE,
            # TemplateFieldChoices.REMAINDER,
            # TemplateFieldChoices.PRICE,
            # TemplateFieldChoices.MEASURE,
            # TemplateFieldChoices.SIZE,
            # TemplateFieldChoices.AM,
            # TemplateFieldChoices.DM,
            # TemplateFieldChoices.STORE_NUMBER,
            # TemplateFieldChoices.REMAINDER_2,
            # TemplateFieldChoices.BARCODE_X5,
        ]
    )
    serializer_data = {
        'file': dbfile.pk,
        'project': project.pk,
        'template': template.pk,
    }
    service = ImportZonesService(serializer_data=serializer_data)
    service.process()

    zones_qs = Zone.objects.filter(project=project).order_by('created_at')
    assert zones_qs.count() == 5
    assert zones_qs.last().title == 'zone 5'
    assert zones_qs.last().code == '5'

    os.remove(filepath)
