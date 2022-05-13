import requests
from bs4 import BeautifulSoup


def scrap_url(country: str):
    if country == "Georgia":
        response = requests.get(
            url=f"https://en.wikipedia.org/wiki/{country}_(country)",
        ).text
    elif country == "Palestine":
        response = requests.get(
            url=f"https://en.wikipedia.org/wiki/State_of_{country}",
        ).text
    elif country == "Congo":
        response = requests.get(
            url=f"https://en.wikipedia.org/wiki/Democratic_Republic_of_the_{country}",
        ).text
    else:
        response = requests.get(
            url=f"https://en.wikipedia.org/wiki/{country}",
        ).text

    soup = BeautifulSoup(response, features='html.parser')

    img = soup.find(class_='thumbborder')
    url = img['src']
    url = url.replace('125', '480')
    return url
