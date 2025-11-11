"""Общий (не класифицируемый) функционал"""

from human_requests.abstraction import FetchResponse, HttpMethod
import aiohttp
from io import FileIO

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..manager import ChizhikAPI


class ClassGeneral:
    """Общие методы API Перекрёстка.

    Включает методы для работы с изображениями, формой обратной связи,
    получения информации о пользователе и других общих функций.
    """

    def __init__(self, parent: "ChizhikAPI", CATALOG_URL: str):
        self._parent: ChizhikAPI = parent
        self.CATALOG_URL: str = CATALOG_URL

    async def download_image(self, url: str) -> FileIO:
        """Скачать изображение по URL."""
        result = await aiohttp.request
