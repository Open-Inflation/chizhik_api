# Chizhik API *(not official / не официальный)*

Chizhik (Чижик) - https://chizhik.club/

[![GitHub Actions](https://github.com/Open-Inflation/chizhik_api/workflows/API%20Tests%20Daily/badge.svg)](https://github.com/Open-Inflation/chizhik_api/actions?query=workflow%3A"API+Tests+Daily?query=branch%3Amain")
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chizhik_api)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/chizhik_api?label=PyPi%20downloads)](https://pypi.org/project/chizhik-api/)
[![Discord](https://img.shields.io/discord/792572437292253224?label=Discord&labelColor=%232c2f33&color=%237289da)](https://discord.gg/UnJnGHNbBp)
[![Telegram](https://img.shields.io/badge/Telegram-24A1DE)](https://t.me/miskler_dev)



## Installation:
1. Install package:
```bash
pip install chizhik_api
python -m hrequests install
```

### Usage:
```py
from chizhik_api import ChizhikAPI

def main():
    # RUS: Использование проксирования опционально. Вы можете создать несколько агентов с разными прокси для ускорения парса.
    # ENG: Proxy usage is optional. You can create multiple agents with different proxies for faster parsing.
    with ChizhikAPI(proxy="user:password@host:port", headless=False) as API:
        # RUS: Выводит активные предложения магазина
        # ENG: Outputs active offers of the store
        print(f"Active offers output: {API.Advertising.active_inout().json()!s:.100s}...\n")

        # RUS: Выводит список городов соответствующих поисковому запросу (только на русском языке)
        # ENG: Outputs a list of cities corresponding to the search query (only in Russian language)
        city_list = API.Geolocation.cities_list(search_name='ар', page=1).json()
        print(f"Cities list output: {city_list!s:.100s}...\n")
        # Счет страниц с единицы / index starts from 1

        # RUS: Выводит список всех категорий на сайте
        # ENG: Outputs a list of all categories on the site
        catalog = API.Catalog.tree().json()
        print(f"Categories list output: {catalog!s:.100s}...\n")

        # RUS: Выводит список всех товаров выбранной категории (ограничение 100 элементов, если превышает - запрашивайте через дополнительные страницы)
        # ENG: Outputs a list of all items in the selected category (limiting to 100 elements, if exceeds - request through additional pages)
        items = API.Catalog.products_list(category_id=catalog[0]['id'], page=1).json()
        print(f"Items list output: {items!s:.100s}...\n")
        # Счет страниц с единицы / index starts from 1

        # RUS: Сохраняем изображение с сервера (в принципе, сервер отдал бы их и без обертки моего объекта, но лучше максимально претворяться обычным пользователем)
        # ENG: Saving an image from the server (in fact, the server gave them and without wrapping my object, but better to be as a regular user)
        image = API.General.download_image(items['items'][0]['images'][0]['image'])
        with open(image.url.split("/")[-1], 'wb') as f:
            f.write(image.content)

if __name__ == '__main__':
    main()
```

### Report / Обратная связь

If you have any problems using it /suggestions, do not hesitate to write to the [project's GitHub](https://github.com/Open-Inflation/chizhik_api/issues)!
