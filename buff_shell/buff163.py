from bs4 import BeautifulSoup
import requests
import re
import time

headers = {
 'User-Agent': '',
 'Cookie': '',}
session = requests.Session()
url = 'https://buff.163.com/api/market/goods?game=csgo&page_num='

def handle_page(data):
    data


def get_more_pages(start,end):
    for page_num in range(start,end):
        response = session.get(url, headers=headers)
        print(response)
        handle_page(response)
        time.sleep(2)


get_more_pages(1,769)