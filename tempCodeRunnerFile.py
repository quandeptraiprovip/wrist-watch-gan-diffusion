"https://vuahanghieu.com/dong-ho" if page == 1 else f"https://vuahanghieu.com/dong-ho?page={page}"
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
