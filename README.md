<div align="center">

# Chizhik API *(not official)*

![Tests last run (ISO)](https://img.shields.io/badge/dynamic/json?label=Tests%20last%20run&query=%24.workflow_runs%5B0%5D.updated_at&url=https%3A%2F%2Fapi.github.com%2Frepos%2FOpen-Inflation%2Fchizhik_api%2Factions%2Fworkflows%2Ftests.yml%2Fruns%3Fper_page%3D1%26status%3Dcompleted&logo=githubactions&cacheSeconds=300)
[![Tests](https://github.com/Open-Inflation/chizhik_api/actions/workflows/tests.yml/badge.svg)](https://github.com/Open-Inflation/chizhik_api/actions/workflows/tests.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chizhik_api)
![PyPI - Package Version](https://img.shields.io/pypi/v/chizhik_api?color=blue)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/chizhik_api?label=PyPi%20downloads)](https://pypi.org/project/chizhik-api/)
[![License](https://img.shields.io/github/license/Open-Inflation/chizhik_api)](https://github.com/Open-Inflation/chizhik_api/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/792572437292253224?label=Discord&labelColor=%232c2f33&color=%237289da)](https://discord.gg/UnJnGHNbBp)
[![Telegram](https://img.shields.io/badge/Telegram-24A1DE)](https://t.me/miskler_dev)


Chizhik (Чижик) - https://chizhik.club/

**[⭐ Star us on GitHub](https://github.com/Open-Inflation/chizhik_api)** | **[📚 Read the Docs](https://open-inflation.github.io/chizhik_api/quick_start)** | **[🐛 Report Bug](https://github.com/Open-Inflation/chizhik_api/issues)**

### Принцип работы

</div>

> Библиотека полностью повторяет сетевую работу обычного пользователя на сайте.

<div align="center">

## Usage:

</div>

```bash
pip install chizhik_api
python -m camoufox fetch
```

```py
from chizhik_api import ChizhikAPI

async def main():
    # RUS: Использование проксирования опционально. Вы можете создать несколько агентов с разными прокси для ускорения парса.
    # ENG: Proxy usage is optional. You can create multiple agents with different proxies for faster parsing.
    async with ChizhikAPI(proxy="user:password@host:port", headless=False) as API:
        # RUS: Выводит активные предложения магазина
        # ENG: Outputs active offers of the store
        print(f"Active offers output: {(await API.Advertising.active_inout()).json()!s:.100s}...\n")
        
        # RUS: Выводит список городов соответствующих поисковому запросу (только на русском языке)
        # ENG: Outputs a list of cities corresponding to the search query (only in Russian language)
        city_list = (await API.Geolocation.cities_list(search_name='ар', page=1)).json()
        print(f"Cities list output: {city_list!s:.100s}...\n")
        # Счет страниц с единицы / index starts from 1

        # RUS: Выводит список всех категорий на сайте
        # ENG: Outputs a list of all categories on the site
        catalog = (await API.Catalog.tree()).json()
        print(f"Categories list output: {catalog!s:.100s}...\n")

        # RUS: Выводит список всех товаров выбранной категории (ограничение 100 элементов, если превышает - запрашивайте через дополнительные страницы)
        # ENG: Outputs a list of all items in the selected category (limiting to 100 elements, if exceeds - request through additional pages)
        items = (await API.Catalog.products_list(category_id=catalog[0]['id'], page=1)).json()
        print(f"Items list output: {items!s:.100s}...\n")
        # Счет страниц с единицы / index starts from 1

        # RUS: Сохраняем изображение с сервера (в принципе, сервер отдал бы их и без обертки моего объекта, но лучше максимально претворяться обычным пользователем)
        # ENG: Saving an image from the server (in fact, the server gave them and without wrapping my object, but better to be as a regular user)
        image = await API.General.download_image(items['items'][0]['images'][0]['image'])
        with open(image.name, 'wb') as f:
            f.write(image.read())

import asyncio
asyncio.run(main())
```

Для более подробной информации смотрите референсы [документации](https://open-inflation.github.io/chizhik_api/quick_start).

---

<div align="center">

### Report

If you have any problems using it / suggestions, do not hesitate to write to the [project's GitHub](https://github.com/Open-Inflation/chizhik_api/issues)!

</div>
