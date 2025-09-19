from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse

load_dotenv()

token = os.getenv("API_TOKEN")

def get_link():
    link = input("Введите ссылку: ")
    return(link)

def is_shorten_link(url):
    parsed = urlparse(url)
    if parsed.netloc == "vk.cc":
        return True
    return False  

def count_clicks(token, link):
    url = "https://api.vk.ru/method/utils.getLinkStats"

    parsed = urlparse(link)
    key_param = parsed.path[1:]
    headers = {"Authorization": token}
    payload = {"v": "5.199", "key": key_param, "interval": "forever"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response_dict = response.json()

    stats = response_dict.get('response', {}).get('stats', [])
    if not stats or 'views' not in stats[0]:
        raise requests.HTTPError("Нет данных о просмотрах")

    clicks_count = stats[0]['views']
    return clicks_count

def shorten_link(token, link):
    url = "https://api.vk.ru/method/utils.getShortLink"
    headers = {"Authorization": token}
    payload = {"v": '5.199', "url": link, "private": "0"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    response_dict = response.json()
    if "response" not in response_dict:
        error_msg = response_dict["error"]["error_msg"]
        raise requests.HTTPError (error_msg)
    short_link = response_dict["response"]["short_url"]
    return short_link

def main():
    user_input = get_link()
    if is_shorten_link(user_input):
        try:
            parsed = count_clicks(token, user_input)
            print("Количество просмотров: ", parsed)
        except requests.exceptions.HTTPError as exc:
            print(exc)
    else:
        try:
            short_link = shorten_link(token, user_input)
            print("Сокращенная ссылка: ", short_link)
        except requests.exceptions.HTTPError as exc:
            print(exc)

if __name__ == '__main__':
    main()

 