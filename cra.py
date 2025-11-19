from bs4 import BeautifulSoup

# Mở file HTML đã lưu
with open("vuahanghieu.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Tìm tất cả div class="products-grid"
grids = soup.find_all("div", class_="item simple-config")

image_urls = []

for grid in grids:
    imgs = grid.find_all("img")
    for img in imgs:
        # lấy src hoặc data-src nếu lazy-load
        src = img.get("src") or img.get("data-src")
        if src:
            image_urls.append(src)

print(f"Tìm được {len(image_urls)} ảnh")
for url in image_urls:
    print(url)
