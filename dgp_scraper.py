import os
import requests
from bs4 import BeautifulSoup
from flag_scraper import scrap_url

response = requests.get(
    url="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)",
).text
soup = BeautifulSoup(response, features='html.parser')


flags = soup.find_all(class_="flagicon")

for flag in flags:
    flag.decompose()


references = soup.find_all(class_="reference")

for ref in references:
    ref.decompose()


table = soup.find(class_='wikitable')
tbody = table.find('tbody')
rows = table.find_all('tr')


data = open('data.json', 'w')
data.write('{\n')
data.write('    "list_of_countries_by_gdp": [')


for row in rows[2:]:
    shift = 0
    cells = row.find_all('td')

    country = cells[0].text
    country = country.replace('\u00A0', '')
    print(f"...scrap data of {country}...")
    region = cells[1].text

    if 'N/A' in cells[2].text:
        imf_estimate = 'N/A'
        imf_year = 'N/A'
        shift += 1
    else:
        imf_estimate = cells[2].text
        imf_estimate = imf_estimate.replace(',', '')
        imf_estimate = imf_estimate.replace('\n', '')
        imf_year = cells[3].text
        imf_year = imf_year.replace(',', '')
        imf_year = imf_year.replace('\n', '')

    if 'N/A' in cells[4 - shift].text:
        un_estimate = 'N/A'
        un_year = 'N/A'
        shift += 1
    else:
        un_estimate = cells[4 - shift].text
        un_estimate = un_estimate.replace(',', '')
        un_estimate = un_estimate.replace('\n', '')
        un_year = cells[5 - shift].text
        un_year = un_year.replace(',', '')
        un_year = un_year.replace('\n', '')

    if 'N/A' in cells[6 - shift].text:
        wb_estimate = 'N/A'
        wb_year = 'N/A'
    else:
        wb_estimate = cells[6 - shift].text
        wb_estimate = wb_estimate.replace(',', '')
        wb_estimate = wb_estimate.replace('\n', '')
        wb_year = cells[7 - shift].text
        wb_year = wb_year.replace(',', '')
        wb_year = wb_year.replace('\n', '')

    flag_url = scrap_url(country)

    data.write(f'''
    {{
        "country": "{country}",
        "region": "{region}",
        "dgp": {{
            "imf":{{"estimate":"{imf_estimate}", "year": "{imf_year}"}},
            "un":{{"estimate": "{un_estimate}", "year": "{un_year}"}},
            "wb":{{"estimate": "{wb_estimate}", "year": "{wb_year}"}}
        }},
        "flag": "{flag_url}"
    }},''')


# delete trailing coma after last item in array
data.seek(data.tell() - 1, os.SEEK_SET)


data.write(']')
data.write('\n}')
data.close()
