"""Общий (не класифицируемый) функционал"""

import hrequests


class ClassGeneral:
    """Общие методы API Перекрёстка.

    Включает методы для работы с изображениями, формой обратной связи,
    получения информации о пользователе и других общих функций.
    """

    def __init__(self, parent, CATALOG_URL: str):
        self._parent = parent
        self.CATALOG_URL = CATALOG_URL

    def download_image(self, url: str) -> hrequests.Response:
        """Скачать изображение по URL."""
        return self._parent._request("GET", url=url)
