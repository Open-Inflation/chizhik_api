from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

import hrequests
import hrequests.cookies
from requests import Request

from .endpoints.advertising import ClassAdvertising
from .endpoints.catalog import ClassCatalog
from .endpoints.general import ClassGeneral
from .endpoints.geolocation import ClassGeolocation


def _pick_https_proxy() -> str | None:
    """Возвращает прокси из HTTPS_PROXY/https_proxy (если заданы)."""
    return os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")


@dataclass
class ChizhikAPI:
    """
    Клиент Чижика.
    """

    timeout: float = 15.0
    """Время ожидания ответа от сервера."""
    browser: str = "firefox"
    """Используемый браузер: firefox / chrome."""
    headless: bool = True
    """Запускать браузер в headless режиме?"""
    proxy: str | None = field(default_factory=_pick_https_proxy)
    """Прокси-сервер для всех запросов (если нужен). По умолчанию берет из окружения (если есть)"""
    browser_opts: dict[str, Any] = field(default_factory=dict)
    """Дополнительные опции для браузера (см. hrequests.BrowserSession)"""
    CATALOG_URL: str = "https://app.chizhik.club/api/v1"
    """URL для работы с каталогом."""
    MAIN_SITE_URL: str = "https://chizhik.club/catalog/"
    """URL главной страницы сайта."""

    # будет создана в __post_init__
    session: hrequests.BrowserSession = field(init=False, repr=False)
    """Внутренняя сессия для выполнения HTTP-запросов."""

    # ───── lifecycle ─────
    def __post_init__(self) -> None:
        self.session = hrequests.BrowserSession(
            session=hrequests.Session(
                browser=self.browser,
                timeout=self.timeout,
            ),
            browser=self.browser,
            headless=self.headless,
            proxy=self.proxy,
            **self.browser_opts,
        )

        self.Geolocation: ClassGeolocation = ClassGeolocation(self, self.CATALOG_URL)
        self.Catalog: ClassCatalog = ClassCatalog(self, self.CATALOG_URL)
        self.Advertising: ClassAdvertising = ClassAdvertising(self, self.CATALOG_URL)
        self.General: ClassGeneral = ClassGeneral(self, self.CATALOG_URL)

    def __enter__(self):
        """Вход в контекстный менеджер с автоматическим прогревом сессии."""
        # self._warmup()
        return self

    # Прогрев сессии (headless ➜ cookie `session` ➜ accessToken)
    def _warmup(self) -> None:
        """Прогрев сессии через браузер для получения человекоподобности."""
        self.session.goto(self.MAIN_SITE_URL)
        self.session.awaitSelector("next-route-announcer", timeout=self.timeout)

    def __exit__(self, *exc):
        """Выход из контекстного менеджера с закрытием сессии."""
        self.close()

    def close(self):
        """Закрыть HTTP-сессию и освободить ресурсы."""
        self.session.close()

    def _request(
        self,
        method: str,
        url: str,
        *,
        json_body: Any | None = None,
    ) -> hrequests.Response:
        """Выполнить HTTP-запрос через внутреннюю сессию.

        Единая точка входа для всех HTTP-запросов библиотеки.
        Добавляет к ответу объект Request для совместимости.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
            url: URL для запроса
            json_body: Тело запроса в формате JSON (опционально)
        """
        # Единая точка входа в чужую библиотеку для удобства
        resp: hrequests.Response = self.session.request(
            method.upper(), url, data=json_body, timeout=self.timeout
        )

        if hasattr(resp, "request"):
            raise RuntimeError(
                "Response object does have `request` attribute. "
                "This may indicate an update in `hrequests` library."
            )

        ctype = resp.headers.get("content-type", "")
        if "text/html" in ctype:
            # исполним скрипт в браузерном контексте; куки запишутся в сессию
            with resp.render(headless=self.headless, browser=self.browser) as rend:
                rend.awaitSelector(selector="pre", timeout=self.timeout)

                jsn = json.loads(rend.find("pre").text)

                fin_resp = hrequests.Response(
                    url=resp.url,
                    status_code=resp.status_code,
                    headers=resp.headers,
                    cookies=hrequests.cookies.cookiejar_from_dict(
                        self.session.cookies.get_dict()
                    ),
                    raw=json.dumps(jsn, ensure_ascii=True).encode("utf-8"),
                )
        else:
            fin_resp = resp

        fin_resp.request = Request(
            method=method.upper(),
            url=url,
            json=json_body,
        )
        return fin_resp
