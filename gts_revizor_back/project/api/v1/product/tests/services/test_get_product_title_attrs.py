import pytest

from api.v1.product.services import GetProductTitleAttrsService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('is_hidden', [True, False])
def test_get_additional_title_attrs_successful(
    products_factory,
    title_attrs_factory,
    is_hidden,
    project,
):
    """Тест для успешного получения доп. аттрибутов названия продуктов."""
    product = products_factory(count=1)
    title_attrs_count = 5

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=is_hidden,
    )

    additional_title_attrs = GetProductTitleAttrsService(
        project_id=project.id,
        product_id=product.id,
        is_hidden=is_hidden,
    ).process()

    assert additional_title_attrs.count() == title_attrs_count
