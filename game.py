import pygame
import sys
import os

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class EnterFace(pygame.sprite.Sprite):
    image = load_image("game.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = EnterFace.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


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
