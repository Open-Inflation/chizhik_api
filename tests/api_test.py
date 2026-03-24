from typing import Any

import pytest
from human_requests import (
    autotest_data,
    autotest_depends_on,
    autotest_hook,
    autotest_params,
)
from human_requests.autotest import (
    AutotestCallContext,
    AutotestContext,
    AutotestDataContext,
)
from PIL import Image

from chizhik_api import ChizhikAPI
from chizhik_api.endpoints.catalog import ClassCatalog, ProductService
from chizhik_api.endpoints.geolocation import ClassGeolocation, ShopService


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Переопределяет фикстуру anyio_backend, чтобы использовать asyncio
    для всей сессии, устраняя ScopeMismatch с фикстурой 'api'.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def api():
    """Фикстура для инициализации API в рамках сессии."""
    async with ChizhikAPI(headless=True, test_mode=True) as api_instance:
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


@autotest_params(target=ShopService.search)
def _capture_shop(ctx: AutotestContext) -> None:
    return {"query": "Москва"}


@autotest_hook(target=ShopService.search)
def _capture_first_store_id(
    _resp: Any,
    data: list[dict[str, Any]],
    ctx: AutotestContext,
) -> None:
    if not isinstance(data, list) or not data:
        pytest.fail("ShopService.search returned empty data.")

    store_id = data[0].get("sap_id")
    if not isinstance(store_id, str):
        pytest.fail("ShopService.search did not return a valid category id.")

    ctx.state["autotest_store_id"] = store_id


@autotest_depends_on(ShopService.search)
@autotest_params(target=ClassCatalog.delivery_tree)
def _delivery_tree(ctx: AutotestContext):
    return {"store_id": ctx.state["autotest_store_id"]}


@autotest_depends_on(ShopService.search)
@autotest_depends_on(ClassCatalog.delivery_tree)
@autotest_params(target=ClassCatalog.delivery_tree_extended)
def _delivery_tree_extended(ctx: AutotestContext):
    return {
        "store_id": ctx.state["autotest_store_id"],
        "category_alias": ctx.state.get("autotest_category_alias"),
    }


@autotest_depends_on(ShopService.search)
@autotest_depends_on(ClassCatalog.delivery_tree)
@autotest_params(target=ClassCatalog.delivery_products_list)
def _delivery_products_list(ctx: AutotestContext):
    return {
        "store_id": ctx.state["autotest_store_id"],
        "category_alias": ctx.state.get("autotest_category_alias"),
    }


@autotest_depends_on(ShopService.search)
@autotest_params(target=ClassCatalog.delivery_search)
def _delivery_search(ctx: AutotestContext):
    return {"store_id": ctx.state["autotest_store_id"], "query": "кола"}


@autotest_hook(target=ClassCatalog.delivery_products_list)
def _capture_first_plu(
    _resp: Any,
    data: list[dict[str, Any]],
    ctx: AutotestContext,
) -> None:
    if not isinstance(data, dict) or not data:
        pytest.fail("ClassCatalog.delivery_products_list returned empty data.")

    store_id = data.get("products")
    if not isinstance(store_id, list):
        pytest.fail(
            "ClassCatalog.delivery_products_list did not return a valid category id."
        )

    ctx.state["autotest_plu"] = store_id[0]["plu"]


@autotest_depends_on(ClassCatalog.delivery_tree)
@autotest_params(target=ProductService.delivery_info)
def _delivery_info(ctx: AutotestContext):
    return {
        "store_id": ctx.state["autotest_store_id"],
        "product_id": ctx.state.get("autotest_plu"),
    }


@autotest_hook(target=ClassCatalog.delivery_tree_extended)
def _capture_first_subcategory_alias(
    _resp: Any,
    data: list[dict[str, Any]],
    ctx: AutotestContext,
) -> None:
    if not isinstance(data, dict) or not data:
        pytest.fail("ShopService.search returned empty data.")

    store_id = data.get("categories_tags")
    if not isinstance(store_id, list) or not store_id:
        pytest.fail("ShopService.search did not return a valid category id.")

    ctx.state["autotest_subcategory_alias"] = store_id[0]["id"]


@autotest_depends_on(ShopService.search)
@autotest_depends_on(ClassCatalog.delivery_tree_extended)
@autotest_params(target=ClassCatalog.delivery_tree_ancestors)
def _delivery_tree_ancestors(ctx: AutotestContext):
    return {
        "store_id": ctx.state["autotest_store_id"],
        "category_alias": ctx.state.get("autotest_subcategory_alias"),
    }


@autotest_depends_on(ClassCatalog.tree)
@autotest_params(target=ClassCatalog.products_list)
def _products_list_params(ctx: AutotestCallContext) -> dict[str, Any]:
    category_id = ctx.state.get("autotest_category_id")
    return {"category_id": category_id, "search": "кола"}


@autotest_hook(target=ClassCatalog.delivery_tree)
def _capture_first_category_alias(
    _resp: Any,
    data: list[dict[str, Any]],
    ctx: AutotestContext,
) -> None:
    if not isinstance(data, list) or not data:
        pytest.fail("Catalog.delivery_tree returned empty data.")

    category_id = data[0].get("id")
    if not isinstance(category_id, str):
        pytest.fail("Catalog.delivery_tree did not return a valid category id.")

    ctx.state["autotest_category_alias"] = category_id


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


@autotest_data(name="unstandard_headers")
def _unstandard_headers_data(ctx: AutotestDataContext) -> dict[str, Any]:
    return ctx.api.unstandard_headers


@autotest_data(name="unstandard_urls")
def _unstandard_urls_data(ctx: AutotestDataContext) -> dict[str, Any]:
    return ctx.api.unstandard_urls


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
