from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
os.system("pkill -f chromedriver")


options = Options()
options.headless = True  # chạy ẩn nền
driver = webdriver.Chrome(options=options)



driver.get("https://vuahanghieu.com/dong-ho?page=3")
time.sleep(5)  # đợi JS load xong

html_content = driver.page_source

# Lưu ra file để inspect
with open("vuahanghieu.html", "w", encoding="utf-8") as f:
    f.write(html_content)

driver.quit()
print("HTML đã lưu xong: dongho.html")
