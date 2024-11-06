import time
import requests

# format
# if error:
#   returns a dict with d['error'] = "... currently loading"
# else:
#   returns a list


def calculate_whine(message: str):
    API_URL = "https://api-inference.huggingface.co/models/seara/rubert-tiny2-russian-sentiment"
    headers = {"Authorization": "Bearer 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",
               'x-use-cache': 'true'}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    counter = 0
    while True:
        output: dict = query({
            "inputs": message,
        })
        if isinstance(output, dict):
            if 'error' in output.keys():
                if 'currently loading' in output['error']:
                    # print("time to sleep:", output['estimated_time'])
                    time.sleep(output['estimated_time'])
                else:
                    raise BaseException("Unhandled Error:", output['error'])
            else:
                raise BaseException("Unknown dict format")
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
            raise BaseException("Unknown data structure:", type(output))

        counter += 1
        if counter == 10:
            raise BaseException("attempts timeout:", counter)
