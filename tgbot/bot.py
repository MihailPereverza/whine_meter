import asyncio
import os

import httpx

backend_url = os.getenv("BACKEND_URL")


async def ask_backend():
    async with httpx.AsyncClient(base_url=backend_url) as client:
        response = await client.get("/info")
        print(response.content)


asyncio.run(ask_backend())
