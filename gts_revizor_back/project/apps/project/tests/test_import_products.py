import os
from secrets import token_urlsafe
import pytest

from django.test import override_settings

from apps.template.models.template_choices import TemplateFieldChoices
from apps.product.models import Product
from apps.project.tasks.import_products import ImportProductsService

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_import_products(project, templates_factory, files_factory):
    dirpath = f'apps/project/tests/'
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    filepath = f'{dirpath}FORTEST_{token_urlsafe(4)}.txt'
    dbfile = files_factory(count=1, file=filepath)

    with open(filepath, 'w', encoding='windows-1251') as ofile:
        with open('apps/project/tests/import_products.txt', 'r') as ifile:
            for idx, line in enumerate(ifile.readlines()):
                if idx in (0, 1):
                    continue
                ofile.writelines(line)

    template = templates_factory(
        count=1,
        field_separator=';',
        decimal_separator=',',
        fields=[
            TemplateFieldChoices.VENDOR_CODE,
            TemplateFieldChoices.TITLE,
            TemplateFieldChoices.PIN_NOT_DOWNLOAD,
            TemplateFieldChoices.BARCODE,
            TemplateFieldChoices.REMAINDER,
            TemplateFieldChoices.PRICE,
            TemplateFieldChoices.MEASURE,
            TemplateFieldChoices.SIZE,
            TemplateFieldChoices.AM,
            TemplateFieldChoices.DM,
            TemplateFieldChoices.STORE_NUMBER,
            TemplateFieldChoices.REMAINDER_2,
            # TemplateFieldChoices.ZONE_CODE,
            # TemplateFieldChoices.ZONE_NAME,
            # TemplateFieldChoices.BARCODE_X5,
        ]
    )
    serializer_data = {
        'file': dbfile.pk,
        'project': project.pk,
        'template': template.pk,
    }
    service = ImportProductsService(serializer_data=serializer_data)
    service.process()

    products_qs = Product.objects.filter(project=project).order_by('vendor_code')
    assert products_qs.count() == 5
    fproduct = products_qs.first()
    assert fproduct.vendor_code == '100001'
    splitted_title = fproduct.title.split(',')
    title = ''.join(splitted_title[:-1])
    measure = splitted_title[-1]
    assert title == 'Футболка с кор.рукавом черный XS'
    assert measure == ' ШТ'
    assert fproduct.barcode == '4620123276753'
    assert fproduct.remainder == -200
    assert fproduct.price == 500
    assert fproduct.size == 'XS'
    assert fproduct.am == 'amamam'
    assert fproduct.dm == 'dmdmdm'
    assert fproduct.store_number == 9999
    assert fproduct.remainder_2 == 11

    os.remove(filepath)
