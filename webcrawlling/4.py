from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
  browser = p.chromium.launch(headless=False)
  page= browser.new_page()
  page.goto('http://quotes.toscrape.com/')

  html=page.content()
  soup=BeautifulSoup(html,'lxml')
  #print(soup.find('span',class_='text').get_text())
  print(soup.select_one('span.text').text)
  print(soup.select_one('small.author').text)

  # 페이지 내 모든 명언 블록 선택
  # div.quote → class="quote"인 div 전체
  # 여러 개이므로 리스트 형태로 반환됨
  quotes=soup.select('div.quote') # 리스트로 반환
  quotes_list = []

  for quote in quotes:
    # 각 div.quote 안에서
    # - span.text → 명언 내용
    # - small.author → 작성자
    # 를 추출해서 딕셔너리 형태로 저장
    quotes_list.append({'quote':quote.select_one('span.text').text, 'author':quote.select_one('small.author').text})

  import pandas as pd
  df=pd.DataFrame(quotes_list)
  print(df.head())

