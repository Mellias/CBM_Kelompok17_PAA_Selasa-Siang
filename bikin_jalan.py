from PIL import Image, ImageDraw
import random

# Inisialisasi ukuran canvas dan skala
skala = 10
lebar = 150 * skala
tinggi = 150 * skala
roadSize = 10
padding = 10

# Inisialisasi gambar
gedung = Image.open("image/gedung_kecil.png")
sekolah = Image.open("image/sekolah.png")
rumah = Image.open("image/rumah.png")
bangunan = [gedung, sekolah, rumah]

# Membuat gambar dan konteks menggambar
image = Image.new("RGBA", (lebar, tinggi), "green")
draw = ImageDraw.Draw(image)

# Fungsi untuk menggambar jalan horizontal
def draw_horizontal_road(y, road_map):
    draw.line([0, y, lebar, y], fill="black", width=roadSize)
    for x in range(lebar):
        for w in range(roadSize):
            if y + w < tinggi:
                road_map[x][y + w] = True

# Fungsi untuk menggambar jalan vertikal
def draw_vertical_road(x, road_map):
    draw.line([x, 0, x, tinggi], fill="black", width=roadSize)
    for y in range(tinggi):
        for w in range(roadSize):
            if x + w < lebar:
                road_map[x + w][y] = True

# Fungsi untuk menggambar belokan satu arah
def draw_turn(x, y, direction, road_map):
    if direction == "right":
        draw.line([x, y, x + roadSize, y], fill="black", width=roadSize)
        draw.line([x + roadSize, y, x + roadSize, y + roadSize], fill="black", width=roadSize)
    elif direction == "left":
        draw.line([x, y, x - roadSize, y], fill="black", width=roadSize)
        draw.line([x - roadSize, y, x - roadSize, y + roadSize], fill="black", width=roadSize)
    elif direction == "up":
        draw.line([x, y, x, y - roadSize], fill="black", width=roadSize)
        draw.line([x, y - roadSize, x + roadSize, y - roadSize], fill="black", width=roadSize)
    elif direction == "down":
        draw.line([x, y, x, y + roadSize], fill="black", width=roadSize)
        draw.line([x, y + roadSize, x + roadSize, y + roadSize], fill="black", width=roadSize)
    
    for i in range(roadSize):
        for j in range(roadSize):
            if direction in ["right", "left"]:
                if x + i < lebar and y + j < tinggi:
                    road_map[x + i][y + j] = True
            elif direction in ["up", "down"]:
                if x + j < lebar and y + i < tinggi:
                    road_map[x + j][y + i] = True

# Fungsi untuk membuat jalan secara iteratif
def make_roads(road_map):
    horizontal_positions = []
    vertical_positions = []
    
    # Menggambar jalan horizontal dengan jarak acak
    y = 0
    while y < tinggi:
        y += random.randint(30, 50) * skala
        if y < tinggi:
            draw_horizontal_road(y, road_map)
            horizontal_positions.append(y)
    
    # Menggambar jalan vertikal dengan jarak acak
    x = 0
    while x < lebar:
        x += random.randint(40, 50) * skala
        if x < lebar:
            draw_vertical_road(x, road_map)
            vertical_positions.append(x)
    
    # Membuat pertigaan dan belokan satu arah pada titik pertemuan
    for y in horizontal_positions:
        for x in vertical_positions:
            if random.choice([True, False]):
                draw_turn(x, y, random.choice(["right", "left", "up", "down"]), road_map)

# Inisialisasi peta jalan
road_map = [[False] * tinggi for _ in range(lebar)]

# Memanggil fungsi untuk membuat jalan
make_roads(road_map)

# Fungsi untuk menggambar padding di sekitar jalan
def draw_padding(road_map):
    for x in range(lebar):
        for y in range(tinggi):
            if road_map[x][y]:
                x1, y1 = max(0, x - padding), max(0, y - padding)
                x2, y2 = min(lebar, x + roadSize + padding), min(tinggi, y + roadSize + padding)
                for i in range(x1, x2):
                    for j in range(y1, y2):
                        if not road_map[i][j]:  # Only draw padding if it's not already part of a road
                            draw.point((i, j), fill="lightgreen")

# Membuat peta yang mempertimbangkan padding
draw_padding(road_map)

# Fungsi untuk menempatkan bangunan pada posisi acak tanpa bertabrakan dengan jalan atau padding
def place_buildings(num_buildings, road_map):
    for _ in range(num_buildings):
        # pilih bangunan secara acak
        building = random.choice(bangunan)
        
        placed = False
        while not placed:
            # Tentukan posisi acak untuk bangunan
            x = random.randint(0, lebar - building.width)
            y = random.randint(0, tinggi - building.height)
            
            # Periksa apakah posisi ini aman (tidak bertabrakan dengan jalan atau padding)
            collision = False
            for i in range(building.width):
                for j in range(building.height):
                    if road_map[x + i][y + j]:  # Check collision with road and padding
                        collision = True
                        break
                if collision:
                    break
            
            if not collision:
                # Tempelkan bangunan pada peta
                image.paste(building, (x, y), building)
                # Tandai area yang ditempati bangunan pada peta
                for i in range(building.width):
                    for j in range(building.height):
                        road_map[x + i][y + j] = True
                placed = True

# Tempatkan beberapa bangunan pada peta
place_buildings(10, road_map)

# Menampilkan dan menyimpan gambar
image.show()
image.save("iterative_roads_with_turns_and_padding_no_collision.png")
