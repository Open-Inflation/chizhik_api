# Chizhik API *(not official / не официальный)*

Chizhik (Чижик) - https://chizhik.club/

[![GitHub Actions](https://github.com/Open-Inflation/chizhik_api/workflows/API%20Tests%20Daily/badge.svg)](https://github.com/Open-Inflation/chizhik_api/actions?query=workflow%3A"API+Tests+Daily?query=branch%3Amain")
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chizhik_api)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/chizhik_api?label=PyPi%20downloads)](https://pypi.org/project/chizhik-api/)
[![Discord](https://img.shields.io/discord/792572437292253224?label=Discord&labelColor=%232c2f33&color=%237289da)](https://discord.gg/UnJnGHNbBp)
[![Telegram](https://img.shields.io/badge/Telegram-24A1DE)](https://t.me/miskler_dev)



## Installation / Установка:
1. Install package / Установка пакета:
```bash
pip install chizhik_api
```
2. ***Debian/Ubuntu Linux***: Install dependencies / Установка зависимостей:
```bash
sudo apt update && sudo apt install -y libgtk-3-0 libx11-xcb1
```
3. Install browser / Установка браузера:
```bash
camoufox fetch
```

### Usage / Использование:
```py
from chizhik_api import Chizhik
import asyncio


async def main():
    # RUS: Использование проксирования опционально. Вы можете создать несколько агентов с разными прокси для ускорения парса.
    # ENG: Proxy usage is optional. You can create multiple agents with different proxies for faster parsing.
    async with Chizhik(proxy="user:password@host:port", debug=False) as API:
        # RUS: Выводит активные предложения магазина
        # ENG: Outputs active offers of the store
        print(f"Active offers output: {await API.active_inout()!s:.100s}...\n")

        # RUS: Выводит список городов соответствующих поисковому запросу (только на русском языке)
        # ENG: Outputs a list of cities corresponding to the search query (only in Russian language)
        print(f"Cities list output: {await API.cities_list(search_name='ар', page=1)!s:.100s}...\n")
        # Счет страниц с единицы / index starts from 1

        # RUS: Выводит список всех категорий на сайте
        # ENG: Outputs a list of all categories on the site
        catalog = await API.categories_list()
        print(f"Categories list output: {catalog!s:.100s}...\n")

        # RUS: Выводит список всех товаров выбранной категории (ограничение 100 элементов, если превышает - запрашивайте через дополнительные страницы)
        # ENG: Outputs a list of all items in the selected category (limiting to 100 elements, if exceeds - request through additional pages)
        items = await API.products_list(category_id=catalog[0]['id'], page=1)
        print(f"Items list output: {items!s:.100s}...\n")
        # Счет страниц с единицы / index starts from 1

        # RUS: Сохраняем изображение с сервера (в принципе, сервер отдал бы их и без обертки моего объекта, но лучше максимально претворяться обычным пользователем)
        # ENG: Saving an image from the server (in fact, the server gave them and without wrapping my object, but better to be as a regular user)
        image = await API.download_image(items['items'][0]['images'][0]['image'])
        with open(image.name, 'wb') as f:
            f.write(image.getvalue())

        # RUS: Если требуется, можно настроить вывод логов в консоль после иницализации
        # ENG: If required, you can configure the output of logs in the console after initialization
        API.debug = True
        await API.products_list(category_id=catalog[0]['id'], page=2)

        # RUS: Так же как и debug, в рантайме можно переназначить прокси
        # ENG: As with debug, you can reassign the proxy in runtime
        API.proxy = "user:password@host:port"
        # RUS: Чтобы применить изменения, нужно пересоздать подключение
        # ENG: To apply changes, you need rebuild connection
        await API.rebuild_connection()
        await API.products_list(category_id=catalog[0]['id'], page=3)


if __name__ == '__main__':
    asyncio.run(main())
```

### Report / Обратная связь

If you have any problems using it /suggestions, do not hesitate to write to the [project's GitHub](https://github.com/Open-Inflation/chizhik_api/issues)!

Если у вас возникнут проблемы в использовании / пожелания, не стесняйтесь писать на [GitHub проекта](https://github.com/Open-Inflation/chizhik_api/issues)!
