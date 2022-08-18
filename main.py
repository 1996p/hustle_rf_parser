
import requests
import json
from time import time

URL = 'https://xn--80awro.xn--p1ai/krossovki?start={position}&tmpl=component'
HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

SHOP_URL = 'https://хасл.рф/'

all_trainers_data = {'trainers': []}


def get_content(url: str) -> dict:
    response = requests.get(url=url, headers=HEADERS).json()['rows']
    print(f'Going to url {url}...')
    return response


def parse_json(data: dict) -> None:
    for iterator in range(0, 40):

        current_trainers_json = data[iterator]

        attrs = current_trainers_json['attributes'][0]['list']
        able_sizes = []

        for attr in attrs:
            able_sizes.append(attr['name'])

        trainers_info = {
            'name': current_trainers_json['name'],
            'actual_price': current_trainers_json['product_price'],
            'old_price': current_trainers_json['product_old_price'],
            'discount': current_trainers_json['product_old_price'] - current_trainers_json['product_price'],
            'image_url': current_trainers_json['image'],
            'link': SHOP_URL + current_trainers_json['product_link'],
            'able_size': able_sizes
        }

        all_trainers_data['trainers'].append(trainers_info)


def write_file(raw_trainers_data: dict) -> None:
    with open('хасл_рф_кроссовки.json', 'w') as file:
        json.dump(raw_trainers_data, file, indent=4, ensure_ascii=False)


def main() -> None:
    for i in range(0, 4080, 40):
        data = get_content(URL.format(position=i))
        parse_json(data)

    write_file(all_trainers_data)


if __name__ == '__main__':
    t0 = time()
    main()
    print(f'{time() - t0} seconds has passed')
