import pygame
import json
import os

# === Константы ===
TILE_SIZE = 32
WIDTH, HEIGHT = 640, 480
FPS = 30

# === Классы ===
class Player:
    def __init__(self, filename="player.json"):
        self.filename = filename
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
            self.x = data["x"]
            self.y = data["y"]
            self.health = data["health"]
            self.inventory = data["inventory"]
        else:
            self.x, self.y = 100, 100
            self.health = 20
            self.inventory = {}

    def save(self):
        data = {
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "inventory": self.inventory
        }
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, TILE_SIZE, TILE_SIZE))

    def move(self, dx, dy):
        self.x += dx * TILE_SIZE
        self.y += dy * TILE_SIZE

class World:
    def __init__(self, filename="map.json"):
        self.filename = filename
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
            self.cols = data["cols"]
            self.rows = data["rows"]
            self.tiles = data["tiles"]
        else:
            self.cols, self.rows = 20, 15
            self.tiles = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def save(self):
        data = {"cols": self.cols, "rows": self.rows, "tiles": self.tiles}
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def draw(self, screen):
        colors = {
            0: (135, 206, 235),  # sky
            1: (139, 69, 19),    # dirt
            2: (128, 128, 128)   # stone
        }
        for y in range(self.rows):
            for x in range(self.cols):
                color = colors.get(self.tiles[y][x], (0, 0, 0))
                pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# === Основная игра ===
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player()
    world = World()

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Рисуем
        world.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)

    # Сохраняем перед выходом
    player.save()
    world.save()
    pygame.quit()

if __name__ == "__main__":
    main()
