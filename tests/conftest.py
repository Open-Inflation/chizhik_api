# conftest.py
import os

import pytest

from chizhik_api import ChizhikAPI


def _dump_debug(name: str, resp) -> None:
    """Опциональный дамп ответа для отладки, если выставлен CHIZHIK_DEBUG=1."""
    if os.getenv("CHIZHIK_DEBUG") == "1":
        try:
            with open(f"debug_{name}.json", "w", encoding="utf-8") as f:
                f.write(resp.text)
        except Exception:
            pass


@pytest.fixture(scope="session")
def api():
    """
    Открываем один экземпляр клиента на всю сессию тестов.
    Корректно зовём менеджер контекста вручную.
    """
    client = ChizhikAPI()
    client.__enter__()  # эквивалент 'with ChizhikAPI() as api'
    try:
        yield client
    finally:
        client.__exit__(None, None, None)


@pytest.fixture(scope="session")
def tree_json(api):
    """Кэш дерева категорий на сессию."""
    resp = api.Catalog.tree()
    _dump_debug("tree", resp)
    data = resp.json()
    if not data:
        pytest.skip("Пустое дерево категорий")
    return data


@pytest.fixture(scope="session")
def first_category_id(tree_json):
    """id первой категории из дерева."""
    return tree_json[0]["id"]


@pytest.fixture(scope="session")
def products_list_json(api, first_category_id):
    """Кэш списка товаров по первой категории."""
    resp = api.Catalog.products_list(category_id=first_category_id)
    _dump_debug("products_list", resp)
    data = resp.json()
    items = data.get("items") or []
    if not items:
        pytest.skip("В категории нет товаров")
    return data


@pytest.fixture(scope="session")
def first_product_id(products_list_json):
    """id первого товара из списка."""
    return products_list_json["items"][0]["id"]
