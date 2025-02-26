import pytest

from api.v1.product.services.convert_additional_title_attrs_qs_to_str import ConvertAdditionalTitleAttrsToStrService
from apps.project.tasks.export_document_services.add_title_attrs import AddTitleAttrsService

pytestmark = [pytest.mark.django_db]


def test_add_title_attrs(products_factory, title_attrs_factory, project):
    product = products_factory(count=1)
    title_attrs_count = 3
    is_hidden_attr = False

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=is_hidden_attr,
        content=(content for content in ('красный', 'синий', 'желтый'))
    )

    attrs_str = ConvertAdditionalTitleAttrsToStrService(
        additional_title_attrs=product.title_attrs.all(),
        delimiter=',',
    ).process()
    assert attrs_str == ', красный, синий, желтый'

    data = AddTitleAttrsService().process(
        export_content={
            'barcode': '1111',
            'title': 'test',
            'vendor_code': 'qqwwee',
        },
        product_id=product.pk,
        project_id=project.pk,
    )
    assert 'pin_additional_title_1' in data
    assert data['pin_additional_title_1'] == 'красный'

    assert 'pin_additional_title_2' in data
    assert data['pin_additional_title_2'] == 'синий'

    assert 'pin_additional_title_3' in data
    assert data['pin_additional_title_3'] == 'желтый'
