from PIL import Image, ImageDraw
import random

# Ukuran gambar dan jumlah langkah
skala = 10
lebar = 150 * skala
tinggi = 150 * skala
jumlah_langkah = 10
w = 2 * skala
h = 2 * skala

image = Image.new("RGBA", (lebar, tinggi), "green")
images = Image.new("RGBA", (lebar, tinggi), "green")

draw = ImageDraw.Draw(image)
draws = ImageDraw.Draw(images)

titikSudut = [(0,0), (lebar - w, tinggi - h), (0, tinggi - h), (lebar - w, 0)]

#startPoint = { "atas" : "bawah", "bawah" : "atas", "kanan" : "kiri", "kiri" : "kanan"}
move = { 
    "atas" : (0, 2 * skala), 
    "bawah" :(0, -2 * skala), 
    "kanan" : (2 * skala, 0),
    "kiri" : (-2 * skala, 0)
}

def makeRoads(x, y, arah, count, length):
    #global lebar, tinggi
    #w, h = (2*skala, 2*skala) 
    draw.rectangle(xy = (x, y, x + w, y + h), fill = "black")
    if not count :
        count = jumlah_langkah
        if not random.randint(0, 3):
            titikSudut.append((x, y))
            arah = random.choice(direction[2:] if arah == "atas" or arah == "bawah" else direction[:2])
    if (length > 450 and (x < 0 or y < 0 or x >= lebar or y >= tinggi) ) or length >= 700:
        return
    if (x >= 0 and x < lebar-2) and (y >= 0 and y < tinggi-2):
        makeRoads(x+move[arah][0], y+move[arah][1], arah, count-1, length+1)
    else :
        titikSudut.append((x % lebar, y % tinggi))
        titikSudut.append(((lebar + x + move[arah][0]) % lebar, (tinggi + y + move[arah][1]) % tinggi))
        makeRoads((lebar + x + move[arah][0]) % lebar, (tinggi + y + move[arah][1]) % tinggi, arah, jumlah_langkah, length + 1)
    
direction = ["atas", "bawah", "kanan", "kiri"]
def render():
    directions = random.choice(direction)
    if directions == "atas":
        x = jumlah_langkah * random.randint(1, lebar // jumlah_langkah)
        y = 0
    elif directions == "bawah":
        x = jumlah_langkah * random.randint(1, lebar // jumlah_langkah)
        y = tinggi - 1
    elif direction == "kanan":
        x = 0
        y = jumlah_langkah * random.randint(1, tinggi // jumlah_langkah)
    else:
        x = lebar-1
        y = jumlah_langkah * random.randint(1, tinggi // jumlah_langkah)
    makeRoads(x, y, directions, jumlah_langkah, 1)
    
def drawMap(x, y, x1, y1, fill):
    padding  = 2 * skala
    x += padding
    y += padding
    if x >= x1 - skala or y >= y1 - skala:
        return
    #draw.rectangle(xy = (x, y, x1-skala , y1-skala), fill = "lightgreen")

def search():
    for index, ver in enumerate(titikSudut):
        nearX = lebar
        nearY = tinggi
        minX = 0
        minY = 0
        maxX = 0
        maxY = 0
        for i in range(0, len(titikSudut)):
            if i == index :
               continue
            if titikSudut[i][0] > ver[0] and titikSudut[i][0]  < nearX:
                nearX = titikSudut[i][0]
            if titikSudut[i][1] > ver[1] and titikSudut[i][1]  < nearY:
                nearY = titikSudut[i][1]
            if titikSudut[i][0] >= minX and titikSudut[i][0] < ver[0]:
               minX = titikSudut[i][0]
               maxY = titikSudut[i][1]
            if titikSudut[i][1] >= minY and titikSudut[i][1] < ver[1]:
               minY = titikSudut[i][1]
               maxX = titikSudut[i][0]
        if minX > 0 and minY > 0:
            #print("jumpa")
            if (minX,minY) not in titikSudut:
                titikSudut.append((minX,minY)) 
            if (maxX,maxY) not in titikSudut:
                titikSudut.append((maxX,maxY))
            print(ver, minX,minY)
            drawMap(minX + skala, minY+skala, ver[0], ver[1], True)
        if (nearX,nearY) not in titikSudut:
            titikSudut.append((nearX,nearY))
        if minX == 0 or minY == 0:
            drawMap(minX, minY, ver[0], ver[1], True)

render()

search()
print(titikSudut)
print(len(titikSudut))
for ver in titikSudut:
    draws.rectangle(xy = (ver[0], ver[1], ver[0] + (2 * skala), ver[1] + (2 * skala)), fill = "black")
    
# Menyimpan gambar sebagai file
image.show()
image.save("map.png")