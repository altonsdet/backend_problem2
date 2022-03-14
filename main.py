from urllib.request import Request
from urllib.request import urlopen
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4
import json
import re

WEB = 'http://bgp.he.net'


# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = bs4.BeautifulSoup(html, features="html.parser")
    return soup


def find_pages(page):
    pages = []
    for link in page.find_all(href=re.compile('/country')):
        pages.append(link.get('href'))
    return pages


def scrape_pages(links):
    mappings = {}
    for link in links:
        country_page = url_to_soup(WEB + link)
        current_country = link.split('/')[2]
        for row in country_page.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) > 0:
                current_asn = re.findall(r'\d+', columns[0].string)[0]
                name = columns[1].string
                routes_v4 = columns[3].string
                routes_v6 = columns[5].string
                mappings[current_asn] = {'Country': current_country,
                                         'Name': name,
                                         'Routes v4': routes_v4,
                                         'Routes v6': routes_v6}
    return mappings


def create_json_file(mapping):
    json_ = json.dumps(mapping, indent=4, sort_keys=False)
    json_file = open('data.json', 'w')
    json_file.write(json_)
    json_file.close()


print("Starting")
main_page = url_to_soup(WEB + '/report/world')
country_links = find_pages(main_page)
asn_mappings = scrape_pages(country_links)
create_json_file(asn_mappings)
print("Done")