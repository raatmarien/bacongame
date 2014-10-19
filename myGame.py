import os, sys
import pygame
import math
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

class Enemy(pygame.sprite.Sprite):
    width = 20
    height = 20

    x = 0
    y = 0

    speed_x = 0
    speed_y = 0

    def __init__(self, x, y, speed_x, speed_y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.x = self.x + self.speed_x 
        self.y = self.y + self.speed_y 
        if self.x < 0:
            self.x = 0
            self.speed_x = abs(self.speed_x)
        if self.x > self.screen_width - self.width:
            self.x = self.screen_width - self.width
            self.speed_x = -abs(self.speed_x)
        if self.y < 0:
            self.y = 0
            self.speed_y = abs(self.speed_y)
        if self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height
            self.speed_y = -abs(self.speed_y)

        self.rect.x = self.x
        self.rect.y = self.y

class EnemyOne(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y,8,8)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([2,2])
        self.image.fill((255,255,92))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y

        if self.rect.x < -2:
            self.kill()
        if self.rect.x > screen_width:
            self.kill()
        if self.rect.y < -2:
            self.kill()
        if self.rect.y > screen_height:
            self.kill()

class Player(pygame.sprite.Sprite):
    width = 100
    height = 100

    speed_x = 0
    speed_y = 0

    speed_friction = 0.92
    movement_acceleration = 0.9

    direction = 0
    turn_speed = 0
    turn_friction = 0.60
    turn_acceleration = 0.05

    is_move_forward = False
    is_move_backward = False

    is_turn_right = False
    is_turn_left = False

    is_shoot = False

    def __init__(self, x, y, sprite):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite
        self.orig_image = self.image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def update(self):
        if self.is_move_forward and (not self.is_move_backward):
            self.move_forward()
        if self.is_move_backward and (not self.is_move_forward):
            self.move_backward()
        if self.is_turn_right and (not self.is_turn_left):
            self.turn_right();
        if self.is_turn_left and (not self.is_turn_right):
            self.turn_left()

        if self.is_shoot:
            self.shoot()
        
        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y
        self.direction = self.direction + self.turn_speed

        self.speed_x = self.speed_x * self.speed_friction
        self.speed_y = self.speed_y * self.speed_friction

        self.turn_speed = self.turn_speed * self.turn_friction

        orig_rect = self.orig_image.get_rect()
        rot_image = pygame.transform.rotate(self.orig_image
                                           , -self.direction * 180 / math.pi)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = rot_rect

        self.rect.x = self.x
        self.rect.y = self.y

        self.stop_on_walls()

    def stop_on_walls(self):
        if self.x < 0:
            self.x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width
        if self.y < 0:
            self.y = 0
        if self.y > screen_height - self.height:
            self.y = screen_height - self.height
    
    def turn_right(self):
        self.turn_speed = self.turn_speed - self.turn_acceleration

    def turn_left(self):
        self.turn_speed = self.turn_speed + self.turn_acceleration


    def move_forward(self):
        direction = self.direction - (math.pi / 2)
        self.speed_x = (self.speed_x 
                       + (self.movement_acceleration * math.cos(direction)))
        self.speed_y = (self.speed_y 
                       + (self.movement_acceleration
                          * math.cos(direction - (math.pi / 2))))

    def move_backward(self):
        direction = self.direction - (math.pi / 2)
        self.speed_x = (self.speed_x 
                       - (self.movement_acceleration * math.cos(direction)))
        self.speed_y = (self.speed_y 
                       - (self.movement_acceleration
                          * math.cos(direction - (math.pi / 2))))

    def shoot(self):
        b = Bullet(self.rect.center[0],self.rect.center[1],2,2)
        all_sprites.add(b)
        moving_sprites.add(b)


    def set_move_forward(self, b):
        self.is_move_forward = b
    
    def set_move_backward(self, b):
        self.is_move_backward = b

    def set_turn_right(self, b):
        self.is_turn_right = b
    
    def set_turn_left(self, b):
        self.is_turn_left = b

    def set_shoot(self, b):
        self.is_shoot = b


pygame.init()
screen_width = 1500
screen_height = 900

screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('myGame')
background = pygame.Surface(screen.get_size())
background = background.convert();
background.fill((0,0,0))

all_sprites = pygame.sprite.Group()
moving_sprites = pygame.sprite.Group()

player_tex = "triangle.png"
player_sprite = pygame.image.load(player_tex).convert_alpha()

player = Player (screen_width / 2, screen_height / 2, player_sprite)
all_sprites.add(player)
moving_sprites.add(player)

enemy1 = EnemyOne(100,100)
all_sprites.add(enemy1)
moving_sprites.add(enemy1)

bullet = Bullet(0,0,2,2)
all_sprites.add(bullet)
moving_sprites.add(bullet)

clock = pygame.time.Clock()


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #Input handling
        if event.type == pygame.KEYDOWN and event.key == K_w:
            player.set_move_forward(True)
        if event.type == pygame.KEYUP and event.key == K_w:
            player.set_move_forward(False)
        if event.type == pygame.KEYDOWN and event.key == K_s:
            player.set_move_backward(True)
        if event.type == pygame.KEYUP and event.key == K_s:
            player.set_move_backward(False)
        if event.type == pygame.KEYDOWN and event.key == K_a:
            player.set_turn_right(True)
        if event.type == pygame.KEYUP and event.key == K_a:
            player.set_turn_right(False)
        if event.type == pygame.KEYDOWN and event.key == K_d:
            player.set_turn_left(True)
        if event.type == pygame.KEYUP and event.key == K_d:
            player.set_turn_left(False)

        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            player.set_shoot(True)
        if event.type == pygame.KEYUP and event.key == K_SPACE:
            player.set_shoot(False)


    moving_sprites.update()


    screen.fill((0,0,0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
