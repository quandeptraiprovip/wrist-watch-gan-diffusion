from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os, requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def fetch_page(url):
    driver = get_driver()
    try:
        driver.get(url)

        # Scroll từ từ để load ảnh
        last = 0
        while True:
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(0.4)
            new = driver.execute_script("return window.pageYOffset;")
            if new == last:
                break
            last = new

        html = driver.page_source
        return html
    except Exception as e:
        print("LỖI fetch_page:", e)
        return ""
    finally:
        driver.quit()

def extract_images(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="item simple-config")
    imgs = []

    for item in items:
        img = item.find("img")
        if not img:
            continue
        src = img.get("src") or img.get("data-src")
        if src and src.startswith("http"):
            imgs.append(src)

    return imgs

def download_and_resize(url, save_path):
    try:
        r = requests.get(url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        img = img.resize((128, 128))
        img.save(save_path)
        return True
    except Exception as e:
        print("Lỗi tải ảnh:", e)
        return False


# ---------------------------
# MAIN LOOP
# ---------------------------

page = 346
os.makedirs("images", exist_ok=True)

while True:
    url = "https://vuahanghieu.com/dong-ho" if page == 1 else f"https://vuahanghieu.com/dong-ho?page={page}"
    print("\n🔍 CRAWL:", url)

    html = fetch_page(url)
    if not html:
        print("⛔ HTML rỗng → STOP.")
        # break

    imgs = extract_images(html)
    if len(imgs) == 0:
        print("⛔ Hết sản phẩm → STOP.")
        # break

    print("📸 Tìm được:", len(imgs), "ảnh")

    for idx, link in enumerate(imgs):
        save_path = f"images/p{page}_{idx}.jpg"
        download_and_resize(link, save_path)

    page += 1
