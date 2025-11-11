import pytest
from PIL import Image
from chizhik_api import ChizhikAPI


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Переопределяет фикстуру anyio_backend, чтобы использовать asyncio 
    для всей сессии, устраняя ScopeMismatch с фикстурой 'api'.
    """
    return 'asyncio' 


@pytest.fixture(scope="session")
async def api():
    """Фикстура для инициализации API в рамках сессии"""
    # anyio автоматически управляет асинхронным контекстным менеджером
    async with ChizhikAPI() as api_instance:
        yield api_instance


@pytest.fixture
async def category_data(api):
    """Фикстура для получения данных категории"""
    tree_resp = await api.Catalog.tree()
    tree_data = tree_resp.json()
    if not tree_data:
        pytest.skip("Пустое дерево категорий")
    return tree_data[0]["id"]


@pytest.fixture
async def product_data(api, category_data):
    """Фикстура для получения данных продукта"""
    products_resp = await api.Catalog.products_list(category_id=category_data)
    products_data = products_resp.json()
    items = products_data.get("items") or []
    if not items:
        pytest.skip("В категории нет товаров")
    return items[0]["id"]


async def test_active_inout(api, schemashot):
    resp = await api.Advertising.active_inout()
    schemashot.assert_json_match(resp.json(), api.Advertising.active_inout)


async def test_cities_list(api, schemashot):
    resp = await api.Geolocation.cities_list(search_name="ар", page=1)
    schemashot.assert_json_match(resp.json(), api.Geolocation.cities_list)


async def test_tree(api, schemashot):
    resp = await api.Catalog.tree()
    data = resp.json()
    if not data:
        pytest.skip("Пустое дерево категорий")
    schemashot.assert_json_match(data, api.Catalog.tree)


async def test_products_list(api, category_data, schemashot):
    resp = await api.Catalog.products_list(category_id=category_data)
    data = resp.json()
    items = data.get("items") or []
    if not items:
        pytest.skip("В категории нет товаров")
    schemashot.assert_json_match(data, api.Catalog.products_list)


async def test_product_info(api, product_data, schemashot):
    resp = await api.Catalog.Product.info(product_id=product_data)
    schemashot.assert_json_match(resp.json(), api.Catalog.Product.info)


async def test_download_image(api):
    url = "https://chizhik.x5static.net/media/chizhik-assets/product_images/3060608.jpg"
    resp = await api.General.download_image(url)
    
    with Image.open(resp) as img:
        fmt = img.format.lower()
    assert fmt in ("png", "jpeg", "webp")
