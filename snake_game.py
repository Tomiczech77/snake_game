import pyglet
from random import randrange
from pathlib import Path

# instance pro složku s obrázky na grafiku hada
TILES_DIRECTORY = Path("snake-tiles")

# konstanta velikost jednoho čtverce
SQUARE = 64 # v pixelech

# velikost herního pole je 10 x 10
GAME_FIELD_SIZE = 10
window = pyglet.window.Window(width=SQUARE*GAME_FIELD_SIZE, height=SQUARE*GAME_FIELD_SIZE)
pyglet.text.layout

class Game_state:
    def __init__(self):
        self.snake = [(0, 0), (0, 1), (0, 2), (1, 2)]
        self.snake_sprites = []
        self.snake_directions = ['tail-top', 'bottom-top', 'bottom-head']
        self.way = "right"
        self.food = []
        self.add_food()
        self.width = GAME_FIELD_SIZE
        self.height = GAME_FIELD_SIZE
        image_background = pyglet.image.load("background.jpg")
        self.background = pyglet.sprite.Sprite(image_background)
        self.background.scale = 0.6

    def add_food(self):
        """Přidá jídlo pro hada"""
        while True:
            if self.food == []:
                x = randrange(0, 10)
                y = randrange(0, 10)
                if (x, y) in self.snake:
                    continue
                else:
                    self.food.append((x, y))
                    break
    
    def move(self, t):
        """Nastavení pohybu hada na základě použité klávesy od hráče (WSAD)"""
        x, y = self.snake[-1]
        if self.way == "right":
            new_head = (x + 1, y) # úprava původní hlavy
        elif self.way == "left":
            new_head = (x - 1, y) # úprava původní hlavy
        elif self.way == "up":
            new_head = (x, y + 1) # úprava původní hlavy
        elif self.way == "down":
            new_head = (x, y - 1) # úprava původní hlavy

        # had, když narazí do stěny, hra končí
        (x, y) = new_head
        if x < 0 or x > 9 or y < 0 or y > 9:
            pyglet.clock.unschedule(self.move)
            return

        # had, když narazí do sebe sama, hra končí
        if new_head in self.snake:
            pyglet.clock.unschedule(self.move)
            return

        if new_head not in self.food:
            del self.snake[0] # smazání první souřadnici

        # pojídání jídla hadem
        if new_head in self.food: # jidlo had
            self.food.remove(new_head) # smaže jídlo hada
            self.add_food() # přidá další náhodné jídlo pro hada
        self.snake.append(new_head) # had se prodlouží o danou souřadnici s jídlem


    #ovládání pomocí kláves "wsad" (změna atributu self.way pomocí kláves)
    def button(self, text):
        """Nastavení směru po stisknutí klávesy"""
        # pyglet.window.key.UP
        # pyglet.window.key.DOWN
        # pyglet.window.key.LEFT
        # pyglet.window.key.RIGHT
        if text == "d":
            game.way = "right"
        elif text == "a":
            game.way = "left"
        elif text == "w":
            game.way = "up"
        elif text == "s":
            game.way = "down"


    def draw(self):
        """Vykresluje"""
        window.clear()
        # pozadí herního okna
        game.background.draw()
        # vykreslení hada na dané souřadnici
        for (x, y) in self.snake:
            green_tile.x = x * SQUARE
            green_tile.y = y * SQUARE
            green_tile.draw()
        # vykreslení jídla (jablka)
        for (x, y) in self.food:
            apple.x = x * SQUARE
            apple.y = y * SQUARE
            apple.draw()
    


    def draw_snake_parts(self):
        '''
        Draw the right IMG for each part of snake on the right place.
        '''
        self.snake_sprites.clear()
        for index, xy in enumerate(self.snake):
            x = xy[0]*GAME_FIELD_SIZE
            y = xy[1]*GAME_FIELD_SIZE
            IMG_name = self.snake_directions[index]
            self.snake_sprites.append(pyglet.sprite.Sprite(snake_tiles[IMG_name], x, y, batch=batch))



        



# cyklus for, který přidává obrázky do slovníku snake_tiles
snake_tiles = {}
for path in TILES_DIRECTORY.glob("*.png"):
    snake_tiles[path.stem] = pyglet.image.load(path)


# vytvoření objektu "game" + rozpohybování hada
game = Game_state()
pyglet.clock.schedule_interval(game.move, 1/4)
batch = pyglet.graphics.Batch()


# zelená dlaždice
image_green = snake_tiles["tail-head"]
green_tile = pyglet.sprite.Sprite(image_green)

# jablko
image_apple = pyglet.image.load("apple.png")
apple = pyglet.sprite.Sprite(image_apple)

# registrace funkcí
window.push_handlers(
    on_text=game.button,
    on_draw=game.draw
    )

pyglet.app.run()