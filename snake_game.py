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
        self.width = 10
        self.height = 10
        self.move()
    

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
        (x, y) = self.snake[-1]
        if self.way == "right":
            new_head = (x + 1, y) # úprava původní hlavy
        elif self.way == "left":
            new_head = (x - 1, y) # úprava původní hlavy
        elif self.way == "up":
            new_head = (x, y + 1) # úprava původní hlavy
        elif self.way == "down":
            new_head = (x, y - 1) # úprava původní hlavy

        if new_head not in self.food:
            del self.snake[0] # smazání první souřadnici
        # pojídání jídla hadem
        elif new_head in self.food: # jidlo had
            self.food.remove(new_head) # smaže jídlo hada
            self.add_food() # přidá další náhodné jídlo pro hada
        self.snake.append(new_head) # had se prodlouží o danou souřadnici s jídlem

        body_snake = self.snake[0:-1] # tělo hada (bez hlavy)
        # had, když narazí do stěny, hra končí
        if x < 0 or x > 9 or y < 0 or y > 9:
            pyglet.clock.unschedule(move)
        # had, když narazí do sebe sama, hra končí
        elif new_head in body_snake:
            pyglet.clock.unschedule(move)




pyglet.clock.schedule_interval(Game_state.move, 1/4)

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