from typing import Any, Optional

import httpx

SIZE_POOL_httpx = 100


class Singletonhttpx:
    httpx_client: Optional[httpx.AsyncClient] = None

    @classmethod
    def get_httpx_client(cls) -> httpx.AsyncClient:
        if cls.httpx_client is None:
            timeout = httpx.Timeout(timeout=5)
            limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
            cls.httpx_client = httpx.AsyncClient(
                timeout=timeout,
                limits=limits,
                http2=True,
            )

        return cls.httpx_client

    @classmethod
    async def close_httpx_client(cls) -> None:
        if cls.httpx_client:
            await cls.httpx_client.aclose()
            cls.httpx_client = None

    @classmethod
    async def send_data_to_facebook(cls, pixel: str, token: str, data: dict) -> Any:
        client = cls.get_httpx_client()
        url = f"https://graph.facebook.com/v17.0/{pixel}/events?access_token={token}"
        try:
            response = await client.post(url, json=data)
            if response.status_code != 200:
                return {"Произошла ошибка" + str(await response.text())}
            json_result = response.json()
        except Exception as e:
            return {"Ошибка": e}

        return json_result


async def on_start_up() -> None:
    Singletonhttpx.get_httpx_client()


async def on_shutdown() -> None:
    await Singletonhttpx.close_httpx_client()
