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
def game_over():
        image_game_over = pyglet.image.load("game_over.png")
        game_over = pyglet.sprite.Sprite(image_game_over)
        return print(game_over)


class Game_state:
    def __init__(self):
        self.snake = [(0, 0), (0, 1), (0, 2)]
        self.way = "up"
        self.food = []
        self.add_food()
        self.skull = []
        self.game_over = False
        self.label = pyglet.text.Label("GAME OVER",
                                    font_name ="Verdana",
                                    font_size = 50,
                                    x = window.width//2, y = window.height//2,
                                    anchor_x="center", anchor_y="center")
        self.label.color = (255, 255, 100, 255)
        self.label.bold = True
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

    def add_skull(self, t):
        """Zkontroluje, jestli hra stále běží.
        Pokud ano, přidá lebku jako past na hada.
        Pokud ne, přeruší se."""
        while True:
            if self.game_over == True:
                break
            self.skull.clear()
            if self.skull == []:
                x = randrange(0, 10)
                y = randrange(0, 10)
                if (x, y) in self.snake:
                    continue
                elif (x, y) in self.food:
                    continue
                else:
                    self.skull.append((x, y))
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

        # had, když narazí do stěny nebo sebe sama nebo sní lebku, hra končí
        (x, y) = new_head
        if (x < 0 or x > 9 or y < 0 or y > 9) or new_head in self.snake or new_head in self.skull:
            self.game_over = True
            pyglet.clock.unschedule(self.move)
            return

        if new_head not in self.food and new_head not in self.skull:
            del self.snake[0] # smazání první souřadnici

        # pojídání jídla hadem
        if new_head in self.food: # jidlo had
            self.food.remove(new_head) # smaže jídlo hada
            self.add_food() # přidá další náhodné jídlo pro hada
        self.snake.append(new_head) # had se prodlouží o danou souřadnici s jídlem


    def button(self, text):
        """Nastavení směru po stisknutí kláves 'WSAD' 
        (změna atributu self.way pomocí kláves)."""
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
        """Vykresluje pozadí, hada, jídlo, lebku a na závěr hry GAME OVER"""
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
        # vykreslení lebky
        for (x, y) in self.skull:
            skull.x = x * SQUARE
            skull.y = y * SQUARE
            skull.draw()
        # když skončí hra, vykreslí se GAME OVER
        if self.game_over == True:
            self.label.draw()

        

    
       
# cyklus for, který přidává obrázky do slovníku snake_tiles
snake_tiles = {}
for path in TILES_DIRECTORY.glob("*.png"):
    snake_tiles[path.stem] = pyglet.image.load(path)



# vytvoření objektu "game" + rozpohybování hada
game = Game_state()
pyglet.clock.schedule_interval(game.move, 1/4)


# každých 5 vteřin se změní souřadnice lebky
pyglet.clock.schedule_interval(game.add_skull, 5)


# načtení podoby hada
image_green = snake_tiles["tail-head"]
green_tile = pyglet.sprite.Sprite(image_green)

# načtení obrázku jablko (červené)
image_apple = pyglet.image.load("apple.png")
apple = pyglet.sprite.Sprite(image_apple)

# načtení obrázku lebka
image_skull = pyglet.image.load("skull.png")
skull = pyglet.sprite.Sprite(image_skull)

# registrace funkcí
window.push_handlers(
    on_text=game.button,
    on_draw=game.draw
    )

pyglet.app.run()

