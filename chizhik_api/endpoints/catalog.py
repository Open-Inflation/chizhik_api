"""Работа с каталогом"""

from __future__ import annotations

import urllib.parse
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from human_requests import ApiChild, ApiParent, api_child_field, autotest
from human_requests.abstraction import FetchResponse, HttpMethod

from ..abstraction import DeliveryMode

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
        url = f"{self._parent.API_URL}/v1/catalog/unauthorized/categories/"
        if city_id:
            url += f"?city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def delivery_tree(
        self,
        store_id: str,
        mode: DeliveryMode = DeliveryMode.STORE,
        include_restrict: bool = True,
    ):
        url = f"{self._parent.DELIVERY_API_URL}/catalog/v3/stores/{store_id}/categories?mode={mode}&include_subcategories=1&include_restrict={str(include_restrict).lower()}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def delivery_tree_extended(
        self,
        store_id: str,
        category_alias: str,
        mode: DeliveryMode = DeliveryMode.STORE,
        include_restrict: bool = True,
    ):
        url = f"{self._parent.DELIVERY_API_URL}/catalog/v2/stores/{store_id}/categories/{category_alias}/extended?mode={mode}&include_restrict={str(include_restrict).lower()}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def delivery_tree_ancestors(
        self,
        store_id: str,
        category_alias: str,
        mode: DeliveryMode = DeliveryMode.STORE,
        include_restrict: bool = True,
    ):
        url = f"{self._parent.DELIVERY_API_URL}/catalog/v3/stores/{store_id}/categories/{category_alias}/ancestors?mode={mode}&include_restrict={str(include_restrict).lower()}"
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
        url = f"{self._parent.API_URL}/v1/catalog/unauthorized/products/?page={page}"
        if category_id:
            url += f"&category_id={category_id}"
        if city_id:
            url += f"&city_id={city_id}"
        if search:
            url += f"&term={urllib.parse.quote(search)}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def delivery_products_list(
        self,
        store_id: str,
        category_alias: str,
        offset: int = 0,
        limit: int = 499,
        mode: DeliveryMode = DeliveryMode.STORE,
        include_restrict: bool = True,
    ):
        url = f"{self._parent.DELIVERY_API_URL}/catalog/v2/stores/{store_id}/categories/{category_alias}/products?mode={mode}&include_restrict={str(include_restrict).lower()}&limit={limit}&offset={offset}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def delivery_search(
        self,
        store_id: str,
        query: str,
        limit: int = 12,
        mode: DeliveryMode = DeliveryMode.STORE,
        include_restrict: bool = True,
    ):
        url = f"{self._parent.DELIVERY_API_URL}/catalog/v3/stores/{store_id}/search?mode={mode}&include_restrict={str(include_restrict).lower()}&q={query}&limit={limit}"
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

        url = f"{self._parent.API_URL}/v1/catalog/unauthorized/products/{product_id}/"
        if city_id:
            url += f"?city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)

    @autotest
    async def delivery_info(
        self,
        store_id: str,
        product_id: int,
        mode: DeliveryMode = DeliveryMode.STORE,
        include_restrict: bool = True,
    ):
        # TODO
        url = f"{self._parent.DELIVERY_API_URL}/catalog/v2/stores/{store_id}/products/{product_id}?mode={mode}&include_restrict={str(include_restrict).lower()}"
        return await self._parent._request(HttpMethod.GET, url)
