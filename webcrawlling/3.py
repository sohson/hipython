from playwright.sync_api import sync_playwright # 브라우저를 코드로 제어할 수 있게 해주는 라이브러리

with sync_playwright() as p:
  browser = p.chromium.launch(headless=False) # False → 실제 브라우저 창을 화면에 띄움 (True로 바꾸면 백그라운드에서 실행)

  page = browser.new_page()
  page.goto("https://www.example.com/")
  print(page.title())
  
  page_html = page.content()
  print(page_html[:200])
  
  page.wait_for_timeout(5000)
  browser.close()

print('크롤링 완료!')