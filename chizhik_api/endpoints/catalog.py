"""Работа с каталогом"""

from typing import TYPE_CHECKING, Optional

from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI


class ClassCatalog:
    """Методы для работы с каталогом товаров.

    Включает поиск товаров, получение информации о категориях,
    работу с фидами товаров и отзывами.
    """

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: "ChizhikAPI" = parent
        self.CATALOG_URL: str = CATALOG_URL
        self.Product: ProductService = ProductService(
            parent=self._parent, CATALOG_URL=CATALOG_URL
        )
        """Сервис для работы с товарами в каталоге."""

    async def tree(self, city_id: Optional[str] = None) -> FetchResponse:
        """Получить дерево категорий."""
        url = f"{self.CATALOG_URL}/catalog/unauthorized/categories/"
        if city_id:
            url += f"?city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)

    async def products_list(
        self, category_id: int, page: int = 1, city_id: Optional[str] = None
    ) -> FetchResponse:
        """Получить список продуктов в категории."""
        url = f"{self.CATALOG_URL}/catalog/unauthorized/products/?page={page}&category_id={category_id}"
        if city_id:
            url += f"&city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)


class ProductService:
    """Сервис для работы с товарами в каталоге."""

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: "ChizhikAPI" = parent
        self.CATALOG_URL: str = CATALOG_URL

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

        url = f"{self.CATALOG_URL}/catalog/unauthorized/products/{product_id}/"
        if city_id:
            url += f"?city_id={city_id}"
        return await self._parent._request(HttpMethod.GET, url)
