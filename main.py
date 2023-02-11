"""
MIT License

Copyright (c) 2023 Rasim Mert YILDIRIM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pygame
import threading
import time
import random

resolution = (1000, 1000)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('Escape From Snakes')
background_color = (0, 0, 0)

FPS = 30
delay = round(1 / FPS, 4)

block_size = 20
left, up, right, down = (-block_size, 0), (0, -block_size), (block_size, 0), (0, block_size)

snake_limit = 20
score_per_frame = 1
score_per_kill = 100

NL = "*" * 20 + "\n"

keep_running = True

def random_position():
    while True:
        position = ((random.randint(0, 1000) // block_size) * block_size, (random.randint(0, 1000) // block_size) * block_size)
        if position != (apple.x, apple.y):
            return position

def random_color():
    while True:
        random_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        if random_color != (0, 0, 0):
            return random_color

pygame.init()

class Snake:
    def __init__(self, position, color, length, head_color):
        self.positions = [position for _ in range(length)]
        self.head_color = head_color
        self.x, self.y = position
        self.direction = None
        self.directions = []
        self.length = length
        self.color = color
        self.alive = True

        threading.Thread(target=self.loop).start()

    def decide(self):
        self.directions = []
        if self.x < apple.x and self.direction != left:
            self.directions.append(right)
        elif self.x > apple.x and self.direction != right:
            self.directions.append(left)
        if self.y < apple.y and self.direction != up:
            self.directions.append(down)
        elif self.y > apple.y and self.direction != down:
            self.directions.append(up)
        else:
            self.directions.append(self.direction)
        self.direction = random.choice(self.directions)

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

    def check_length(self):
        while len(self.positions) > self.length:
            self.positions.pop(0)

    def check_collisions(self):
        if (self.x, self.y) in self.positions:
            self.die()
        else:
            self.positions.append((self.x, self.y))

    def die(self):
        self.alive = False
        score.increase(score_per_kill)
        snakes._list_.remove(self)
        snakes.snake_count -= 1
        snakes.create_snake(2)

    def draw(self):
        for x, y in self.positions:
            pygame.draw.rect(screen, self.color, (x, y, block_size, block_size))
        # draw head
        pygame.draw.rect(screen, self.head_color, (self.x, self.y, block_size, block_size))


    def loop(self):
        while self.alive and keep_running:
            self.decide()
            self.move()
            self.check_length()
            self.draw()
            self.check_collisions()
            time.sleep(delay)


class Snakes:
    def __init__(self, limit):
        self.snake_count = 0
        self.limit = limit
        self._list_ = []

    def create_snake(self, count=1):
        if self.snake_count < self.limit:
            for _ in range(count):
                self._list_.append(Snake(length=random.randint(5, 40),
                                         position=random_position(),
                                         head_color=random_color(),
                                         color=random_color()))
                self.snake_count += 1

    def kill_all(self):
        for snake in self._list_:
            snake.die()
        self.snake_count = 0
        self._list_ = []

class Apple:
    def __init__(self, color=(255, 0, 0)):
        self.update_position()
        self.color = color

    def update_position(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.x = (self.x // block_size) * block_size
        self.y = (self.y // block_size) * block_size

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, block_size, block_size))

    def check_collisions(self):
        for snake in snakes._list_:
            if (self.x, self.y) in snake.positions:
                self.quit()
                break

    def quit(self):
        global keep_running
        keep_running = False
        print(NL + NL + f" Score: {score.value} ".center(20, "*")  + "\n" + NL + NL)

    def loop(self):
        while keep_running:
            self.update_position()
            self.draw()
            self.check_collisions()
            time.sleep(delay)


class Score:
    def __init__(self, position=(0, 0), text_color=(255, 255, 255)):
        self.value = 0
        self.position = position
        self.text_color = text_color
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def update_text(self):
        self.text = self.font.render(f'Score: {self.value}', True, self.text_color)

    def increase(self, value_to_add):
        self.value += value_to_add

    def draw(self):
        screen.blit(self.text, self.position)

    def loop(self):
        while keep_running:
            self.increase(score_per_frame)
            self.update_text()
            self.draw()
            time.sleep(delay)


apple = Apple()
score = Score()
snakes = Snakes(limit=snake_limit)

def main():
    def fill_and_update_screen():
        while keep_running:
            screen.fill(background_color)
            time.sleep(delay)
            pygame.display.update()

    threading.Thread(target=fill_and_update_screen).start()
    threading.Thread(target=score.loop).start()
    threading.Thread(target=apple.loop).start()
    snakes.create_snake(1)

main()

while keep_running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            keep_running = False

    time.sleep(delay)
    
