# tests/test_api.py
import pytest


def test_active_inout(api, schemashot):
    resp = api.Advertising.active_inout()
    schemashot.assert_json_match(resp.json(), api.Advertising.active_inout)


def test_cities_list(api, schemashot):
    resp = api.Geolocation.cities_list(search_name="ар", page=1)
    schemashot.assert_json_match(resp.json(), api.Geolocation.cities_list)


def test_tree(api, schemashot, tree_json):
    # уже распарсено фикстурой, но для привязки к callable передаём эталон из API
    schemashot.assert_json_match(tree_json, api.Catalog.tree)


def test_products_list(api, schemashot, products_list_json):
    schemashot.assert_json_match(products_list_json, api.Catalog.products_list)


def test_product_info(api, schemashot, first_product_id):
    resp = api.Catalog.Product.info(product_id=first_product_id)
    schemashot.assert_json_match(resp.json(), api.Catalog.Product.info)


def test_download_image(api):
    resp = api.General.download_image(
        "https://media.chizhik.club/media/backendprod-dpro/categories/icon/Type%D0%AC%D0%9F%D0%91__%D0%92%D0%96-min.png"
    )
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").startswith("image/png")
    assert resp.content.startswith(b"\x89PNG\r\n\x1a\n")
