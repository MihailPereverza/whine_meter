import asyncio

import httpx

from sqlalchemy.testing.plugin.plugin_base import logging


async def calculate_whine(message: str, retrying: bool = False) -> float | None:
    API_URL = "https://api-inference.huggingface.co/models/seara/rubert-tiny2-russian-sentiment"
    headers = {"Authorization": "Bearer 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",
               'x-use-cache': 'true'}

    async def query(payload) -> dict | list:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, headers=headers, json=payload)
            return response.json()

    output = await query({"inputs": message})
    if isinstance(output, dict):
        if retrying:
            logging.error("error when retrying: %s", output)
            return None

        if 'error' in output and 'currently loading' in output['error']:
            # print("time to sleep:", output['estimated_time'])
            await asyncio.sleep(output['estimated_time'])
            return await calculate_whine(message, retrying=True)
        else:
            logging.error("unhandled error: %s", output)
            return None
    elif isinstance(output, list):
        neg = 0
        pos = 0
        for el in output[0]:
            if el['label'] == 'negative':
                neg = el['score']
            if el['label'] == 'positive':
                pos = el['score']
        return max(0, neg - pos)
    else:
        logging.error("Unknown data structure: %s", output)
        return None
