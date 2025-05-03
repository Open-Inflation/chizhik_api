from .api import ChizhikAPI
from io import BytesIO


class Chizhik:
    CATALOG_URL = "https://app.chizhik.club/api/v1"

    def __init__(self, debug: bool = False, proxy: str = None):
        self._debug = debug
        self._proxy = proxy

    def __enter__(self):
        raise NotImplementedError("Use `async with Chizhik() as ...:`")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self, debug: bool = None, proxy: str = None):
        if debug is not None:
            self._debug = debug
        if proxy is not None:
            self._proxy = proxy
        self.api = ChizhikAPI(debug=self._debug, proxy=self._proxy)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self) -> None:
        await self.api.close()

    @property
    def debug(self) -> bool:
        """Get or set debug mode. If set to True, it will print debug messages and show browser."""
        return self._debug

    @debug.setter
    def debug(self, value: bool):
        self._debug = value
        self.api.debug = value

    @property
    def proxy(self) -> str:
        return self._proxy

    @proxy.setter
    def proxy(self, value: str):
        self._proxy = value
        self.api.proxy = value

    async def categories_list(self, city_id: str = None) -> dict:
        url = f"{self.CATALOG_URL}/catalog/unauthorized/categories/"
        if city_id: url += f"?city_id={city_id}"
        return await self.api.request(url)

    async def products_list(self, category_id: int, page: int = 1, city_id: str = None) -> dict:
        url = f"{self.CATALOG_URL}/catalog/unauthorized/products/?page={page}&category_id={category_id}"
        if city_id: url += f"&city_id={city_id}"
        return await self.api.request(url)

    async def cities_list(self, search_name: str, page: int = 1) -> dict:
        return await self.api.request(f"{self.CATALOG_URL}/geo/cities/?name={search_name}&page={page}")

    async def active_inout(self) -> dict:
        return await self.api.request(f"{self.CATALOG_URL}/catalog/unauthorized/active_inout/")

    async def download_image(self, url: str) -> BytesIO:
        return await self.api.request(url=url, is_image=True)

    async def rebuild_connection(self) -> None:
        await self.api._new_session()
