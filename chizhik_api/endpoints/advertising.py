"""Реклама"""

import hrequests

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..manager import ChizhikAPI


class ClassAdvertising:
    """Методы для работы с рекламными материалами Перекрёстка.

    Включает получение баннеров, слайдеров, буклетов и другого рекламного контента.
    """

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: "ChizhikAPI" = parent
        self.CATALOG_URL: str = CATALOG_URL

    def active_inout(self) -> hrequests.Response:
        """Получить активные рекламные баннеры."""
        return self._parent._request(
            "GET", f"{self.CATALOG_URL}/catalog/unauthorized/active_inout/"
        )
