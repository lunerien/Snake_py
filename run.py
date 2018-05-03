import pygame
import sys
from snake import Snake


class Game(object):
    def __init__(self):
        # Config
        self.max_tps = 10

        # Initialization
        pygame.init()
        self.myFont = pygame.font.SysFont("monospace", 15)
        self.screen = pygame.display.set_mode((1280, 720))
        self.tps_clock = pygame.time.Clock()
        self.points = 0

        self.player = Snake(self, 0.5, 20)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # Rendering
            self.screen.fill((0, 0, 0))
            self.tick()
            self.draw()
            pygame.display.flip()

            self.tps_clock.tick(self.max_tps)

    def tick(self):
        coll = self.player.collision()
        if coll != -1:
            self.points += coll
            self.player.tick()
        else:
            self.points = 0
            self.player = Snake(self, 0.5, 20)

    def draw(self):
        self.player.draw()
        label = self.myFont.render("Points: " + str(self.points), 1, (255, 255, 0))
        self.screen.blit(label, (100, 100))


if __name__ == '__main__':
    Game()
