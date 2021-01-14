import pygame
import sys
import os
import random
import signal
import time

# signal.alarm(2)
# time.sleep(5)
# signal.alarm(0)
pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
random.shuffle(lst)
panels = pygame.sprite.Group()
red_button_sprites = pygame.sprite.Group()
green_button_sprites = pygame.sprite.Group()
blue_button_sprites = pygame.sprite.Group()
car_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()

running = True
off_button = pygame.sprite.Group()
come_car = False
check = False
sound = pygame.mixer.Sound('data/54047__guitarguy1985__buzzer.wav')
sound1 = pygame.mixer.Sound('data/jg-032316-sfx-elevator-button.mp3')


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


class Car(pygame.sprite.Sprite):
    image = load_image('car.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = -150

    def update(self):
        global come_car, check
        if self.rect.x != 15:
            self.rect.x += 1
        else:
            come_car = False
            check = True


class GreenButton(pygame.sprite.Sprite):
    image = load_image('knopka1.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = GreenButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 989
        self.rect.y = 309

    def update(self, *args):
        global check
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and check:
            sound1.play()


class RedButton(pygame.sprite.Sprite):
    image = load_image('knopka2.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = RedButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 1134
        self.rect.y = 310

    def update(self, *args):
        global check
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and check:
            sound1.play()


class BlueButton(pygame.sprite.Sprite):
    image = load_image('knopka3.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = BlueButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 114
        self.rect.y = 574

    def update(self, *args):
        global come_car
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            sound.play()
            time.sleep(2)
            come_car = True


class Off(pygame.sprite.Sprite):
    image = load_image('off.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Off.image
        self.rect = self.image.get_rect()
        self.rect.x = 432
        self.rect.y = 236

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pass


class Panel(pygame.sprite.Sprite):
    global lst
    image = load_image(lst[0] + '.png')
    del lst[0]

    def __init__(self, group):
        super().__init__(group)
        self.image = Panel.image
        self.rect = self.image.get_rect()
        self.rect.x = 432
        self.rect.y = 236


EnterFace(main_sprites)
Car(car_sprites)
Off(off_button)
GreenButton(green_button_sprites)
BlueButton(blue_button_sprites)
RedButton(red_button_sprites)
while running:
    # внутри игрового цикла ещё один цикл
    # приема и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        blue_button_sprites.update(event)
        green_button_sprites.update(event)
        red_button_sprites.update(event)
    screen.fill((199, 195, 194))
    main_sprites.draw(screen)
    blue_button_sprites.draw(screen)
    green_button_sprites.draw(screen)
    red_button_sprites.draw(screen)
    car_sprites.draw(screen)
    off_button.draw(screen)
    if come_car:
        car_sprites.update()
    pygame.display.flip()
pygame.quit()
