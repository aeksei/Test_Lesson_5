import json
import datetime

import xmltodict

import config
import client
from decorators import lru_cache


URL = "https://www.cbr.ru/scripts/XML_daily.asp"
USD_ID = "R01235"


@lru_cache(maxsize=10)
def get_exchange(day: int, month: int, year: int) -> dict:
    date = datetime.date(year=year, month=month, day=day)

    params = {
        "date_req": date.strftime(config.QUERY_DATE)
    }

    resp = client.get_response(URL, params)
    return xml_to_dict(resp.text)


def xml_to_dict(text: str) -> dict:
    return xmltodict.parse(text)


def get_usd_value(exchange_dict: dict) -> float:
    valute_list = exchange_dict["ValCurs"]["Valute"]
    usd_dict = next(filter(lambda item: item["@ID"] == USD_ID, valute_list), None)
    if usd_dict is None:
        raise ValueError("Нет курса для доллара")

    usd_str_value = usd_dict["Value"]
    usd_str_value = usd_str_value.replace(",", ".")

    return float(usd_str_value)


if __name__ == "__main__":
    exchange = get_exchange(20, 1, 2020)
    print(json.dumps(exchange, ensure_ascii=False, indent=config.JSON_INDENT))

    print(get_usd_value(exchange))
