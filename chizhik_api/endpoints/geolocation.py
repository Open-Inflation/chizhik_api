"""Геолокация"""
import hrequests


class ClassGeolocation:
    """Методы для работы с геолокацией и выбором магазинов.
    
    Включает получение информации о городах, адресах, поиск магазинов
    и управление настройками доставки.
    """
    def __init__(self, parent, CATALOG_URL: str):
        self._parent = parent
        self.CATALOG_URL = CATALOG_URL

    def cities_list(self, search_name: str, page: int = 1) -> hrequests.Response:
        """Получить список городов по частичному совпадению имени."""
        return self._parent._request("GET", f"{self.CATALOG_URL}/geo/cities/?name={search_name}&page={page}")