"""Общий (не класифицируемый) функционал"""

from io import BytesIO
from typing import TYPE_CHECKING

import aiohttp

if TYPE_CHECKING:
    from ..manager import ChizhikAPI


class ClassGeneral:
    """Общие методы API Чижика.

    Включает методы для работы с изображениями, формой обратной связи,
    получения информации о пользователе и других общих функций.
    """

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: ChizhikAPI = parent
        self.CATALOG_URL: str = CATALOG_URL

    async def download_image(self, url: str) -> BytesIO:
        """Скачать изображение по URL."""
        async with aiohttp.request("GET", url) as resp:
            body = await resp.read()
            file = BytesIO(body)
            file.name = url.split("/")[-1]
            return file
