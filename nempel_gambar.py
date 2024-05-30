# Ini adalah kodingan untuk latihan menempelkan gambar dan membuat GUI

from PIL import Image, ImageDraw, ImageTk
import random
import tkinter as tk
from tkinter import ttk

# Inisialisasi ukuran gambar
skala = 10
lebar = 150 * skala
tinggi = 150 * skala

# Inisialisasi gambar lain
gedung = Image.open("image/gedung_kecil.png")
sekolah = Image.open("image/sekolah.png")
rumah = Image.open("image/rumah.png")
bangunan = [gedung, sekolah, rumah]

# Membuat gambar 
gambar = Image.new ("RGBA", (lebar, tinggi), "green")
draw = ImageDraw.Draw(gambar)

# Fungsi untuk menempatkan bangunan pada posisi acak
def place_buildings(num_buildings):
    for _ in range(num_buildings):
        # pilih bangunan secara acak
        building = random.choice(bangunan)

        # Tentukan posisi acak untuk bangunan
        x = random.randint(0, lebar - building.width)
        y = random.randint(0, tinggi - building.height)

        # Tempelkan bangunan pada peta
        gambar.paste(building, (x, y), building)

# Tempatkan beberapa bangunan pada peta
place_buildings(10)

# Mengubah gambar PIL ke format yang dapat ditampilkan di tkinter
gambar_tk = ImageTk.PhotoImage(gambar)

# Membuat GUI dengan tkinter
window = tk.Tk()
window.title("Peta dengan Bangunan")

# Menambahkan kanvas untuk menampilkan gambar
canvas = tk.Canvas(window, width=lebar, height=tinggi)
canvas.pack()

# Menampilkan gambar pada kanvas
canvas.create_image(0, 0, anchor=tk.NW, image=gambar_tk)

# Memulai loop utama tkinter
window.mainloop()
