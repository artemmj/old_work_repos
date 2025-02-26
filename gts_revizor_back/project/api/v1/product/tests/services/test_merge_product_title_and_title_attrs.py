import pytest

from api.v1.product.services import MergeProductTitleAndTitleAttrsService

pytestmark = [pytest.mark.django_db]


def test_merge_product_title_and_additional_title_attrs_successful(
    products_factory,
    title_attrs_factory,
    project,
):
    """Тест для успешного соединения доп аттрибутов названия продуктов и названия."""
    product = products_factory(count=1, title='Антистресс утка')
    title_attrs_count = 3

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=False,
        content=(content for content in ('красный', 'синий', 'желтый')),
    )

    res_string = MergeProductTitleAndTitleAttrsService(
        additional_title_attrs=product.title_attrs.filter(is_hidden=False),
        hidden_title_attrs=product.title_attrs.filter(is_hidden=True),
        product_title=product.title,
    ).process()

    assert res_string == 'Антистресс утка, красный, синий, желтый'


def test_merge_product_title_and_hidden_title_attrs_successful(
    products_factory,
    title_attrs_factory,
    project,
):
    """Тест для успешного соединения скрытых аттрибутов названия продуктов и названия."""
    product = products_factory(count=1, title='Антистресс утка')
    title_attrs_count = 3

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=True,
        content=(content for content in ('красный', 'синий', 'желтый')),
    )

    res_string = MergeProductTitleAndTitleAttrsService(
        additional_title_attrs=product.title_attrs.filter(is_hidden=False),
        hidden_title_attrs=product.title_attrs.filter(is_hidden=True),
        product_title=product.title,
    ).process()

    assert res_string == 'Антистресс утка (красный, синий, желтый)'


def test_merge_product_title_and_all_title_attrs_successful(
    products_factory,
    title_attrs_factory,
    project,
):
    """Тест для успешного соединения дополнительных и скрытых аттрибутов названия продуктов и названия."""
    product = products_factory(count=1, title='Антистресс утка')
    title_attrs_count = 3

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=True,
        content=(content for content in ('красный', 'синий', 'желтый')),
    )

    title_attrs_factory(
        count=title_attrs_count,
        project=project,
        product_id=product.id,
        is_hidden=False,
        content=(content for content in ('красный', 'синий', 'желтый')),
    )

    res_string = MergeProductTitleAndTitleAttrsService(
        additional_title_attrs=product.title_attrs.filter(is_hidden=False),
        hidden_title_attrs=product.title_attrs.filter(is_hidden=True),
        product_title=product.title,
    ).process()

    assert res_string == 'Антистресс утка, красный, синий, желтый (красный, синий, желтый)'
