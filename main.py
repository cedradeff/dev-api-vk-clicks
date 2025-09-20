from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse


def is_shorten_link(token, link):
    link_parsed = urlparse(link)
    key_param = link_parsed.path[1:]
    url = "https://api.vk.ru/method/utils.getLinkStats"
    headers = {"Authorization": token}
    payload = {"v": '5.199', "key": key_param}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response_data = response.json()
    return "error" not in response_data


def count_clicks(token, link):
    url = "https://api.vk.ru/method/utils.getLinkStats"
    link_parsed = urlparse(link)
    key_param = link_parsed.path[1:]
    headers = {"Authorization": token}
    payload = {"v": "5.199", "key": key_param, "interval": "forever"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response_data = response.json()
    if "error" in response_data:
        error_msg = response_data["error"]["error_msg"]
        raise requests.HTTPError(error_msg)
    stats = response_data.get('response', {}).get('stats', [])
    if not stats:
        return 0
    clicks_count = stats[0]['views']
    return clicks_count


def shorten_link(token, link):
    url = "https://api.vk.ru/method/utils.getShortLink"
    headers = {"Authorization": token}
    payload = {"v": '5.199', "url": link, "private": "0"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response_data = response.json()
    if "error" in response_data:
        error_msg = response_data["error"]["error_msg"]
        raise requests.HTTPError(error_msg)
    short_link = response_data["response"]["short_url"]
    return short_link


def main():
    token = os.environ["VK_ACCESS_TOKEN"]
    user_input = input("Введите ссылку: ")
    if is_shorten_link(token, user_input):
        try:
            click_counts = count_clicks(token, user_input)
            print("Количество просмотров: ", click_counts)
        except requests.exceptions.HTTPError as exc:
            print(exc)
    else:
        try:
            short_link = shorten_link(token, user_input)
            print("Сокращенная ссылка: ", short_link)
        except requests.exceptions.HTTPError as exc:
            print(exc)


if __name__ == '__main__':
    load_dotenv()
    main()
