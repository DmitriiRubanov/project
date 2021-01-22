import pygame
import sys
import os
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
import sqlite3

pygame.init()
clock = pygame.time.Clock()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
panels = pygame.sprite.Group()
red_button_sprites = pygame.sprite.Group()
green_button_sprites = pygame.sprite.Group()
blue_button_sprites = pygame.sprite.Group()
car_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()
lst1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
images = []
running = True
reverse = False
checheeee = []
save = False
yeah = False
load_sprites = pygame.sprite.Group()
off_button = pygame.sprite.Group()
come_car = False
check = False
new = True
results = False
i = 0
black = pygame.sprite.Group()
sound = pygame.mixer.Sound('data/54047__guitarguy1985__buzzer.wav')
sound1 = pygame.mixer.Sound('data/jg-032316-sfx-elevator-button.mp3')
sound2 = pygame.mixer.Sound('data/race-car-driving-away_f1l83s4d-[AudioTrimmer.com].mp3')
sound3 = pygame.mixer.Sound('data/race-car-driving-away_f1l83s4d-[AudioTrimmer.com] (1).mp3')
loading = False
sound4 = pygame.mixer.Sound('data/72372e56a594c6f.mp3')
menu = True
nado = [True, False, True, False, True, True, True, False, True, False]
con = sqlite3.connect('records.db')
cur = con.cursor()
result = ''
write = False
balls = 0


class Result(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/untitled.ui', self)
        self.pushButton.clicked.connect(self.results)

    def results(self):
        global result, balls
        for i in range(10):
            if nado[i] == checheeee[i]:
                balls += 1
        balls *= 100
        txt = self.lineEdit.text()
        result = cur.execute("""INSERT INTO recorde(name,score) VALUES(?,?)""", (txt, balls,))
        con.commit()
        self.close()


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
    reverse_image = load_image('reverse_car.png')
    image = load_image('car.png')
    normal_car = load_image('car.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = -150
        self.n = 0

    def update(self):
        global come_car, check, x, y, reverse, yeah, new, loading
        if reverse:
            self.image = self.reverse_image
            if self.rect.x != -600:
                self.rect.x -= 5
            else:
                self.image = self.normal_car
                check = False
                reverse = False
                new = True
        elif come_car:
            if self.rect.x != 15:
                self.rect.x += 5
            else:
                loading = True
                check = True
                come_car = False
                x = 490
                y = 298
        elif yeah:
            if self.rect.x != 1005:
                self.rect.x += 5
            else:
                check = False
                yeah = False
                self.rect.x = -500
                new = True


class GreenButton(pygame.sprite.Sprite):
    image = load_image('knopka1.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = GreenButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 989
        self.rect.y = 309

    def update(self, *args):
        global check, yeah, i, checheeee
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and check:
            sound1.play()
            check = False
            yeah = True
            sound3.play()
            i += 1
            checheeee.append(True)


class RedButton(pygame.sprite.Sprite):
    image = load_image('knopka2.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = RedButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 1134
        self.rect.y = 310

    def update(self, *args):
        global check, reverse, i, checheeee
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and check:
            sound1.play()
            time.sleep(0.1)
            check = False
            reverse = True
            sound2.play()
            i += 1
            checheeee.append(False)


class BlueButton(pygame.sprite.Sprite):
    image = load_image('knopka3.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = BlueButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 114
        self.rect.y = 574

    def update(self, *args):
        global come_car, new, i, results
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and new:
            sound.play()
            time.sleep(2)
            sound2.play()
            come_car = True
            new = False


class Off(pygame.sprite.Sprite):
    image = load_image('off.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Off.image
        self.rect = self.image.get_rect()
        self.rect.x = 1230
        self.rect.y = 0

    def update(self, *args):
        global menu
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            menu = True


class Start(pygame.sprite.Sprite):
    image = load_image('start.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Start.image
        self.rect = self.image.get_rect()
        self.rect.x = 540
        self.rect.y = 291

    def update(self, *args):
        global menu
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            menu = False


class Exit(pygame.sprite.Sprite):
    image = load_image('exit.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Exit.image
        self.rect = self.image.get_rect()
        self.rect.x = 540
        self.rect.y = 428

    def update(self, *args):
        global running, results
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            running = False


class Menu(pygame.sprite.Sprite):
    image = load_image('maxresdefault.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Menu.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        global menu
        self.rect.x = 0
        self.rect.y = 0


class Panel(pygame.sprite.Sprite):
    image = load_image('1.png')
    image1 = load_image('2.png')
    image2 = load_image('3.png')
    image3 = load_image('4.png')
    image4 = load_image('5.png')
    image5 = load_image('6.png')
    image6 = load_image('7.png')
    image7 = load_image('8.png')
    image8 = load_image('9.png')
    image9 = load_image('10.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Panel.image
        self.rect = self.image.get_rect()
        self.rect.x = -700
        self.rect.y = -700

    def update(self, *args):
        global i, results, save, menu
        if i == 0:
            self.rect.x = 432
            self.rect.y = 236
        if i == 1:
            self.image = self.image1
        if i == 2:
            self.image = self.image2
        if i == 3:
            self.image = self.image3
        if i == 4:
            self.image = self.image4
        if i == 5:
            self.image = self.image5
        if i == 6:
            self.image = self.image6
        if i == 7:
            self.image = self.image7
        if i == 8:
            self.image = self.image8
        if i == 9:
            self.image = self.image9
        if i == 10:
            results = True
            save = True


class ExitGame(pygame.sprite.Sprite):
    image = load_image('exit.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = ExitGame.image
        self.rect = self.image.get_rect()
        self.rect.x = 981
        self.rect.y = 610

    def update(self, *args):
        global running, results
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            running = False

x = -500
y = -500
EnterFace(main_sprites)
Car(car_sprites)
Off(off_button)
GreenButton(green_button_sprites)
BlueButton(blue_button_sprites)
RedButton(red_button_sprites)
Panel(panels)
menuu = pygame.sprite.Group()
Menu(menuu)
start = pygame.sprite.Group()
Start(start)
ex = pygame.sprite.Group()
Exit(ex)
exit_game = pygame.sprite.Group()
ExitGame(exit_game)
pygame.mixer.music.load('data/Papers, Please - Arstotzkan Anthem.mp3')
pygame.mixer.music.play()
while running:
    # внутри игрового цикла ещё один цикл
    if menu:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            menuu.update()
            start.update(event)
            ex.update(event)
        screen.fill((110, 111, 109))
        menuu.draw(screen)
        start.draw(screen)
        ex.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    elif results:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            menuu.update()
            exit_game.update(event)
        if save:
            app = QApplication(sys.argv)
            n = Result()
            n.show()
            save = False

        screen.fill((110, 111, 109))
        menuu.draw(screen)
        exit_game.draw(screen)
        font = pygame.font.Font(None, 40)
        result = cur.execute("""SELECT name, score FROM recorde""").fetchall()
        result = sorted(result, key=lambda x: -x[1])
        for i in range(min(len(result), 8)):
            font = pygame.font.Font(None, 40)
            text = font.render(result[i][0] + ' - ' + str(result[i][1]), True, (255, 255, 255))
            screen.blit(text, (100, 170 + 50 * i))
        clock.tick(60)
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            blue_button_sprites.update(event)
            green_button_sprites.update(event)
            red_button_sprites.update(event)
            black.update()
            off_button.update(event)
            if check:
                panels.update(event)
        screen.fill((110, 111, 109))
        main_sprites.draw(screen)
        blue_button_sprites.draw(screen)
        green_button_sprites.draw(screen)
        red_button_sprites.draw(screen)
        car_sprites.draw(screen)
        off_button.draw(screen)
        car_sprites.update()
        black.draw(screen)
        panels.draw(screen)
        clock.tick(60)
        pygame.display.flip()
pygame.quit()
