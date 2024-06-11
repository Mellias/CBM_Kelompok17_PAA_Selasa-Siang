from PIL import Image, ImageDraw
import random
from numpy import sort

class map:
    def __init__(self):
        self.scale = 10
        self.width = 150 * self.scale
        self.height = 150 * self.scale
        self.road_len = 20 * self.scale
        self.road_width = 20
        self.padding = self.scale
        self.simpang = []
        self.jarak = 10

    def limitX(self, x):
        return max(0, min(x, self.width))

    def limitY(self, y):
        return max(0, min(y, self.height))

    def makeRoads(self, pos, direction):
        self.len += 1
        nearX = pos[0]
        for sim in self.simpang:
            if sim[0] > pos[0] - 20 and sim[0] < pos[0] + 20:
                nearX = sim[0]
        pos = (nearX, pos[1])
        pos = (pos[0] // 20 * 20, pos[1] // 20 * 20)
        if self.len > 150 and (pos[0] <= 0 or pos[0] >= self.width or pos[1] <= 0 or pos[1] >= self.height):
            return
        self.simpang.append(pos)
        step = random.choice([1, 1])
        nextvertice = (
            pos[0] + self.road_width if direction == "y" else pos[0] + self.road_len * step, 
            pos[1] + self.road_width if direction == "x" else pos[1] + self.road_len * step
        )
        self.simpang.append(nextvertice)
        valid = [
            pos[0] <= 0 and direction == "y", 
            pos[1] <= 0 and direction == "x", 
            pos[0] >= self.height and direction == "x",
            pos[1] >= self.height and direction == "x" 
        ]
        nextvertice = (self.limitX(nextvertice[0]), self.limitY(nextvertice[1]))
        xsort, ysort = sort([pos[0], nextvertice[0]]), sort([pos[1], nextvertice[1]])
        if not sum(valid):
            self.mapDraw.rectangle(((xsort[0], ysort[0]), (xsort[1], ysort[1])), "black")
            if direction == "y":
                self.mapDraw.line(((xsort[0] + 10, ysort[0] + 10), (xsort[0] + 10, ysort[1] - 10)), "white", 1)
            else:
                self.mapDraw.line(((xsort[0] + 20, ysort[0] + 10), (xsort[1] - 10, ysort[0] + 10)), "white", 1)
        nextX = self.width if nextvertice[0] <= 0 else (nextvertice[0] - (20 if direction == "y" else 0) if nextvertice[0] < self.width else 0)
        nextY = self.height if nextvertice[1] <= 0 else (nextvertice[1] - (20 if direction == 'x' else 0) if nextvertice[1] < self.height else 0)
        self.makeRoads((nextX, nextY), random.choice(["x", "y"]))

    def createMap(self):
        self.simpang = []
        self.len = 0
        self.map = Image.new("RGBA", (self.width, self.height), "lightgreen")
        self.mapDraw = ImageDraw.Draw(self.map)
        start_pos = (random.randrange(0, self.width, self.road_len), random.choice([0, self.height]))
        self.makeRoads(start_pos, "x")
        self.map.save("map1.png")
        self.mapping()
        self.map.save("map2.png")
        return self.map
    
    def mapping(self):
        print(self.simpang)
        for titik in self.simpang:
            if titik[1] >= self.height:
                continue
            
            nearX, nearY = 0, 0
            
            for tetangga in self.simpang:
                if titik == tetangga or titik[0] <= 0 or titik[1] <= 0:
                    continue
                if tetangga[0] < titik[0] and tetangga[1] == titik[1]:
                    nearX = max(nearX, tetangga[0])
                if tetangga[1] < titik[1]:
                    nearY = max(nearY, tetangga[1])
            if titik[0] - nearX >= 30 and titik[1] - nearY >= 30:
                self.simpang.extend([
                    (nearX, nearY),
                    (nearX - self.jarak, titik[1]),
                    (titik[0], nearY)
                ])
                self.mapDraw.rectangle(((nearX + 10, nearY + 10), (titik[0] - 10, titik[1] - 10)), "green")
                #self.generateBuilding(((nearX + 10, nearY + 10), (titik[0] - 10, titik[1] - 10)))
    
    def show(self):
        self.map.show()

myMap = map()
myMap.createMap()
myMap.show()
