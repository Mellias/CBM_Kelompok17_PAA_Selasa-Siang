from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

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
        self.buildings = {
            "big": Image.open("bangunan/big.png"),
            "medium_v": Image.open("bangunan/medium_v.png"),
            "small_v": Image.open("bangunan/small_v.png"),
            "house_v": Image.open("bangunan/house_v.png"),
            "medium_h": Image.open("bangunan/medium_h.png"),
            "small_h": Image.open("bangunan/small_h.png"),
            "house_h": Image.open("bangunan/house_h.jpg")
        }
        self.env = [
            Image.open("asset/flower.png"),
            Image.open("asset/tree.png"),
            Image.open("asset/stone.png")
        ]
        self.map = Image.new("RGBA", (self.width, self.height), "lightgreen")
        self.mapDraw = ImageDraw.Draw(self.map)

        # Set the counts for buildings
        self.building_counts = {
            "big": 1,
            "medium_v": 2,
            "medium_h": 2,
            "small_v": 7,
            "small_h": 8,
            "house_v": 7,
            "house_h": 8
        }

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

    def generateBuilding(self, pos):
        x = pos[0][0]
        # Prepare the buildings
        buildings_to_place = []

        for building_type, count in self.building_counts.items():
            buildings_to_place.extend([self.buildings[building_type]] * count)

        random.shuffle(buildings_to_place)  # Shuffle to place buildings randomly

        # titik paling atas area
        def getBangunanX(x):
            return [bangunan for bangunan in buildings_to_place if bangunan.size[0] + x < pos[1][0] - self.padding]

        def getBangunanY(x, y):
            return [bangunan for bangunan in self.env if bangunan.size[0] + x < pos[1][0] - self.padding and bangunan.size[1] + y < pos[1][1] - 50]

        while x < pos[1][0]:
            kandidat = getBangunanX(x)
            if not kandidat:
                break  # Exit the loop if there are no candidate buildings

            build = kandidat.pop(0)  # Take the first available building
            self.mapDraw.rectangle(((x, pos[0][1]), (x + build.size[0] + 20, pos[0][1] + build.size[1])), "green")
            self.map.paste(build, (x, pos[0][1]))
            x += build.size[0] + self.jarak
    
        x = pos[0][0]
        y = pos[0][1] + 50 + self.padding

        while y < pos[1][1] - 50:
            tertinggi = 50
            while x < pos[1][0]:
                kandidat = getBangunanY(x, y)
                if len(kandidat):
                    build = random.choice(kandidat)
                    self.mapDraw.rectangle(((x, y), (x + build.size[0] + 20, y + build.size[1])), "green")
                    self.map.paste(build, (x, random.randint(y, y + (tertinggi - build.size[1]))))
                    tertinggi = max(build.size[1], tertinggi)
                    x += build.size[0] + self.padding
                else:
                    break
            y += tertinggi + self.padding
        x = pos[0][0]

        # titik paling bawah area
        while x < pos[1][0]:
            kandidat = getBangunanX(x)
            if len(kandidat):
                build = kandidat.pop(0)  # Take the first available building
                self.mapDraw.rectangle(((x, pos[1][1] - build.size[1]), (x + build.size[0] + 20, pos[1][1] - build.size[1] + build.size[1])), "green")
                self.map.paste(build, (x, pos[1][1] - build.size[1]))
                x += build.size[0] + self.jarak
            else:
                break

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
                self.generateBuilding(((nearX + 10, nearY + 10), (titik[0] - 10, titik[1] - 10)))

class MapApp:
    def __init__(self, root):
        self.myMap = map()
        self.zoom_factor = 1.0
        self.INITIAL_WIDTH = 500
        self.INITIAL_HEIGHT = 400
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 400
        self.viewport_height = 400
        self.new_map = None

        self.setup_ui(root)
        self.update_map()

    def setup_ui(self, root):
        root.title("Map Generator")
        root.bind("<MouseWheel>", self.scroll)

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.map_label = ttk.Label(frame)
        self.map_label.grid(row=0, column=0, padx=10, pady=10)

        generate_button = ttk.Button(root, text="Generate Map", command=self.update_map)
        generate_button.grid(row=1, column=0, pady=10)

        zoom_in_button = ttk.Button(root, text="Zoom In", command=self.zoom_in)
        zoom_in_button.grid(row=2, column=0, pady=5)

        zoom_out_button = ttk.Button(root, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.grid(row=3, column=0, pady=5)

    def update_map(self):
        self.new_map = self.myMap.createMap()
        self.update()

    def update(self):
        cropped_map = self.new_map.crop((self.viewport_x * self.zoom_factor, self.viewport_y * self.zoom_factor, 
                                         self.viewport_x * self.zoom_factor + self.viewport_width * self.zoom_factor, 
                                         self.viewport_y * self.zoom_factor + self.viewport_height * self.zoom_factor))
        resized_map = cropped_map.resize((self.INITIAL_WIDTH, self.INITIAL_HEIGHT))
        img_tk = ImageTk.PhotoImage(resized_map)
        self.map_label.config(image=img_tk)
        self.map_label.image = img_tk

    def zoom_in(self):
        if self.zoom_factor < 5.0:
            self.zoom_factor += 0.1
            self.update()

    def zoom_out(self):
        if self.zoom_factor > 0.5:
            self.zoom_factor -= 0.1
            self.update()

    def scroll(self, event):
        self.viewport_y = max(0, self.viewport_y - 20) if event.delta > 0 else min(self.new_map.height, self.viewport_y + 20)
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()
