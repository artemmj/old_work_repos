from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.product.models import Product, ScannedProduct, AdditionalProductTitleAttribute

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def products_factory():
    """Фикстура для генерации продуктов."""

    def _factory(count: int, **fields) -> Union[Product, List[Product]]:
        if count == 1:
            return mixer.blend(
                Product,
                **fields,
            )
        return mixer.cycle(count).blend(
            Product,
            **fields,
        )

    return _factory


@pytest.fixture
def scanned_products_factory():
    """Фикстура для генерации отсканированных продуктов."""

    def _factory(count: int, **fields) -> Union[ScannedProduct, List[ScannedProduct]]:
        if count == 1:
            return mixer.blend(
                ScannedProduct,
                **fields,
            )
        return mixer.cycle(count).blend(
            ScannedProduct,
            **fields,
        )

    return _factory


@pytest.fixture
def title_attrs_factory():
    """Фикстура для генерации доп аттрибутов названия продукта."""

    def _factory(count: int, **fields) -> Union[AdditionalProductTitleAttribute, List[AdditionalProductTitleAttribute]]:
        if count == 1:
            return mixer.blend(
                AdditionalProductTitleAttribute,
                **fields,
            )
        return mixer.cycle(count).blend(
            AdditionalProductTitleAttribute,
            **fields,
        )

    return _factory
