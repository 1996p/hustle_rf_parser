import asyncio
import aiohttp
import json
from time import time

URL = 'https://xn--80awro.xn--p1ai/krossovki?start={position}&tmpl=component'
HEADERS = {
    'Accept': '*/*',
    'User-Agent': ''
}

SHOP_URL = 'https://хасл.рф/'

all_trainers_data = {'trainers': []}


async def get_content(url: str, session: aiohttp.ClientSession) -> None:
    """Отвечает за отправку GET-запроса на страницу с данными"""
    async with session.get(url=url, headers=HEADERS) as response:
        json_data = await response.json(content_type='text/html')
        parse_json(json_data['rows'])


def parse_json(data: dict) -> None:
    """Отвечает за парсинг данных формата json, складывает все в общий словарь с данными"""
    for iterator in range(0, 40):

        current_trainers_json = data[iterator]
        able_sizes = []
        try:
            attrs = current_trainers_json['attributes'][0]['list']
            for attr in attrs:
                able_sizes.append(attr['name'])

        except Exception:
            pass

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
    """Преобразует данные в объект json, а так же записывает их в .json файл"""
    with open('хасл_рф_кроссовки.json', 'w') as file:
        json.dump(raw_trainers_data, file, indent=4, ensure_ascii=False)


async def main() -> None:
    """Формирует таски"""
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_content(URL.format(position=i), session)) for i in range(0, 4000, 40)]
        await asyncio.gather(*tasks)

    write_file(all_trainers_data)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(f'{time() - t0} seconds has passed')
