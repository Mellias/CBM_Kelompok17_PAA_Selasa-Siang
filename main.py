from PIL import Image, ImageTk
import tkinter as tk
import random

# ukuran peta
MAP_SIZE = 150
CELL_SIZE = 32

# Konstanta untuk jenis jalan
EMPTY = 0
JALAN = 'road'
CROSSROAD = 'crossroad'
T_JUNCTION = 't_junction'
TURN = 'turn'

# Batas jumlah jenis jalan
CROSSROAD_LIMIT = 10
T_JUNCTION_LIMIT = 12
TURN_LIMIT = 30

# Jarak minimal antara jalan
MIN_DISTANCE = 5

# Konstanta ukuran bangunan
BANGUNAN_BESAR = 'big_building'
BANGUNAN_SEDANG = 'medium_building'
BANGUNAN_KECIL = 'small_building'
RUMAH = 'house'
POHON = 'tree'

UKURAN_BANGUNAN = {
    BANGUNAN_BESAR: (10, 5),
    BANGUNAN_SEDANG: (5, 3),
    BANGUNAN_KECIL: (2, 2),
    RUMAH: (1, 2),
    POHON: (1, 1)
}

GAMBAR_BANGUNAN = {
    BANGUNAN_BESAR: 'big_building.png',
    BANGUNAN_SEDANG: 'medium_building.png',
    BANGUNAN_KECIL: 'small_building.png',
    RUMAH: 'house.png',
    POHON: 'tree.png'
}

MINIMUM_BANGUNAN = {
    BANGUNAN_BESAR: 45,
    BANGUNAN_SEDANG: 100,
    BANGUNAN_KECIL: 150,
    RUMAH: 200,
    POHON: 400
}

class MapGenerator:
    def __init__(self, size):
        self.size = size
        self.map = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.generate_map()
    
    def generate_map(self):
        # MEMBERSIHKAN PETA
        self.map = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        crossroad_count = 0
        t_junction_count = 0
        turn_count = 0

        while crossroad_count < CROSSROAD_LIMIT or t_junction_count < T_JUNCTION_LIMIT or turn_count < TURN_LIMIT:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            if self.map[x][y] == EMPTY and self.is_location_valid(x, y):
                if crossroad_count < CROSSROAD_LIMIT:
                    self.map[x][y] = CROSSROAD
                    self.extend_road(x, y, 'up')
                    self.extend_road(x, y, 'down')
                    self.extend_road(x, y, 'left')
                    self.extend_road(x, y, 'right')
                    crossroad_count += 1
                elif t_junction_count < T_JUNCTION_LIMIT:
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    if direction == 'up':
                        self.map[x][y] = 'tjunction_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down':
                        self.map[x][y] = 'tjunction_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'left':
                        self.map[x][y] = 'tjunction_left'
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    elif direction == 'right':
                        self.map[x][y] = 'tjunction_right'
                        self.extend_road(x, y, 'right')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    t_junction_count += 1
                elif turn_count < TURN_LIMIT:
                    direction = random.choice(['up-right', 'up-left', 'down-right', 'down-left'])
                    if direction == 'up-right':
                        self.map[x][y] = 'turn_right_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'right')
                    elif direction == 'up-left':
                        self.map[x][y] = 'turn_left_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                    elif direction == 'down-right':
                        self.map[x][y] = 'turn_right_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down-left':
                        self.map[x][y] = 'turn_left_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                    turn_count += 1

        self.place_buildings()
        self.place_trees()

    def is_location_valid(self, x, y, width=1, height=1):
        for a in range(max(0, x - MIN_DISTANCE), min(self.size, x + width + MIN_DISTANCE)):
            for b in range(max(0, y - MIN_DISTANCE), min(self.size, y + height + MIN_DISTANCE)):
                if self.map[a][b] != EMPTY:
                    return False
        return True

    def extend_road(self, x, y, direction):
        if direction == 'up':
            for a in range(x-1, -1, -1):
                if self.map[a][y] != EMPTY:
                    break
                self.map[a][y] = 'vertical_road'
        elif direction == 'down':
            for a in range(x+1, self.size):
                if self.map[a][y] != EMPTY:
                    break
                self.map[a][y] = 'vertical_road'
        elif direction == 'left':
            for b in range(y-1, -1, -1):
                if self.map[x][b] != EMPTY:
                    break
                self.map[x][b] = 'horizontal_road'
        elif direction == 'right':
            for b in range(y+1, self.size):
                if self.map[x][b] != EMPTY:
                    break
                self.map[x][b] = 'horizontal_road'

    def place_buildings(self):
        for building, minimum in MINIMUM_BANGUNAN.items():
            if building == POHON:
                continue
            count = 0
            while count < minimum:
                x = random.randint(0, self.size - UKURAN_BANGUNAN[building][0])
                y = random.randint(0, self.size - UKURAN_BANGUNAN[building][1])
                if self.is_location_valid_for_building(x, y, UKURAN_BANGUNAN[building][0], UKURAN_BANGUNAN[building][1]):
                    for a in range(x, x + UKURAN_BANGUNAN[building][0]):
                        for b in range(y, y + UKURAN_BANGUNAN[building][1]):
                            self.map[a][b] = building
                    count += 1

    def place_trees(self):
        count = 0
        while count < MINIMUM_BANGUNAN[POHON]:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.map[x][y] == EMPTY:
                self.map[x][y] = POHON
                count += 1

    def is_location_valid_for_building(self, x, y, width, height):
        # periksa apakah ada sel di area yang diusulkan yang merupakan jalan atau bangunan lain
        for a in range(x, x + width):
            for b in range(y, y + height):
                if a >= 0 and a < self.size and b >= 0 and b < self.size:
                    if self.map[a][b] != EMPTY:
                        return False
        # periksa sel di sekitarnya untuk mencari jalan dalam jarak 1 sel
        road_found = False
        for a in range(max(0, x - 1), min(self.size, x + width + 1)):
            for b in range(max(0, y - 1), min(self.size, y + height + 1)):
                if self.map[a][b] in ['vertical_road', 'horizontal_road', CROSSROAD, 'tjunction_up', 'tjunction_down', 'tjunction_left', 'tjunction_right', 'turn_right_up', 'turn_left_up', 'turn_right_down', 'turn_left_down']:
                    road_found = True
                # memastikan jarak minimal 2 sel dari bangunan lain
                if a in range(x, x + width) and b in range(y, y + height):
                    continue
                if self.map[a][b] in UKURAN_BANGUNAN:
                    return False
        return road_found

    def get_map(self):
        return self.map

class MapDisplay(tk.Frame):
    def __init__(self, parent, map_data):
        super().__init__(parent)
        self.parent = parent
        self.map_data = map_data

        # memuat gambar
        self.images = {
            'vertical_road': ImageTk.PhotoImage(Image.open("asset/vertical_road.png")),
            'horizontal_road': ImageTk.PhotoImage(Image.open("asset/horizontal_road.png")),
            'crossroad': ImageTk.PhotoImage(Image.open("asset/crossroad.png")),
            'tjunction_up': ImageTk.PhotoImage(Image.open("asset/tjunction_up.png")),
            'tjunction_down': ImageTk.PhotoImage(Image.open("asset/tjunction_down.png")),
            'tjunction_left': ImageTk.PhotoImage(Image.open("asset/tjunction_left.png")),
            'tjunction_right': ImageTk.PhotoImage(Image.open("asset/tjunction_right.png")),
            'turn_left_down': ImageTk.PhotoImage(Image.open("asset/turn_left_down.png")),
            'turn_left_up': ImageTk.PhotoImage(Image.open("asset/turn_left_up.png")),
            'turn_right_up': ImageTk.PhotoImage(Image.open("asset/turn_right_up.png")),
            'turn_right_down': ImageTk.PhotoImage(Image.open("asset/turn_right_down.png")),
            BANGUNAN_BESAR: ImageTk.PhotoImage(Image.open(f"asset/{GAMBAR_BANGUNAN[BANGUNAN_BESAR]}")),
            BANGUNAN_SEDANG: ImageTk.PhotoImage(Image.open(f"asset/{GAMBAR_BANGUNAN[BANGUNAN_SEDANG]}")),
            BANGUNAN_KECIL: ImageTk.PhotoImage(Image.open(f"asset/{GAMBAR_BANGUNAN[BANGUNAN_KECIL]}")),
            RUMAH: ImageTk.PhotoImage(Image.open(f"asset/{GAMBAR_BANGUNAN[RUMAH]}")),
            POHON: ImageTk.PhotoImage(Image.open(f"asset/{GAMBAR_BANGUNAN[POHON]}")),
            'grass': ImageTk.PhotoImage(Image.open("asset/grass.png"))  # tambahkan gambar rumput
        }

        # frame untuk kanvas peta dan tombol
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # kanvas untuk menampilkan peta dengan scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg="grey", scrollregion=(0, 0, MAP_SIZE * CELL_SIZE, MAP_SIZE * CELL_SIZE))
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.hbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky=tk.EW)
        self.vbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.draw_map()

        # frame untuk tombol
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=2, padx=10, pady=10, sticky=tk.N)

        self.redesign_button = tk.Button(self.button_frame, text="REDESIGN", command=self.redesign_map)
        self.redesign_button.pack()

    def draw_map(self):
        self.canvas.delete("all")
        for a in range(MAP_SIZE):
            for b in range(MAP_SIZE):
                cell_type = self.map_data[a][b]
                if cell_type in self.images:
                    if cell_type in UKURAN_BANGUNAN:
                        building_size = UKURAN_BANGUNAN[cell_type]
                        if self.is_top_left_of_building(a, b, building_size):
                            self.canvas.create_image(b * CELL_SIZE, a * CELL_SIZE, anchor=tk.NW, image=self.images[cell_type])
                    else:
                        self.canvas.create_image(b * CELL_SIZE, a * CELL_SIZE, anchor=tk.NW, image=self.images[cell_type])
                else:
                    self.canvas.create_image(b * CELL_SIZE, a * CELL_SIZE, anchor=tk.NW, image=self.images['grass'])

    def is_top_left_of_building(self, a, b, building_size):
        if a + building_size[0] <= MAP_SIZE and b + building_size[1] <= MAP_SIZE:
            for x in range(building_size[0]):
                for y in range(building_size[1]):
                    if self.map_data[a + x][b + y] != self.map_data[a][b]:
                        return False
            return True
        return False

    def redesign_map(self):
        # buat data peta baru
        map_generator = MapGenerator(MAP_SIZE)
        self.map_data = map_generator.get_map()
        # gambar ulang map
        self.draw_map()

def main():
    root = tk.Tk()
    root.title("Map IKN")

    map_generator = MapGenerator(MAP_SIZE)
    map_data = map_generator.get_map()
    map_display = MapDisplay(root, map_data)
    map_display.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
