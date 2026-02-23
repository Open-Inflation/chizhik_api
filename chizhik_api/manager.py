from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from camoufox.async_api import AsyncCamoufox
from human_requests import (
    ApiParent,
    HumanBrowser,
    HumanContext,
    HumanPage,
    api_child_field,
)
from human_requests.abstraction import FetchResponse, HttpMethod, Proxy
from playwright.async_api import TimeoutError as PWTimeoutError

from .endpoints.advertising import ClassAdvertising
from .endpoints.catalog import ClassCatalog
from .endpoints.general import ClassGeneral
from .endpoints.geolocation import ClassGeolocation


@dataclass
class ChizhikAPI(ApiParent):
    """
    Клиент Чижика.
    """

    timeout_ms: float = 10000.0
    """Время ожидания ответа от сервера в миллисекундах."""
    headless: bool = True
    """Запускать браузер в headless режиме?"""
    proxy: str | dict | Proxy | None = field(default_factory=Proxy.from_env)
    """Прокси-сервер для всех запросов (если нужен). По умолчанию берет из окружения (если есть).
    Принимает как формат Playwright, так и строчный формат."""
    browser_opts: dict[str, Any] = field(default_factory=dict)
    """Дополнительные опции для браузера (см. https://camoufox.com/python/installation/)"""
    CATALOG_URL: str = "https://app.chizhik.club/api/v1"
    """URL для работы с каталогом."""
    MAIN_SITE_URL: str = "https://chizhik.club/catalog/"
    """URL главной страницы сайта."""
    MAIN_SITE_ORIGIN: str = "https://chizhik.club/"

    # будет создана в __post_init__
    session: HumanBrowser = field(init=False, repr=False)
    """Внутренняя сессия браузера для выполнения HTTP-запросов."""
    # будет создано в warmup
    ctx: HumanContext = field(init=False, repr=False)
    """Внутренний контекст сессии браузера"""
    page: HumanPage = field(init=False, repr=False)
    """Внутренний страница сессии браузера"""

    Geolocation: ClassGeolocation = api_child_field(ClassGeolocation)
    """API для работы с геолокацией."""
    Catalog: ClassCatalog = api_child_field(ClassCatalog)
    """API для работы с каталогом товаров."""
    Advertising: ClassAdvertising = api_child_field(ClassAdvertising)
    """API для работы с рекламой."""
    General: ClassGeneral = api_child_field(ClassGeneral)
    """API для работы с общими функциями."""

    async def __aenter__(self):
        """Вход в контекстный менеджер с автоматическим прогревом сессии."""
        await self._warmup()
        return self

    # Прогрев сессии (headless ➜ cookie `session` ➜ accessToken)
    async def _warmup(self) -> None:
        """Прогрев сессии через браузер для получения человекоподобности."""
        px = self.proxy if isinstance(self.proxy, Proxy) else Proxy(self.proxy)
        br = await AsyncCamoufox(
            headless=self.headless,
            proxy=px.as_dict(),
            **self.browser_opts,
            block_images=True,
        ).start()

        self.session = HumanBrowser.replace(br)
        self.ctx = await self.session.new_context()
        self.page = await self.ctx.new_page()
        await self.page.goto(self.CATALOG_URL, wait_until="networkidle")

        ok = False
        try_count = 3
        while not ok and try_count > 0:
            try_count -= 1
            try:
                await self.page.wait_for_selector(
                    "pre", timeout=self.timeout_ms, state="attached"
                )
                ok = True
            except PWTimeoutError:
                await self.page.reload()
        if not ok:
            raise RuntimeError(await self.page.content())

        # await self.page.wait_for_load_state("networkidle")
        # await asyncio.sleep(3)

    async def __aexit__(self, *exc):
        """Выход из контекстного менеджера с закрытием сессии."""
        await self.close()

    async def close(self):
        """Закрыть HTTP-сессию и освободить ресурсы."""
        await self.session.close()

    async def _request(
        self,
        method: HttpMethod,
        url: str,
        *,
        json_body: Any | None = None,
    ) -> FetchResponse:
        """Выполнить HTTP-запрос через внутреннюю сессию.

        Единая точка входа для всех HTTP-запросов библиотеки.
        Добавляет к ответу объект Request для совместимости.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
            url: URL для запроса
            json_body: Тело запроса в формате JSON (опционально)
        """
        resp: FetchResponse = await self.page.fetch(
            url=url,
            method=method,
            body=json_body,
            credentials="same-origin",
            mode="cors",
            timeout_ms=self.timeout_ms,
            referrer=self.MAIN_SITE_ORIGIN,
            headers={"Accept": "application/json, text/plain, */*"},
        )

        return resp
