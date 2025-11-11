"""Геолокация"""

from typing import TYPE_CHECKING

from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI


class ClassGeolocation:
    """Методы для работы с геолокацией и выбором магазинов.

    Включает получение информации о городах, адресах, поиск магазинов
    и управление настройками доставки.
    """

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: ChizhikAPI = parent
        self.CATALOG_URL: str = CATALOG_URL

    async def cities_list(self, search_name: str, page: int = 1) -> FetchResponse:
        """Получить список городов по частичному совпадению имени."""
        return await self._parent._request(
            HttpMethod.GET,
            f"{self.CATALOG_URL}/geo/cities/?name={search_name}&page={page}",
        )
