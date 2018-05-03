import pygame
from pygame.math import Vector2
from enum import Enum
import random


class Snake:
    class Direction(Enum):
        UP = 0
        DOWN = 1
        RIGHT = 2
        LEFT = 3

    class Part:
        def __init__(self, pos, n=None, p=None):
            self.part_pos = pos
            self.next_n = n
            self.prev_n = p

    def __init__(self, game, speed, size_b):
        self.game = game
        self.size = self.game.screen.get_size()
        self.pos = Vector2(self.size[0] / 2, self.size[1] / 2)
        self.block_size = size_b
        self.speed = speed
        self.length = 1
        self.direction = self.Direction.UP
        self.act_dir = self.pos
        self.head = self.Part(self.pos)
        self.tail = self.head
        self.point = False
        self.point_loc = Vector2(0, 0)

    def push(self, pos):
        new_node = self.Part(pos, self.head)
        if self.head:
            self.head.prev_n = new_node
        self.head = new_node
        self.length += 1

    def pop(self):
        self.length -= 1
        if self.tail.prev_n:
            self.tail = self.tail.prev_n
            self.tail.next_n = None

    def is_in(self, vec):
        tmp = self.head.next_n
        while tmp:
            if tmp.part_pos.x == vec.x and tmp.part_pos.y == vec.y:
                return True
            tmp = tmp.next_n
        return False

    def point_collected(self):
        self.length += 1
        self.move()

    def move(self):
        if self.direction == self.direction.RIGHT:
            self.push(Vector2(self.head.part_pos.x + self.block_size, self.head.part_pos.y))
        if self.direction == self.direction.LEFT:
            self.push(Vector2(self.head.part_pos.x - self.block_size, self.head.part_pos.y))
        if self.direction == self.direction.UP:
            self.push(Vector2(self.head.part_pos.x, self.head.part_pos.y - self.block_size))
        if self.direction == self.direction.DOWN:
            self.push(Vector2(self.head.part_pos.x, self.head.part_pos.y + self.block_size))

    def rand_point(self):
        if not self.point:
            self.point_loc.x = random.randrange(0, self.size[0], self.block_size)
            self.point_loc.y = random.randrange(0, self.size[1], self.block_size)
            self.point = True

    def collision(self):
        if self.head.part_pos.x == self.point_loc.x and \
                self.head.part_pos.y == self.point_loc.y:
            self.point_collected()
            self.point = False
            return 1
        if self.is_in(self.head.part_pos) or self.head.part_pos.x < 0 or self.head.part_pos.y < 0 \
                or self.head.part_pos.y > self.size[1] or self.head.part_pos.x > self.size[0]:
            return -1
        return 0

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and self.direction != self.direction.DOWN:
            self.direction = self.direction.UP
        if pressed[pygame.K_DOWN] and self.direction != self.direction.UP:
            self.direction = self.direction.DOWN
        if pressed[pygame.K_RIGHT] and self.direction != self.direction.LEFT:
            self.direction = self.direction.RIGHT
        if pressed[pygame.K_LEFT] and self.direction != self.direction.RIGHT:
            self.direction = self.direction.LEFT
        self.rand_point()
        self.move()
        self.pop()

    def draw(self):
        block = self.head
        while block:
            block_s = (block.part_pos.x, block.part_pos.y, self.block_size, self.block_size)
            pygame.draw.rect(self.game.screen, (0, 100, 255), block_s)
            block = block.next_n
        block_point = (self.point_loc.x, self.point_loc.y, self.block_size, self.block_size)
        pygame.draw.rect(self.game.screen, (255, 100, 0), block_point)
