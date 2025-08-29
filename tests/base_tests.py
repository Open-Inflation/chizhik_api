import pytest
from chizhik_api import ChizhikAPI
from io import BytesIO


def test_active_inout(schemashot):
    with ChizhikAPI() as API:
        result = API.Advertising.active_inout()
        open("debug.json", "w").write(result.text)
        schemashot.assert_json_match(result.json(), API.Advertising.active_inout)

def test_cities_list(schemashot):
    with ChizhikAPI() as API:
        result = API.Geolocation.cities_list(search_name='ар', page=1)
        schemashot.assert_json_match(result.json(), API.Geolocation.cities_list)

def test_tree(schemashot):
    with ChizhikAPI() as API:
        result = API.Catalog.tree()
        jresult = result.json()
        schemashot.assert_json_match(jresult, API.Catalog.tree)

def test_products_list(schemashot):
    with ChizhikAPI() as API:
        categories = API.Catalog.tree()
        result = API.Catalog.products_list(category_id=categories.json()[0]['id'])
        schemashot.assert_json_match(result.json(), API.Catalog.products_list)

def test_product_info(schemashot):
    with ChizhikAPI() as API:
        categories = API.Catalog.tree()
        products = API.Catalog.products_list(category_id=categories.json()[0]['id'])
        pjson = products.json()
        result = API.Catalog.Product.info(product_id=pjson["items"][0]['id'])
        schemashot.assert_json_match(result.json(), API.Catalog.Product.info)



def test_download_image(schemashot):
    with ChizhikAPI() as API:
        result = API.General.download_image("https://media.chizhik.club/media/backendprod-dpro/categories/icon/Type%D0%AC%D0%9F%D0%91__%D0%92%D0%96-min.png")
