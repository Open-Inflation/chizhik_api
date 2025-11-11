# test_api.py
import os

import pytest
from PIL import Image

from chizhik_api import ChizhikAPI


def _dump_debug(name: str, resp) -> None:
    """Опциональный дамп ответа для отладки, если выставлен CHIZHIK_DEBUG=1."""
    if os.getenv("CHIZHIK_DEBUG") == "1":
        try:
            with open(f"debug_{name}.json", "w", encoding="utf-8") as f:
                f.write(resp.text)
        except Exception:
            pass


@pytest.mark.asyncio
async def test_active_inout(schemashot):
    async with ChizhikAPI() as api:
        resp = await api.Advertising.active_inout()
        schemashot.assert_json_match(resp.json(), api.Advertising.active_inout)


@pytest.mark.asyncio
async def test_cities_list(schemashot):
    async with ChizhikAPI() as api:
        resp = await api.Geolocation.cities_list(search_name="ар", page=1)
        schemashot.assert_json_match(resp.json(), api.Geolocation.cities_list)


@pytest.mark.asyncio
async def test_tree(schemashot):
    async with ChizhikAPI() as api:
        resp = await api.Catalog.tree()
        _dump_debug("tree", resp)
        data = resp.json()
        if not data:
            pytest.skip("Пустое дерево категорий")
        schemashot.assert_json_match(data, api.Catalog.tree)


@pytest.mark.asyncio
async def test_products_list(schemashot):
    async with ChizhikAPI() as api:
        # Получаем дерево категорий для извлечения first_category_id
        tree_resp = await api.Catalog.tree()
        _dump_debug("tree", tree_resp)
        tree_data = tree_resp.json()
        if not tree_data:
            pytest.skip("Пустое дерево категорий")
        first_category_id = tree_data[0]["id"]

        # Теперь получаем список продуктов
        resp = await api.Catalog.products_list(category_id=first_category_id)
        _dump_debug("products_list", resp)
        data = resp.json()
        items = data.get("items") or []
        if not items:
            pytest.skip("В категории нет товаров")
        schemashot.assert_json_match(data, api.Catalog.products_list)


@pytest.mark.asyncio
async def test_product_info(schemashot):
    async with ChizhikAPI() as api:
        # Получаем дерево категорий для извлечения first_category_id
        tree_resp = await api.Catalog.tree()
        _dump_debug("tree", tree_resp)
        tree_data = tree_resp.json()
        if not tree_data:
            pytest.skip("Пустое дерево категорий")
        first_category_id = tree_data[0]["id"]

        # Получаем список продуктов для извлечения first_product_id
        products_resp = await api.Catalog.products_list(category_id=first_category_id)
        _dump_debug("products_list", products_resp)
        products_data = products_resp.json()
        items = products_data.get("items") or []
        if not items:
            pytest.skip("В категории нет товаров")
        first_product_id = items[0]["id"]

        # Теперь получаем информацию о продукте
        resp = await api.Catalog.Product.info(product_id=first_product_id)
        schemashot.assert_json_match(resp.json(), api.Catalog.Product.info)


@pytest.mark.asyncio
async def test_download_image():
    async with ChizhikAPI() as api:
        url = "https://chizhik.x5static.net/media/chizhik-assets/product_images/3060608.jpg"
        resp = await api.General.download_image(url)

        # Определение формата через Pillow
        with Image.open(resp) as img:
            fmt = img.format.lower()
        assert fmt in ("png", "jpeg", "webp")
