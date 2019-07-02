import os
import ssl
import sys
import time
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen


import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    result = []
    for page in count(1):
        url = "https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d" % page
        html = crawler.crawling(url)
        # try:
        #     request = Request(url)
        #     context = ssl._create_unverified_context()
        #     response = urlopen(request, context=context)
        #
        #     receive = response.read()
        #     html = receive.decode('UTF-8', errors='replace')
        #     print(f'{datetime.now()}:success for Request [{url}]')
        # except Exception as e:
        #     print(f'{e} : {datetime.now()} ', file=sys.stderr)

        bs = BeautifulSoup(html, 'html.parser')
        # print(bs.prettify())
        tag_table = bs.find('table', attrs={'class': 'table'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split(' ')[:2]
            result.append((name, address) + tuple(sidogu))
            # print('{0}:{1}'.format(name, address))

    # for t in result:
    #     print(t)
    #     # print('=================================================================')

    # store
    table = pd.DataFrame(result, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/pelicana.csv', encoding='UTF-8', mode='w', index=True)
    print(table)


def crawling_nene():
    result = []
    countboard = 0
    for page in range(1, 5):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?page=%d&ex_select=1&ex_select2=&IndexSword=&GUBUN=A' % page
        try:
            request = Request(url)
            context = ssl._create_unverified_context()
            response = urlopen(request, context=context)
            receive = response.read()
            html = receive.decode('UTF-8', errors='replace')
            print(f'{datetime.now()}:success for Request [{url}]')
        except Exception as e:
            print(f'{e} : {datetime.now()} ', file=sys.stderr)

        bs = BeautifulSoup(html, 'html.parser')
        tag_shoptables = bs.findAll('table', attrs={'class': 'shopTable'})

        # for tag_shoptable in tag_shoptables:
        #     strings = list(tag_shoptable.strings)
        #     print(strings)

        for tag_shoptable in tag_shoptables:
            countboard += 1
            shopname = tag_shoptable.find('div', attrs={'class': 'shopName'}).text
            shopadd = tag_shoptable.find('div', attrs={'class': 'shopAdd'}).text
            result.append((shopname, shopadd))

        # 끝 검출
        if countboard != 24:
            break
        countboard = 0
 ###
    table = pd.DataFrame(result, columns=['name', 'address'])
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULT_DIR = f'{BASE_DIR}__results__'
    print(BASE_DIR)
    # table.to_csv(f'{RESULT_DIR}/__results__/nene.csv', encoding='UTF-8', mode='w', index=True)
    table.to_csv('/root/crawling-results/nene.csv', encoding='UTF-8', mode='w', index=True)


def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawler.crawling(url)

            # 끝 검출
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_spans = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_spans:
                strings = list(tag_span.strings)
                # print(strings)

                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidogu = address.split()[:2]
                results.append((name, address) + tuple(sidogu))

    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # table.to_csv('__results__/nene.csv', encoding='UTF-8', mode='w', index=True)
    print(table)


def crawling_goobne():
    results = []
    url = 'http://goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:\cafe24\chromedriver_win32\chromedriver.exe')
    wd.get(url)

    time.sleep(3)
    for page in count(1):
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}:success for request [{script}]')
        time.sleep(2)

        # 실행결과 HTML(동적으로 렌더링 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect las page
        if tags_tr[0].get('class') is None:
            break
        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    wd.quit()
    # for result in results:
    #     print(result)
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/goobne.csv', encoding='UTF-8', mode='w', index=True)


if __name__ == '__main__':
    # crawling_pelicana()
    crawling_nene()
    # crawling_kyochon()
    # crawling_goobne()

    # nene 과제
    # crawling_nene()