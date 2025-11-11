"""Общий (не класифицируемый) функционал"""

from io import BytesIO
from typing import TYPE_CHECKING
from aiohttp_retry import RetryClient, ExponentialRetry


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

    async def download_image(self,
                             url: str,
                             retry_attempts: int = 3,
                             timeout: float = 10) -> BytesIO:
        """Скачать изображение по URL."""
        retry_options = ExponentialRetry(attempts=retry_attempts, start_timeout=3.0, max_timeout=timeout)
    
        async with RetryClient(retry_options=retry_options) as retry_client:
            async with retry_client.get(url) as resp:
                resp.raise_for_status() 
                
                body = await resp.read()
                file = BytesIO(body)
                file.name = url.split("/")[-1]
        return file
