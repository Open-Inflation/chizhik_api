from .api import ChizhikAPI
from io import BytesIO


CATALOG_URL = "https://app.chizhik.club/api/v1"


Chizhik = ChizhikAPI(debug=False)


async def categories_list(city_id: str = None) -> dict:
    url = f"{CATALOG_URL}/catalog/unauthorized/categories/"
    if city_id: url += f"?city_id={city_id}"
    return await Chizhik.request(url)

async def products_list(category_id: int, page: int = 1, city_id: str = None) -> dict:
    url = f"{CATALOG_URL}/catalog/unauthorized/products/?page={page}&category_id={category_id}"
    if city_id: url += f"&city_id={city_id}"
    return await Chizhik.request(url)

async def cities_list(search_name: str, page: int = 1) -> dict:
    return await Chizhik.request(f"{CATALOG_URL}/geo/cities/?name={search_name}&page={page}")

async def active_inout() -> dict:
    return await Chizhik.request(f"{CATALOG_URL}/catalog/unauthorized/active_inout/")

async def download_image(url: str) -> BytesIO:
    return await Chizhik.request(url=url, is_image=True)
    

def set_debug(debug: bool) -> None:
    Chizhik.debug = debug
