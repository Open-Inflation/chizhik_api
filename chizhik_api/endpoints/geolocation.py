"""Геолокация"""

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from human_requests import ApiChild, ApiParent, api_child_field, autotest
from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI  # noqa: F401


@dataclass(init=False)
class ClassGeolocation(ApiChild["ChizhikAPI"]):
    """Методы для работы с геолокацией и выбором магазинов.

    Включает получение информации о городах, адресах, поиск магазинов
    и управление настройками доставки.
    """

    Shop: ShopService = api_child_field(lambda parent: ShopService(parent.parent))
    """Сервис для работы с информацией о магазинах."""


    def __init__(self, parent: "ChizhikAPI"):
        super().__init__(parent)
        ApiParent.__post_init__(self)

    @autotest
    async def cities_list(self, search_name: str, page: int = 1) -> FetchResponse:
        """Получить список городов по частичному совпадению имени."""
        return await self._parent._request(
            HttpMethod.GET,
            f"{self._parent.CATALOG_URL}/geo/cities/?name={search_name}&page={page}",
        )

class ShopService(ApiChild["ChizhikAPI"]):
    """Сервис для работы с информацией о магазинах."""

    @autotest
    async def all(self) -> FetchResponse:
        """Получить список всех точек магазинов."""
        url = f"{self._parent.CATALOG_URL}/shops"
        return await self._parent._request(HttpMethod.GET, url)
    
    @autotest
    async def search(self, query: str) -> FetchResponse:
        """Получить список всех точек магазинов."""
        url = f"{self._parent.CATALOG_URL}/shops?term={query}"
        return await self._parent._request(HttpMethod.GET, url)
