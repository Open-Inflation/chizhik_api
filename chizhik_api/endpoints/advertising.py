"""Реклама"""

from typing import TYPE_CHECKING

from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI


class ClassAdvertising:
    """Методы для работы с рекламными материалами Перекрёстка.

    Включает получение баннеров, слайдеров, буклетов и другого рекламного контента.
    """

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: "ChizhikAPI" = parent
        self.CATALOG_URL: str = CATALOG_URL

    async def active_inout(self) -> FetchResponse:
        """Получить активные рекламные баннеры."""
        return await self._parent._request(
            HttpMethod.GET, f"{self.CATALOG_URL}/catalog/unauthorized/active_inout/"
        )
