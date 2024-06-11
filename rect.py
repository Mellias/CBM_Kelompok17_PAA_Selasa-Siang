from PIL import Image, ImageDraw

map = Image.new("RGBA", (1500, 1500), "lightgreen")
drawMap = ImageDraw.Draw(map)

map.show()
map.save("square.png")