API command here: "kaggle datasets download -d minhquntntht/wrist-watch-128"
```bash
kaggle datasets download -d minhquntntht/wrist-watch-128
```
The dataset contains over 15,524 listings of luxury watches images scarapped from vuahanghieu.com.

Model

StyleGAN2


#The comparision

|Tiêu chí|GAN|Diffusion|
|:---|:----|:----|
|Ý tưởng|Hai mạng đối kháng: Generator và Discriminator|Thêm nhiễu vào ảnh rồi học các khử nhiễu|
|Nguyên lý|Adversarial learning|Denoising + Markov chain/score matching|

Về mặt lý thuyết, thì Diffusion ổn định hơn. Gan mang tính đối kháng hơn.
    
#GAN
Cách hoạt động:
1. Lấy noise z (vector ngẫu nhiên)
2. Generator -> tạo ảnh giả
3. Discriminator -> đoán ảnh
4. Hai mạng cập nhật

Hàm loss:
z∼N(0,1)

Các vấn đề:
Mode collapse: Mode collapse là hiện tượng G chỉ sinh ra một số ít kiểu ảnh giống nhau, mặc dù dữ liệu gốc có nhiều dạng khác nhau.

#Diffusion
Cách hoạt động:
1. Foward process: Thêm nhiễu Gaussian dần dần vào ảnh
2. Reserve process: Học cách loại bỏ nhiễu
3. Sampling: Bắt đầu từ noise thuần và khử dần thành ảnh. Sinh ảnh nhiều bước.

Diffusion mạnh hơn về lý thuyết.
