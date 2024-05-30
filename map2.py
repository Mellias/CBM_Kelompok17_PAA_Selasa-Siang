from PIL import Image, ImageDraw
import random

# Constants
CELL_SIZE = 10
MAP_WIDTH = 150
MAP_HEIGHT = 150
IMAGE_WIDTH = MAP_WIDTH * CELL_SIZE
IMAGE_HEIGHT = MAP_HEIGHT * CELL_SIZE

# Building sizes (width, height)
BIG_BUILDING = (10, 5)
MEDIUM_BUILDING = (5, 3)
SMALL_BUILDING = (2, 2)
HOUSE = (1, 2)

# Colors
ROAD_COLOR = "black"
BIG_BUILDING_COLOR = "gray"
MEDIUM_BUILDING_COLOR = "darkgray"
SMALL_BUILDING_COLOR = "lightgray"
HOUSE_COLOR = "white"
GREEN_SPACE_COLOR = "green"

# Create a blank image
image = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), GREEN_SPACE_COLOR)
draw = ImageDraw.Draw(image)

# Store the positions of placed buildings to avoid overlap
occupied_cells = set()

def draw_rectangle(draw, top_left, size, color):
    x, y = top_left
    width, height = size
    draw.rectangle([x, y, x + width * CELL_SIZE, y + height * CELL_SIZE], fill=color)

def is_area_free(top_left, size):
    x, y = top_left
    width, height = size
    for i in range(width):
        for j in range(height):
            if (x + i, y + j) in occupied_cells:
                return False
    return True

def place_building(size, color):
    while True:
        x = random.randint(0, MAP_WIDTH - size[0])
        y = random.randint(0, MAP_HEIGHT - size[1])
        if is_area_free((x, y), size):
            draw_rectangle(draw, (x * CELL_SIZE, y * CELL_SIZE), size, color)
            for i in range(size[0]):
                for j in range(size[1]):
                    occupied_cells.add((x + i, y + j))
            break

def create_map():
    # Reset the map
    global image, draw, occupied_cells
    image = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), GREEN_SPACE_COLOR)
    draw = ImageDraw.Draw(image)
    occupied_cells = set()
    
    # Place the big building
    place_building(BIG_BUILDING, BIG_BUILDING_COLOR)
    
    # Place medium buildings
    for _ in range(4):
        place_building(MEDIUM_BUILDING, MEDIUM_BUILDING_COLOR)
    
    # Place small buildings
    for _ in range(10):
        place_building(SMALL_BUILDING, SMALL_BUILDING_COLOR)
    
    # Place houses
    for _ in range(10):
        place_building(HOUSE, HOUSE_COLOR)
    
    # Create roads
    create_roads()

def create_roads():
    # Simple horizontal and vertical roads
    for i in range(0, MAP_WIDTH, 30):
        draw.rectangle([i * CELL_SIZE, 0, (i + 2) * CELL_SIZE, IMAGE_HEIGHT], fill=ROAD_COLOR)
    for j in range(0, MAP_HEIGHT, 30):
        draw.rectangle([0, j * CELL_SIZE, IMAGE_WIDTH, (j + 2) * CELL_SIZE], fill=ROAD_COLOR)

def save_map():
    image.show()
    image.save("city_map.png")

create_map()
save_map()
