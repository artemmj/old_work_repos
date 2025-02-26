import pytest

from api.v1.product.services import ConvertHiddenTitleAttrsQsToStrService, GetProductTitleAttrsService

pytestmark = [pytest.mark.django_db]


def test_convert_additional_title_attrs_qs_to_str_successful(
    products_factory,
    title_attrs_factory,
    project,
):
    """Тест для успешного преобразования списка скрытых аттрибутов названия продукта в строку."""
    product = products_factory(count=1)
    title_attrs_count = 3
    is_hidden_attr = True

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=is_hidden_attr,
        content=(content for content in ('красный', 'синий', 'желтый'))
    )

    hidden_title_attrs = GetProductTitleAttrsService(
        project_id=project.id,
        product_id=product.id,
        is_hidden=is_hidden_attr,
    ).process()

    converted_hidden_title_attrs = ConvertHiddenTitleAttrsQsToStrService(
        hidden_title_attrs_qs=hidden_title_attrs,
        delimiter=',',
    ).process()

    assert converted_hidden_title_attrs == '(красный, синий, желтый)'
