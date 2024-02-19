import datetime
import json
import os
from hashlib import md5

import pandas as pd
import requests

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml, application/json;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
URL1 = "https://dataportal-api.nordpoolgroup.com/api/AggregatePrices?year=2024&market=DayAhead&deliveryArea=AT&currency=EUR"
URL2 = "https://www.fxempire.com/api/v1/en/macro-indicators/india/gasoline-prices/history?latest=120&frequency=Monthly"
file1 = 'first.xlsx'
file2 = 'second.xlsx'


def get_data(url):
    url_hash = md5(url.encode()).hexdigest()
    file_name = url_hash + ".txt"
    if os.path.exists(file_name):
        with open(file_name, "r", encoding='UTF-8') as file:
            return json.loads(file.read())
    html = requests.get(url, headers=HEADERS).json()
    with open(file_name, "w", encoding='UTF-8') as file:
        file.write(json.dumps(html))
    return html


def main():
    data1 = get_data(URL1)
    data2 = get_data(URL2)
    df = pd.DataFrame({'Date': [], 'Price': []})
    series = []
    for item in data1.get('multiAreaDailyAggregates', []):
        data = item.get('deliveryStart', '')
        value = item.get('averagePerArea').get("AT")
        row = pd.DataFrame.from_dict({'Date': [data], 'Price': [value]})
        series.append(row)
    df = pd.concat(series, ignore_index=True)
    df.to_excel(file1, index=False)
    df = pd.DataFrame({'Date': [], 'Price': []})
    series = []
    for item in data2:
        data = datetime.datetime.fromtimestamp(item["timestamp"]).strftime('%Y-%m')
        value = item["close"]
        row = pd.DataFrame.from_dict({'Date': [data], 'Price': [value]})
        series.append(row)
    df = pd.concat(series, ignore_index=True)
    df.to_excel(file2, index=False)


if __name__ == '__main__':
    main()
