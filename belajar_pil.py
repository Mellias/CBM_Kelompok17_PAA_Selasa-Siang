from PIL import Image

# Open an image
#img1 = Image.open("image/kuda.png") 
#img2 = Image.open("image/kudaa.png")
# Jika dua gambar tidak dapat digabungkan, maka salah satu gambarnya harus diubah ukurannya supaya bisa saling menyamakan. 
#img2_resized = img2.resize(img1.size)
# Blend two images
#img = Image.blend(img1, img2_resized, alpha=1)

# Rotate an image
#img = img.rotate(angle=60, expand=True, fillcolor="green") 

# Resize an image
#img = img.resize((int(img.width*2), int(img.height*2)), resample=Image.LANCZOS)
#print(img.width, img.height)

# Create an image
#img = Image.new("RGB", (400, 500), "yellow")

# Memotong gambar
img = Image.open("image/kuda.png") # Membuka gambar

imgCropped = img.crop(box = (100, 100, 300, 300)) # Memotong gambar

imgCropped.show() # Menampilkan gambar