"""Общий (не класифицируемый) функционал"""

from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

from aiohttp_retry import ExponentialRetry, RetryClient
from human_requests import ApiChild
from human_requests.abstraction import Proxy

if TYPE_CHECKING:
    from ..manager import ChizhikAPI  # noqa: F401


class ClassGeneral(ApiChild["ChizhikAPI"]):
    """Общие методы API Чижика.

    Включает методы для работы с изображениями, формой обратной связи,
    получения информации о пользователе и других общих функций.
    """

    async def download_image(
        self, url: str, retry_attempts: int = 3, timeout: float = 10
    ) -> BytesIO:
        """Скачать изображение по URL."""
        retry_options = ExponentialRetry(
            attempts=retry_attempts, start_timeout=3.0, max_timeout=timeout
        )

        async with RetryClient(retry_options=retry_options) as retry_client:
            async with retry_client.get(
                url,
                raise_for_status=True,
                proxy=Proxy(self._parent.proxy).as_str(),
            ) as resp:
                body = await resp.read()
                file = BytesIO(body)
                file.name = url.split("/")[-1]
        return file
