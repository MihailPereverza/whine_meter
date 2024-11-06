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
                    raise BaseException("Unknown Error")
            else:
                raise BaseException("Unknown dict format")
        elif isinstance(output, list):
            return output
        else:
            raise BaseException("Unknown data structure")
