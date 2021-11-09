import json
from typing import Optional

import requests

import config


def get_response(url: str, params: Optional[dict] = None) -> requests.Response:
    r = requests.get(url, params=params)
    print(f"Загружен ресурс {r.url}")
    return r


if __name__ == '__main__':
    test_url = "https://pipl.ir/v1/getPerson"

    resp = get_response(test_url)
    print(json.dumps(resp.json(), indent=config.JSON_INDENT))
