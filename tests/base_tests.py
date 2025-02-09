import pytest
import chizhik_api
from io import BytesIO
from snapshottest.pytest import SnapshotTest

def gen_schema(data):
    """Генерирует схему (типы данных вместо значений)."""
    if isinstance(data, dict):
        return {k: gen_schema(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [gen_schema(data[0])] if data else []
    else:
        return type(data).__name__

@pytest.mark.asyncio
async def test_active_inout(snapshot: SnapshotTest):
    result = await chizhik_api.active_inout()
    snapshot.assert_match(gen_schema(result), "active_inout")

@pytest.mark.asyncio
async def test_cities_list(snapshot: SnapshotTest):
    result = await chizhik_api.cities_list(search_name='ар', page=1)
    snapshot.assert_match(gen_schema(result), "cities_list")

@pytest.mark.asyncio
async def test_categories_list(snapshot: SnapshotTest):
    result = await chizhik_api.categories_list()
    snapshot.assert_match(gen_schema(result), "categories_list")

@pytest.mark.asyncio
async def test_products_list(snapshot: SnapshotTest):
    categories = await chizhik_api.categories_list()
    result = await chizhik_api.products_list(category_id=categories[0]['id'])
    snapshot.assert_match(gen_schema(result), "products_list")
@pytest.mark.asyncio
async def test_download_image(snapshot: SnapshotTest):
    result = await chizhik_api.download_image("https://media.chizhik.club/media/backendprod-dpro/categories/icon/Type%D0%AC%D0%9F%D0%91__%D0%92%D0%96-min.png")
    assert isinstance(result, BytesIO)
    assert result.getvalue()
    snapshot.assert_match("image downloaded", "download_image")

@pytest.mark.asyncio
async def test_set_debug(snapshot: SnapshotTest):
    chizhik_api.set_debug(True)
    chizhik_api.set_debug(False)
    snapshot.assert_match("debug mode toggled", "set_debug")
