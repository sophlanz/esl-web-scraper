from bs4 import BeautifulSoup
import requests, lxml, os, json
from parsel import Selector

def google_scholar_pagination():
  # https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    # https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    params = {
        'q': 'online language learning',
        'hl': 'en',       # language of the search
        'start': 0        # page number ⚠
    }

    # JSON data will be collected here
    data = []

    while True:
        html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
        selector = Selector(text=html)

        print(f'extrecting {params["start"] + 10} page...')

        # Container where all needed data is located
        for result in selector.css('.gs_r.gs_or.gs_scl'):
            title = result.css('.gs_rt').xpath('normalize-space()').get()
            title_link = result.css('.gs_rt a::attr(href)').get()
            publication_info = result.css('.gs_a').xpath('normalize-space()').get()
            snippet = result.css('.gs_rs').xpath('normalize-space()').get()
            cited_by_link = result.css('.gs_or_btn.gs_nph+ a::attr(href)').get()

            data.append({
                'page_num': params['start'] + 10, # 0 -> 1 page. 70 in the output = 7th page
                'title': title,
                'title_link': title_link,
                'publication_info': publication_info,
                'snippet': snippet,
                'cited_by_link': f'https://scholar.google.com{cited_by_link}',
            })

        # check if the "next" button is present
        if selector.css('.gs_ico_nav_next').get():
            params['start'] += 10
        else:
            break

    print(json.dumps(data, indent = 2, ensure_ascii = False))

google_scholar_pagination()