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
    results =[]

    for page in count(1):

        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' %page

        html = crawler.crawling(url,encoding='utf-8')

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table',attrs={'class':'table mt20'})
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
            results.append((name,address) + tuple(sidogu))

    # store
    table = pd.DataFrame(results, columns=['name','address','sido','gugun'])
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)


def crawling_nene():
    results = []
    store = ''
    for page in range(1,3):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d'%page

        try:
            request = Request(url)

            response =  urlopen(request)
            receive = response.read()
            html = receive.decode('utf-8')

            print(f'{datetime.now()}: success for request [{url}]')
        except Exception as e:
            print('%s : %s' % (e, datetime.now()), file=sys.stderror)
        # print(html)
        bs = BeautifulSoup(html,'html.parser')
        tag_shopInfo = bs.findAll('div',attrs={'class':'shopInfo'})
        firstShopName = tag_shopInfo[0].find('div',attrs={'class':'shopName'}).text
        if firstShopName != store:
            store = firstShopName
        else:
            break
        for info in tag_shopInfo:
            shopName = info.find('div',attrs={'class':'shopName'}).text
            shopAdd = info.find('div',attrs={'class':'shopAdd'}).text
            shopPizza = info.find('span',attrs={'class','pizzaShop'})
            if shopPizza != None:
                shopPizza = shopPizza.text

            results.append((shopName,shopAdd,shopPizza))

        table = pd.DataFrame(results, columns=['store','address','pizza'])
        table.to_csv('__results__/nene.csv', encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results = []
    for sido1 in range(1,2):
        for sido2 in count(1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1,sido2)
            html = crawler.crawling(url, encoding='utf-8')

            if html is None:
                break

            bs = BeautifulSoup(html,'html.parser')
            tag_ul = bs.find('ul',attrs={'class':'list'})
            tags_span = tag_ul.findAll('span',attrs={'class','store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)
                # print(strings)

                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidofu = address.split()[:2]
                # print(name,address,sidofu,sep=':')
                results.append((name,address)+tuple(sidofu))
        for t in results:
            print(t)

        table = pd.DataFrame(results, columns=['store', 'address', 'si','do'])
        table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawing_goobne():
    results = []

    url = 'http://goobne.co.kr/store/search_store.jsp'
    wd = webdriver.Chrome("D:\cafe24\chromedriver.exe")
    wd.get(url)
    time.sleep(1)

    for page in count(start=1):
        # 자바 스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time.sleep(1)

        # 실행결과 HTML(동적으로 렌더링된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html,'html.parser')
        tag_tbody = bs.find('tbody',attrs={'id':'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 마지막 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            # print(strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name,address)+tuple(sidogu))

        table = pd.DataFrame(results, columns=['store', 'address', 'si', 'do'])
        table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)
        for result in results:
            print(result)


if __name__ == '__main__':
    # 페리카나
    # crawling_pelicana()

    # nene 과제
    crawling_nene()

    # 교촌
    # crawling_kyochon()

    # goobne
    # crawing_goobne()