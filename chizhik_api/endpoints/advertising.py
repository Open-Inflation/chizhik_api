"""Реклама"""

from __future__ import annotations

from typing import TYPE_CHECKING

from human_requests import ApiChild, autotest
from human_requests.abstraction import FetchResponse, HttpMethod

if TYPE_CHECKING:
    from ..manager import ChizhikAPI  # noqa: F401


class ClassAdvertising(ApiChild["ChizhikAPI"]):
    """Методы для работы с рекламными материалами Перекрёстка.

    Включает получение баннеров, слайдеров, буклетов и другого рекламного контента.
    """

    @autotest
    async def active_inout(self) -> FetchResponse:
        """Получить активные рекламные баннеры."""
        return await self._parent._request(
            HttpMethod.GET,
            f"{self._parent.CATALOG_URL}/catalog/unauthorized/active_inout/",
        )
