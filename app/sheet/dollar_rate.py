import requests


def get_dollar_rate():
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    return data["Valute"]["USD"]["Value"]
