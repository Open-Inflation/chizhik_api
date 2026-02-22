"""Геолокация"""

from __future__ import annotations

from typing import TYPE_CHECKING

from human_requests import ApiChild, autotest
from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI  # noqa: F401


class ClassGeolocation(ApiChild["ChizhikAPI"]):
    """Методы для работы с геолокацией и выбором магазинов.

    Включает получение информации о городах, адресах, поиск магазинов
    и управление настройками доставки.
    """

    @autotest
    async def cities_list(self, search_name: str, page: int = 1) -> FetchResponse:
        """Получить список городов по частичному совпадению имени."""
        return await self._parent._request(
            HttpMethod.GET,
            f"{self._parent.CATALOG_URL}/geo/cities/?name={search_name}&page={page}",
        )
