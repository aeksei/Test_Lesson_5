import json
from typing import Iterator

import client
import parser


URL = "https://pipl.ir/v1/getPerson"
FILENAME = "output.txt"


def main():
    person_list = [person for person in random_person()]
    date = {
        "day": 5,
        "month": 5,
        "year": 2021
    }

    for person in person_list:
        usd_salary_to_rub(person, **date)

    print(json.dumps(person_list, indent=4))


def get_person() -> dict:
    resp = client.get_response(URL)

    return resp.json()


def add_rub_salary(person: dict, day: int, month: int, year: int) -> None:
    usd_salary = person["person"]["work"]["salary"]
    usd_salary = usd_salary.replace("$", "")  # todo maybe re.replace
    usd_salary = usd_salary.replace(".", "")
    usd_salary = int(usd_salary)

    usd_to_rub = parser.get_usd_value(parser.get_exchange(day, month, year))

    person["person"]["work"]["salary_rub"] = usd_salary * usd_to_rub


def random_person(count: int = 10) -> Iterator:
    for _ in range(count):
        yield get_person()


def to_json_file(person_list: list[dict]) -> None:
    with open(FILENAME, "w") as f:
        json.dump(person_list, f)


if __name__ == '__main__':
    main()
