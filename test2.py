from PIL import Image, ImageDraw
import random
from numpy import sort

skala = 10
tinggi = 150 * skala
lebar = 150 * skala
roadSize = 10
padding = 10

maps = Image.new("RGBA", (lebar, tinggi), "green")
mapDraw = ImageDraw.Draw(maps)
count = 0

titik = []

def makeRoads(pos, arah):
    global count
    count += 1
    nextX = (pos[0] + 200) if arah == "horizontal" else pos[0]
    nextY = (pos[1] + 200) if arah == "vertical" else pos[1]
    
    print(nextX, nextY)
    mapDraw.line((pos, (nextX, nextY)), "black", roadSize)
    if count <= 10 : makeRoads((nextX, nextY), random.choice(["horizontal", "vertical"]))

makeRoads((random.randint(0, 150) * skala, 0), "vertical")

def mapping():
    for ver in titik:
        xtetangga = 0
        ytetangga = 0
        for ver2 in titik:
            if ver2 != ver:
                if ver2[0] < ver[0] and ver[1] == ver2[1] and xtetangga == 0:
                    xtetangga = ver2[0]
                if ver2[1] < ver[1] and ver[0] == ver2[0] and ytetangga == 0:
                    ytetangga = ver2[1]
        sortedX = sort([xtetangga + padding, ver[0] - padding])
        sortedY = sort([ytetangga + padding, ver[1] - padding])
        mapDraw.rectangle(((sortedX[0], sortedY[0]), (sortedX[1] , sortedY[1])), "lightgreen")

mapping()

maps.show()
        