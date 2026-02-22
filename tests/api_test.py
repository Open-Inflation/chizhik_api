from typing import Any

import aiohttp
import pytest
from human_requests import autotest_depends_on, autotest_hook, autotest_params
from human_requests.abstraction import Proxy
from human_requests.autotest import AutotestCallContext, AutotestContext
from PIL import Image

from chizhik_api import ChizhikAPI
from chizhik_api.endpoints.catalog import ClassCatalog, ProductService
from chizhik_api.endpoints.geolocation import ClassGeolocation


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Переопределяет фикстуру anyio_backend, чтобы использовать asyncio
    для всей сессии, устраняя ScopeMismatch с фикстурой 'api'.
    """
    return "asyncio"


async def test_proxy_ip():
    from chizhik_api.manager import _pick_https_proxy

    proxy = _pick_https_proxy()

    if not proxy:
        pytest.skip("Proxy not configured")

    prx = Proxy(proxy)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://httpbin.org/ip", proxy=prx.as_str()) as resp:
            ip = (await resp.json())["origin"]

    assert (
        ip == prx._server.removeprefix("http://").removeprefix("https://").split(":")[0]
    )


@pytest.fixture(scope="session")
async def api():
    """Фикстура для инициализации API в рамках сессии."""
    async with ChizhikAPI() as api_instance:
        yield api_instance


@autotest_hook(target=ClassCatalog.tree)
def _capture_first_category(
    _resp: Any,
    data: list[dict[str, Any]],
    ctx: AutotestContext,
) -> None:
    if not isinstance(data, list) or not data:
        pytest.fail("Catalog.tree returned empty data.")

    category_id = data[0].get("id")
    if not isinstance(category_id, int):
        pytest.fail("Catalog.tree did not return a valid category id.")

    ctx.state["autotest_category_id"] = category_id


@autotest_depends_on(ClassCatalog.tree)
@autotest_params(target=ClassCatalog.products_list)
def _products_list_params(ctx: AutotestCallContext) -> dict[str, Any]:
    category_id = ctx.state.get("autotest_category_id")
    if isinstance(category_id, int):
        return {"category_id": category_id, "search": "кола"}
    pytest.fail("Catalog.products_list depends on Catalog.tree.")


@autotest_params(target=ClassGeolocation.cities_list)
def _cities_list_params(_ctx: AutotestCallContext) -> dict[str, Any]:
    return {"search_name": "ар", "page": 1}


@autotest_hook(target=ClassCatalog.products_list)
def _capture_first_product(
    _resp: Any,
    data: dict[str, Any],
    ctx: AutotestContext,
) -> None:
    if not isinstance(data, dict):
        pytest.fail("Catalog.products_list returned invalid payload.")

    items = data.get("items")
    if not isinstance(items, list) or not items:
        pytest.fail("Catalog.products_list returned empty products list.")

    product_id = items[0].get("id")
    if not isinstance(product_id, int):
        pytest.fail("Catalog.products_list did not return a valid product id.")

    ctx.state["autotest_product_id"] = product_id


@autotest_depends_on(ClassCatalog.products_list)
@autotest_params(target=ProductService.info)
def _product_info_params(ctx: AutotestCallContext) -> dict[str, int]:
    product_id = ctx.state.get("autotest_product_id")
    if isinstance(product_id, int):
        return {"product_id": product_id}
    pytest.fail("ProductService.info depends on Catalog.products_list.")


async def test_download_image(api):
    url = (
        "https://chizhik.x5static.net/media/chizhik-assets/categories/icon/"
        "Type%D0%9C%D0%BE%D0%BB%D0%BE%D1%87%D0%BD%D1%8B%D0%B5_"
        "%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B.png"
    )
    resp = await api.General.download_image(url)

    with Image.open(resp) as img:
        fmt = img.format.lower()
    assert fmt in ("png", "jpeg", "webp")
