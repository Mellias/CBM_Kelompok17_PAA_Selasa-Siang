from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

class map:
    # Mendeklarasikan variabel
    def __init__(self) -> None:
        self.scale = 10
        self.len = 0
        self.width = 150 * self.scale
        self.height = 150 * self.scale
        self.padding = self.scale
        self.road_len = 20 * self.scale
        self.road_width = 20
        self.simpang = []
        self.jarak = 10
        self.buildings = [
            Image.open("bangunan/big.png"),
            Image.open("bangunan/medium.png"), 
            Image.open("bangunan/small.png"), 
            Image.open("bangunan/house.png")
        ]
        self.env = [
            Image.open("asset/flower.png"),
            Image.open("asset/tree.png"), 
            Image.open("asset/stone.png")
            ]
        
        self.map = Image.new("RGBA", (self.width, self.height), "green" )
        self.mapDraw = ImageDraw.Draw(self.map)
        
    # Membatasi titik x dan y supaya tidak keluar dari map
    def limitX(self, x): 
        return 0 if x <= 0 else (x if x < self.width else self.width )
    def limitY(self, y) : 
        return 0 if y <= 0 else (y if y < self.height else self.height )
   
    # Membuat jalan dengan algoritma rekursif 
    def makeRoads(self, pos, direction):
        self.len += 1
        if self.len > 150 and (pos[0]<=0 or pos[0]>=self.width or pos[1] <= 0 or pos[1] >=self.height ): 
            return
        self.simpang.append(pos)
        step = random.choice([1,1])
       
        nextvertice = ( pos[0] + self.road_width if direction == "y" else pos[0] + self.road_len  * step, pos[1] + self.road_width if direction == "x" else pos[1] + self.road_len *step)
        if nextvertice not in self.simpang : self.simpang.append(nextvertice)
        valid = [pos[0] <= 0 and direction == "y", pos[1] <=0 and direction == "x", nextvertice[1] >= self.height and direction == "x", pos[0] >= self.height and direction == "x"]
        nextvertice = (self.limitX(nextvertice[0]), self.limitY(nextvertice[1]))
        xsort, ysort = sort([pos[0], nextvertice[0]]), sort([pos[1], nextvertice[1]])
        if(xsort[1] >= self.width or xsort[1] <= 0) : 
            self.simpang.append((self.limitX(xsort[1]), pos[1]))
        if(ysort[1] >= self.height or ysort[1] <= 0) : 
            self.simpang.append((pos[0]+10, self.limitY(ysort[1])))
        if not sum(valid) : 
            #Fungsi untk menggambar jalan
            self.mapDraw.rectangle(((xsort[0], ysort[0]), (xsort[1] , ysort[1] )), "black")
            if direction == "y": 
                self.mapDraw.line(((xsort[0] + 10, ysort[0] + 10), ( xsort[0] +10 , ysort[1] - 10)), "white", 1)
            else : self.mapDraw.line(((xsort[0] + 20 , ysort[0] + 10), ( xsort[1] -10 , ysort[0]+10 )), "white", 1)
        
        nextX = self.width if nextvertice[0] <= 0 else (nextvertice[0] - (20 if direction == "y" else 0) if nextvertice[0] < self.width else 0)
        nextY = self.height if nextvertice[1] <= 0 else (nextvertice[1] - (20 if direction == 'x' else 0) if nextvertice[1] < self.height else 0)
        print((nextX, nextY) , " : last - ", self.lastVertex, self.lastVertex2)
        self.lastVertex = (nextX, nextY)
        self.lastVertex2 = pos
        self.makeRoads((nextX,nextY ),random.choice(["x", 'y']) )
    
    # Membuat map baru setiap kali memilih tombol redesign map
    def createMap(self):
        self.simpang = [(0,0), (0,self.height), (self.width, 0) ,(self.width, self.height)]
        self.len = 0
        self.lastVertex = (random.randrange(0, self.width, self.road_len), random.choice([0, self.height]))
        self.lastVertex2 = (random.randrange(0, self.width, self.road_len), random.choice([0, self.height]))
        self.map = Image.new("RGBA", (self.width, self.height ), (100,100,100))
        self.mapDraw = ImageDraw.Draw(self.map)
        self.makeRoads(self.lastVertex, "y")
        #Save map
        self.map.save("map1.png")
        self.mapping()
        #Save map2
        self.map.save("map2.png")
        return self.map
    
    #Panggil fungsi generate building ketika jalan sudah berada di batas bawah map
    def generateBuilding(self, pos):
        x = pos[0][0]
        # gambar digambarkan secara horizontal
        def getBangunanX(x):
            return [bangunan for bangunan in self.buildings if bangunan.size[0] + x < pos[1][0]-self.padding]
        # gambar diletakkan secara vertikal
        def getBangunanY(x,y):
            return [bangunan for bangunan in self.env if bangunan.size[0] + x < pos[1][0]-self.padding and bangunan.size[1] + y < pos[1][1]-50]
        
        while x < pos[1][0]:
            kandidat = getBangunanX(x)
            if len(kandidat):
                build = random.choice(kandidat)
                self.mapDraw.rectangle(((x, pos[0][1]), (x+build.size[0]+20, pos[0][1]+build.size[1])), "green")
                self.map.paste(build, (x, pos[0][1]))
                x += build.size[0] + self.jarak
            else: break
        x = pos[0][0]
        y = pos[0][1] + 50 + self.padding
    
        while  y < pos[1][1] - 50:
            tertinggi = 50
            while x < pos[1][0] :
                kandidat = getBangunanY(x, y)
                if len(kandidat):
                    build = random.choice(kandidat)
                    self.mapDraw.rectangle(((x,y), (x+build.size[0]+20, y+build.size[1])),"green")
                    self.map.paste(build, (x, random.randint(y, y+(tertinggi - build.size[1]))))
                    tertinggi = max(build.size[1], tertinggi)
                    x += build.size[0] + self.padding
                else : break
            y += tertinggi + self.padding
        x = pos[0][0]
        
        if abs(pos[1][1] - pos[0][1]) < 120: 
            return
        while x < pos[1][0]:
            kandidat = getBangunanX(x)
            if len(kandidat):
                build = random.choice(kandidat)
                self.mapDraw.rectangle(((x, pos[1][1]-build.size[1]), (x+build.size[0]+20, pos[1][1]-build.size[1]+build.size[1])),"green")
                self.map.paste(build, (x, pos[1][1]-build.size[1]))
                x += build.size[0] + self.jarak
            else: break
         
    def mapping(self):
        text = ["" for i in range(len(self.simpang))]
        
        for idx, titik in enumerate(self.simpang):
            if titik[1] > self.height : 
                continue
            nearX, nearY = 0, 0
            for titikTetangga in self.simpang:
                if titik != titikTetangga and titik[0] > 0 and titik[1] > 0:
                    nearX = titikTetangga[0] if  (titikTetangga[0] > nearX and titikTetangga[0] < titik[0] and titik[1] == titikTetangga[1]) else nearX
                    nearY = titikTetangga[1] if  (titikTetangga[1] > nearY and titikTetangga[1] < titik[1]) else nearY
            if idx < len(text) and text[idx] != "":
                text[idx] = ""
            if titik[1] == 1500 : 
                print(titik, ": ", nearX , nearY)
            if titik[0] - nearX >= 30 and titik[1]-nearY >= 30:
                if (titik[0], nearY) not in self.simpang: 
                    self.simpang.append((titik[0], nearY-20))
                if titik[1] < self.width - 20 : self.mapDraw.rectangle(((nearX+1,nearY+1), (titik[0]-1, titik[1]-1)), "gray")
                self.mapDraw.rectangle(((nearX + 10, nearY + 10), (titik[0] - 10, titik[1] - 10)), "green")
                self.generateBuilding(((nearX + 10,nearY + 10), (titik[0] - 10, titik[1] - 10)))

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
        root.title("Map IKN")
        root.bind("<MouseWheel>", self.scroll)

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.map_label = ttk.Label(frame)
        self.map_label.grid(row=0, column=0, padx=10, pady=10)

        generate_button = ttk.Button(root, text="Redesign Map", command=self.update_map)
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
        if event.state & 0x0001:
            self.viewport_x = max(0, self.viewport_x - 20) if event.delta > 0 else min(self.new_map.width, self.viewport_x + 20)
        else:
            self.viewport_y = max(0, self.viewport_y - 20) if event.delta > 0 else min(self.new_map.height, self.viewport_y + 20)
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()
