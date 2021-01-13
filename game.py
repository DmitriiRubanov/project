import pygame
import sys
import os

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

running = True
while running:
    # внутри игрового цикла ещё один цикл
    # приема и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()
