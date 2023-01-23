import pyglet
from random import randrange

# konstanta velikost jednoho čtverce
SQUARE = 64 # v pixelech

# velikost herního pole je 10 x 10
window = pyglet.window.Window(width=SQUARE*10, height=SQUARE*10)

class Game_state:
    def __init__(self):
        self.snake = [(0, 0), (0, 1), (0, 2), (1, 2)]
        self.way = "right"
        self.food = []
        self.add_food()
    

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

def move(self):
    """Nastavení pohybu hada na základě použité klávesy od hráče (WSAD)"""
    x, y = game.snake[-1]
    if game.way == "right":
        new_head = (x + 1, y) # úprava původní hlavy
    elif game.way == "left":
        new_head = (x - 1, y) # úprava původní hlavy
    elif game.way == "up":
        new_head = (x, y + 1) # úprava původní hlavy
    elif game.way == "down":
        new_head = (x, y - 1) # úprava původní hlavy
    game.snake.append(new_head) # přidání nové hlavy hada
    # del game.snake[0] # smazání první souřadnice

    body_snake = game.snake[0:-1] # tělo hada (bez hlavy)
    # had, když narazí do stěny, hra končí
    if x == -1 or x == 10 or y == -1 or y == 10:
        pyglet.clock.unschedule(move)
    # had, když narazí do sebe sama, hra končí
    if new_head in body_snake:
        pyglet.clock.unschedule(move)

    if new_head not in game.food:
        del game.snake[0] # smazání první souřadnici
    # pojídání jídla hadem
    elif new_head in game.food: # jidlo had
        game.food.remove(new_head) # smaže jídlo hada
        game.snake.append(new_head) # had se prodlouží o danou souřadnici s jídlem
        game.add_food() # přidá další náhodné jídlo pro hada

        

pyglet.clock.schedule_interval(move, 1/2)

# ovládání pomocí kláves "wsad" (změna atributu self.way pomocí kláves)
def button(text):
    if text == "d":
        game.way = "right"
    elif text == "a":
        game.way = "left"
    elif text == "w":
        game.way = "up"
    elif text == "s":
        game.way = "down"

game = Game_state() # vytvoření objektu "game"

# zelená dlaždice
image_green = pyglet.image.load("tail.png")
green_tile = pyglet.sprite.Sprite(image_green)

# jablko
image_apple = pyglet.image.load("apple.png")
apple = pyglet.sprite.Sprite(image_apple)

def draw():
    window.clear()
    # vykreslení hada
    for (x, y) in game.snake:
        green_tile.x = x * SQUARE
        green_tile.y = y * SQUARE
        green_tile.draw()
    # vykreslení jídla (jablka)
    for (x, y) in game.food:
        apple.x = x * SQUARE
        apple.y = y * SQUARE
        apple.draw()
        
window.push_handlers(
    on_text=button,
    on_draw=draw
    )

pyglet.app.run()