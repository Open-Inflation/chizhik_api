"""Работа с каталогом"""

from __future__ import annotations

import urllib.parse
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from human_requests import ApiChild, ApiParent, api_child_field, autotest
from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI  # noqa: F401


@dataclass(init=False)
class ClassCatalog(ApiChild["ChizhikAPI"], ApiParent):
    """Методы для работы с каталогом товаров.

    Включает поиск товаров, получение информации о категориях,
    работу с фидами товаров и отзывами.
    """

    Product: ProductService = api_child_field(
        lambda parent: ProductService(parent.parent)
    )
    """Сервис для работы с товарами в каталоге."""

    def __init__(self, parent: "ChizhikAPI"):
        super().__init__(parent)
        ApiParent.__post_init__(self)

    @autotest
    async def tree(self, city_id: Optional[str] = None) -> FetchResponse:
        """Получить дерево категорий."""
        url = f"{self._parent.CATALOG_URL}/catalog/unauthorized/categories/"
        if city_id:
            url += f"?city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def products_list(
        self,
        page: int = 1,
        category_id: Optional[int] = None,
        city_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> FetchResponse:
        """Получить список продуктов в категории."""
        url = f"{self._parent.CATALOG_URL}/catalog/unauthorized/products/?page={page}"
        if category_id:
            url += f"&category_id={category_id}"
        if city_id:
            url += f"&city_id={city_id}"
        if search:
            url += f"&term={urllib.parse.quote(search)}"
        return await self._parent._request(HttpMethod.GET, url)


class ProductService(ApiChild["ChizhikAPI"]):
    """Сервис для работы с товарами в каталоге."""

    @autotest
    async def info(
        self, product_id: int, city_id: Optional[str] = None
    ) -> FetchResponse:
        """Получить информацию о товаре по его ID.

        Args:
            product_id (int): ID товара.
            city_id (str, optional): ID города для локализации данных. Defaults to None.

        Returns:
            Response: Ответ от сервера с информацией о товаре.
        """

        url = f"{self._parent.CATALOG_URL}/catalog/unauthorized/products/{product_id}/"
        if city_id:
            url += f"?city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)
