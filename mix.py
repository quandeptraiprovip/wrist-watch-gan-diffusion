from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import os
from PIL import Image
from io import BytesIO






# ======================
# SETUP SELENIUM
# ======================
options = Options()
options.headless = False   # để xem scroll
driver = webdriver.Chrome(options=options)


# ======================
# SCROLL CHẬM TỪ TỪ
# ======================
def slow_scroll():
    scroll_pause = 0.3
    step = 300  
    last_height = driver.execute_script("return document.body.scrollHeight")

    y = 0
    while y < last_height:
        y += step
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(scroll_pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height


# ======================
# LOAD PAGE VÀ SCROLL
# ======================
def fetch_page(url):
    driver.get(url)
    time.sleep(2)
    slow_scroll()
    return driver.page_source


# ======================
# PARSE ẢNH TỪ HTML
# ======================
def extract_images(html):
    soup = BeautifulSoup(html, "html.parser")
    grids = soup.find_all("div", class_="item simple-config")

    urls = []
    for grid in grids:
        imgs = grid.find_all("img")
        for img in imgs:
            src = img.get("src") or img.get("data-src")
            if src and src.startswith("http"):
                urls.append(src)
    return urls


# ======================
# TẢI VÀ RESIZE ẢNH
# ======================
def download_and_resize(url, save_dir="images", size=(128, 128), index=0):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        img = img.resize(size)

        filename = f"{save_dir}/img_{index}.jpg"
        img.save(filename, "JPEG")

        return True
    except:
        return False


# ======================
# MAIN CRAWLER
# ======================
page = 1
all_images = []

# os.system("pkill -f chromedriver")

os.makedirs("images", exist_ok=True)

while True:
    url = "https://vuahanghieu.com/dong-ho" if page == 1 else f"https://vuahanghieu.com/dong-ho?page={page}"
    print(f"\n🔍 Đang crawl: {url}")

    html = fetch_page(url)
    imgs = extract_images(html)

    if len(imgs) == 0:
        print("⛔ Không còn sản phẩm → STOP.")
        break

    print(f"   → Tìm được {len(imgs)} ảnh")
    all_images.extend(imgs)

    page += 1


# ======================
# DOWNLOAD + RESIZE ẢNH
# ======================
print("\n📥 Đang tải & resize ảnh...")

success = 0
for i, url in enumerate(all_images):
    ok = download_and_resize(url, index=i)
    if ok:
        success += 1

print(f"\n🎉 DONE! Đã tải & resize: {success}/{len(all_images)} ảnh")

driver.quit()
