import aiohttp
from camoufox.async_api import AsyncCamoufox
import urllib
import asyncio
from io import BytesIO

class ChizhikAPI:
    def __init__(self, debug: bool = False, cookies: dict = {}, proxy: str = None):
        self.debug = debug
        self.cookies = cookies
        self.session_dict = {}
        self._proxy = proxy

    @property
    def proxy(self):
        return self._proxy if hasattr(self, '_proxy') else None

    @proxy.setter
    def proxy(self, value):
        self._proxy = value

    async def _launch_browser(self, url: str) -> dict:
        # TODO: прокси

        async with AsyncCamoufox(headless=not self.debug, proxy=self.proxy, geoip=True) as browser:
            context = await browser.new_context()
            page = await context.new_page()

            # camoufox автоматически внедряет fingerprint-инъекции
            # Получаем fingerprint-заголовки для aiohttp
            try:
                fp_headers = getattr(context, 'fingerprint_headers', None)
                if fp_headers:
                    self.session_dict = dict(fp_headers)
                else:
                    # Получаем реальные значения из браузера
                    user_agent = await page.evaluate('navigator.userAgent')
                    accept_language = await page.evaluate('navigator.language')
                    self.session_dict = {
                        "User-Agent": user_agent,
                        "Accept-Language": accept_language,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1"
                    }
            except Exception:
                if self.debug: print("Unable to get fingerprint headers")

            # Готовим Future и колбэк
            loop = asyncio.get_running_loop()
            response_future = loop.create_future()

            def _on_response(resp):
                full_url = urllib.parse.unquote(resp.url)
                if not (full_url.startswith(url) and resp.request.method == "GET"):
                    return
                ctype = resp.headers.get("content-type", "").lower()
                if "application/json" not in ctype:
                    return
                if not response_future.done():
                    response_future.set_result(resp)

            context.on("response", _on_response)

            async with context.expect_page() as ev:
                await page.evaluate(f"window.open('{url}', '_blank');")
            popup = await ev.value

            resp = await asyncio.wait_for(response_future, timeout=10.0)
            data = await resp.json()

            # Собираем куки
            raw = await context.cookies()
            self.cookies = {
                urllib.parse.unquote(c["name"]): urllib.parse.unquote(c["value"])
                for c in raw
            }

            await browser.close()
            return data

    async def _fetch(self, url: str) -> tuple[bool, dict | BytesIO]:
        """
        Asynchronously fetches data from the specified URL using aiohttp.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            tuple[bool, dict]: A tuple containing a boolean indicating the success of the fetch and a dictionary containing the response data.
                - If the response content type is 'text/html', the function returns (False, {}).
                - If the response content type is 'application/json', the function returns (True, response.json()).

        Raises:
            aiohttp.ClientError: If there was an error connecting to the server.
            Exception: If the response content type is unknown or the response status is 403 (Forbidden) or any other unknown error/status code.
        """
        async with aiohttp.ClientSession() as session:
            if self.debug: print(f"Requesting \"{url}\"... Cookies: {self.cookies}")

            request_kwargs = dict(
                url=url,
                headers=self.session_dict,
                cookies=self.cookies
            )
            if self.proxy:
                request_kwargs['proxy'] = self.proxy

            async with session.get(**request_kwargs) as response:
                if response.status == 200: # 200 OK
                    if self.debug:
                        print(f"Response status: {response.status}, response type: {response.headers['content-type']}")

                    if response.headers['content-type'].startswith('text/html'):
                        if self.debug: print(f"CONTENT: {await response.text()}")
                        return False, {}
                    elif response.headers['content-type'].startswith('application/json'):
                        return True, await response.json()
                    elif response.headers['content-type'].startswith('image'):
                        image_data = BytesIO()
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            image_data.write(chunk)
                        
                        image_data.name = url.split("/")[-1]
                        
                        return True, image_data
                    else:
                        raise Exception(f"Unknown response type: {response.headers['content-type']}")
                elif response.status == 403:  # 403 Forbidden (сервер воспринял как бота)
                    raise Exception("Anti-bot protection. Use Russia IP address and try again.")
                else:
                    raise Exception(f"Response status: {response.status} (unknown error/status code). Please, create issue on GitHub")

    async def request(self, url: str, is_image: bool = False) -> dict | BytesIO | None:
        """
        Asynchronously sends a request to the specified URL using the playwright and aiohttp.

        The function automatically selects a method for sending data based on whether cookies are available.
        If cookies are available, aiohttp is used as the priority method.
        If no cookies are present, the page is opened in a full browser using playwright to create cookies (which takes longer).

        Args:
            url (str): The URL to send the request to.

        Returns:
            dict: A dictionary containing the response data.
            BytesIO: A BytesIO object containing the image data.
            None: If the requesting image failed, the function returns None.
        """
        if len(self.cookies) > 0 or is_image:
            response_ok, response = await self._fetch(url=url)
            if not response_ok:
                if is_image:
                    if self.debug: print('Unable to fetch image :(')
                    return None

                if self.debug: print(f'Unable to fetch: {response}\n\nStarting browser...')
                # Если получен HTML, переходим в браузер
                return await self._launch_browser(url=url) # возвращаем результат из браузера
            else:
                if self.debug: print('Fetched successfully!\n')
                return response
        else:
            if self.debug: print('No cookies found, start browser (maybe first start)...')
            return await self._launch_browser(url=url)
