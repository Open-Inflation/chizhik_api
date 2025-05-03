import pytest
from chizhik_api import Chizhik
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
    async with Chizhik() as API:
        result = await API.active_inout()
        snapshot.assert_match(gen_schema(result), "active_inout")
    
@pytest.mark.asyncio
async def test_cities_list(snapshot: SnapshotTest):
    async with Chizhik() as API:
        result = await API.cities_list(search_name='ар', page=1)
        snapshot.assert_match(gen_schema(result), "cities_list")

@pytest.mark.asyncio
async def test_categories_list(snapshot: SnapshotTest):
    async with Chizhik() as API:
        result = await API.categories_list()
        snapshot.assert_match(gen_schema(result), "categories_list")

@pytest.mark.asyncio
async def test_products_list(snapshot: SnapshotTest):
    async with Chizhik() as API:
        categories = await API.categories_list()
        result = await API.products_list(category_id=categories[0]['id'])
        snapshot.assert_match(gen_schema(result), "products_list")

@pytest.mark.asyncio
async def test_download_image(snapshot: SnapshotTest):
    async with Chizhik() as API:
        result = await API.download_image("https://media.chizhik.club/media/backendprod-dpro/categories/icon/Type%D0%AC%D0%9F%D0%91__%D0%92%D0%96-min.png")
        assert isinstance(result, BytesIO)
        assert result.getvalue()
    snapshot.assert_match("image downloaded", "download_image")

@pytest.mark.asyncio
async def test_set_debug(snapshot: SnapshotTest):
    async with Chizhik(debug=True) as API:
        API.debug = False
        snapshot.assert_match("debug mode toggled", "set_debug")

@pytest.mark.asyncio
async def test_rebuild_connection(snapshot: SnapshotTest):
    async with Chizhik(debug=True) as API:
        await API.rebuild_connection()
        snapshot.assert_match("connection has been rebuilt", "rebuild_connection")
