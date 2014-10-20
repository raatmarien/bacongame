from __future__ import division
import os, sys
import pygame
import math
from pygame.locals import *
import random
import bar

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Enemy(pygame.sprite.Sprite):
    width = 20
    height = 20

    x = 0
    y = 0

    speed_x = 0
    speed_y = 0

    tot_appear_time = 60
    appear_time = 0


    def __init__(self, x, y, speed_x, speed_y,tot_lifes):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tot_lifes = tot_lifes
        self.lifes = self.tot_lifes

    def update(self):
        # Update color
        self.image.fill(self.color)

        self.appear_time = self.appear_time + 1
        if self.appear_time < self.tot_appear_time:
            opacity = self.appear_time / self.tot_appear_time * 256
            self.image.set_alpha(opacity)
        else:
            enemy_sprites.add(self)
            self.image.set_alpha(255)
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

    def hit(self, damage):
        self.lifes = self.lifes - damage
        if self.lifes <= 0:
            self.kill()
            global score
            global score_multiplier
            score = score + self.hit_score * score_multiplier
            score_multiplier = score_multiplier + 1
        else:
            color_list = list(self.color)
            orig_color_list = list(self.orig_color)
            # for the rest
            for i in range (1,3):
                color_list[i] = int(color_list[i] - 
                                 (orig_color_list[i] / self.tot_lifes * damage))
                if color_list[i] < 0:
                    color_list[i] = 0
            # for red
            color_list[0] = int(color_list[0] + (255 / self.tot_lifes * damage))
            self.color = tuple(color_list)

class EnemyOne(Enemy):
    def __init__(self):
        x = random.randrange(0,screen_width - self.width)
        y = random.randrange(0,screen_height - self.height)

        speed_x = 1 + random.random() * 2
        speed_y = 1 + random.random() * 2

        if random.randrange(0,2) == 0:
            speed_x = -speed_x
        if random.randrange(0,2) == 0:
            speed_y = -speed_y

        Enemy.__init__(self, x, y, speed_x, speed_y,10)

        self.image = pygame.Surface([self.width, self.height])
        self.orig_color = (0,255,0)
        self.color = self.orig_color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.hit_score = enemy_one_score


class EnemyTwo(Enemy):
    bullet_color = (6,223,255)
    frames_since_shot = 0

    def __init__(self):
        x = random.randrange(0,screen_width - self.width)
        y = random.randrange(0,screen_height - self.height)

        speed_x = random.random() * 2
        speed_y = random.random() * 2

        if random.randrange(0,2) == 0:
            speed_x = -speed_x
        if random.randrange(0,2) == 0:
            speed_y = -speed_y

        Enemy.__init__(self, x, y, speed_x, speed_y,3)
        self.image = pygame.Surface([self.width, self.height])
        self.orig_color = (0,0,255)
        self.color = self.orig_color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.shoot_interval = random.randrange(40,300)

        self.hit_score = enemy_two_score

    def update(self):
        Enemy.update(self)
        if self.frames_since_shot > self.shoot_interval:
            self.shoot()
            self.frames_since_shot = 0
            self.shoot_interval = random.randrange(40,300)
        else:
            self.frames_since_shot = self.frames_since_shot + 1

    def shoot(self):
        r_x = random.random() * 4
        r_y = random.random() * 4

        center_player_x = player.rect.x + player.width / 2
        center_player_y = player.rect.y + player.height / 2
        center_self_x = self.rect.x + self.width / 2
        center_self_y = self.rect.y + self.height / 2

        distance_x = 0.0
        distance_y = 0.0
        distance_x = center_player_x - center_self_x
        distance_y = center_player_y - center_self_y
        distance_diagonal = math.sqrt( distance_x * distance_x 
                                     + distance_y * distance_y)
        max_speed = 8 

        speed_bullet_x = ((max_speed * distance_x) / distance_diagonal
                          + r_x - 2)
        speed_bullet_y = ((max_speed * distance_y) / distance_diagonal
                          + r_y - 2)

        bullet_x = 0
        bullet_y = 0

        if speed_bullet_x >= 0 and speed_bullet_y >= 0:
            bullet_x = self.rect.x + self.width
            bullet_y = self.rect.y + self.height
        elif speed_bullet_x >= 0 and speed_bullet_y <= 0 :
            bullet_x = self.rect.x + self.width
            bullet_y = self.rect.y
        elif speed_bullet_x <= 0 and speed_bullet_y >= 0:
            bullet_x = self.rect.x
            bullet_y = self.rect.y + self.height
        elif speed_bullet_x <= 0 and speed_bullet_y <= 0 :
            bullet_x = self.rect.x
            bullet_y = self.rect.y

        bullet = Bullet(bullet_x, bullet_y, speed_bullet_x, speed_bullet_y, 180
                       , self.bullet_color)
        enemy_bullet_sprites.add(bullet)
        moving_sprites.add(bullet)


class Bullet(pygame.sprite.Sprite):
    speed_x = 0.0
    speed_y = 0.0
    width = 2
    height = 2

    transition_period = 25

    def __init__(self, x, y,speed_x, speed_y, life_length, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

        self.speed_x = float(speed_x)
        self.speed_y = float(speed_y)

        self.life_length = life_length

    def update(self):
        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y

        # bounce on walls
        if self.x < 0:
            self.x = 0
            self.speed_x = abs(self.speed_x)
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width
            self.speed_x = -abs(self.speed_x)
        if self.y < 0:
            self.y = 0
            self.speed_y = abs(self.speed_y)
        if self.y > screen_height - self.height:
            self.y = screen_height - self.height
            self.speed_y = -abs(self.speed_y)

        self.rect.x = self.x
        self.rect.y = self.y

        self.life_length = self.life_length - 1

        if self.life_length <= 0:
            self.kill()
        elif self.life_length <= self.transition_period:
            opacity = self.life_length / self.transition_period * 256
            self.image.set_alpha(opacity)

class Player(pygame.sprite.Sprite):
    width = 36
    height = 36

    speed_x = 0
    speed_y = 0

    speed_friction = 0.95
    movement_acceleration = 0.3

    direction = 0
    turn_speed = 0
    turn_friction = 0.60
    turn_acceleration = 0.05

    is_move_forward = False
    is_move_backward = False

    is_turn_right = False
    is_turn_left = False

    is_shoot = False

    max_bullets = 56
    bullets_left = max_bullets
    bullet_color = (255,229,6)

    orig_lifes = 100
    lifes = orig_lifes

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
            self.shoot()

        self.bullets_left = self.max_bullets - len(player_bullet_sprites)

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
        if len(player_bullet_sprites) <= self.max_bullets:
            # Randomize all the things!!!
            r_dir = random.random() / 5
            r_speed = random.random() * 5
            r_life_length = random.randrange(0,20)

            # Normalize the direction
            direction = (math.pi * 2) - self.direction
            direction = direction + math.pi
            direction = direction % (math.pi * 2)
            direction = direction + r_dir - 0.05 # <- to middle it out

            tot = 10 + r_speed

            life_length = 70 + r_life_length

            if direction < (math.pi / 2):
                speed_x = tot * math.cos((math.pi / 2) - direction)
                speed_y = tot * math.cos(direction)
            elif direction < math.pi:
                speed_x = tot * math.cos(direction - (math.pi / 2))
                speed_y = -tot * math.cos(math.pi - direction)
            elif direction < (math.pi * 1.5):
                speed_x = -tot * math.cos((math.pi * 1.5) - direction)
                speed_y = -tot * math.cos(direction - math.pi)
            else:
                speed_x = -tot * math.cos(direction - (1.5 * math.pi))
                speed_y = tot * math.cos((2 * math.pi) - direction)

            b = Bullet(self.rect.center[0], self.rect.center[1]
                      , speed_x, speed_y, life_length, self.bullet_color)
            player_bullet_sprites.add(b)
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

    def hit(self, damage):
        self.lifes = self.lifes - damage
        if self.lifes <= 0:
            game_over()
        global score_multiplier
        score_multiplier = 1

def check_collisions():
    check_collisions_player()
    check_collisions_enemys()

def check_collisions_player():
    bullet_list = enemy_bullet_sprites.sprites()
    player_x = player.rect.x
    player_y = player.rect.y
    player_width = player.width
    player_height = player.height
    for bullet in bullet_list:
       if collides( bullet.x, bullet.y, bullet.width, bullet.height
                  , player_x, player_y, player_width, player_height ):
           bullet.kill()
           player.hit(1)
    enemy_list = enemy_sprites.sprites()
    for enemy in enemy_list:
        if collides( enemy.x, enemy.y, enemy.width, enemy.height
                   , player_x, player_y, player_width, player_height ):
            enemy.kill()
            player.hit(3)

def check_collisions_enemys():
    bullet_list = player_bullet_sprites.sprites()
    enemy_list = enemy_sprites.sprites()
    for bullet in bullet_list:
        for enemy in enemy_list:
            if collides( bullet.x, bullet.y, bullet.width, bullet.height
                       , enemy.x, enemy.y, enemy.width, enemy.height):
                bullet.kill()
                enemy.hit(1)


def collides(x1, y1, width1, height1, x2, y2, width2, height2):
    if (x1 + width1 < x2 or x1 > x2 + width2
        or y1 + height1 < y2 or y1 > y2 + height2):
        return False
    else:
        return True

def game_over():
    sys.exit()

def spawn_enemy_one():
    e = EnemyOne()
    all_sprites.add(e)
    moving_sprites.add(e)

def spawn_enemy_two():
    e = EnemyTwo()
    all_sprites.add(e)
    moving_sprites.add(e)

def draw_score():
    score_text = score_font.render(str(score),1,(245,245,245))
    multiplier_text = multiplier_font.render( "x" + str(score_multiplier)
                                            , 1 , (150,150,150))
    screen.blit(score_text,(750 - score_text.get_width() / 2,850))
    screen.blit(multiplier_text,
               ((746 - multiplier_text.get_width() / 2, 820)))
    

pygame.init()
screen_width = 1500
screen_height = 900

score = 0
score_multiplier = 1
score_font = pygame.font.Font("Munro.ttf", 48)
multiplier_font = pygame.font.Font("Munro.ttf", 24)

enemy_one_score = 5
enemy_two_score = 10

screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('myGame')
background = pygame.Surface(screen.get_size())
background = background.convert();
background.fill((0,0,0))

all_sprites = pygame.sprite.Group()
player_bullet_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
moving_sprites = pygame.sprite.Group()

player_tex = "triangle.png"
player_sprite = pygame.image.load(player_tex).convert_alpha()

player = Player (screen_width / 2, screen_height / 2, player_sprite)
all_sprites.add(player)
moving_sprites.add(player)

# 7 enemys in the beginning
for i in range(0,7):
    e = EnemyOne()
    all_sprites.add(e)
    moving_sprites.add(e)

#Spawn variables
frames_till_first_enemy_2 = 600
frames_since_start = 0
spawn_2_started = False
chance_enemy_1 = 0.005
chance_enemy_2 = 0.002
chance_multiplier = 0.000001

# GUI
health_color = (231,27,0)
health_filled_opacity = 144
health_background_opacity = 71
health_bar = bar.Bar( 0,0, 750, 16, player.lifes / player.orig_lifes
                    , health_color, health_filled_opacity
                    , health_background_opacity)

bullets_bar_color = (225,229,6)
bullets_filled_opacity = 139
bullets_background_opacity = 62
bullets_bar = bar.Bar( 750, 0, 750, 16, player.bullets_left / player.max_bullets
                     , bullets_bar_color, bullets_filled_opacity
                     , bullets_background_opacity)


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


    check_collisions()

    #spawning logic
    if not spawn_2_started:
        frames_since_start = frames_since_start + 1
        if frames_since_start > frames_till_first_enemy_2:
            spawn_2_started = True
    if random.random() <= chance_enemy_1:
        spawn_enemy_one()
    if spawn_2_started and random.random() <= chance_enemy_2:
        spawn_enemy_two()

    chance_enemy_2 = chance_enemy_2 + chance_multiplier
    chance_enemy_1 = chance_enemy_1 + chance_multiplier
    moving_sprites.update()

    if player.lifes == 0:
        health_part_filled = 0
    else:
        health_part_filled = player.lifes / player.orig_lifes
    
    if player.bullets_left == 0:
        bullets_part_filled = 0
    else:
        bullets_part_filled = player.bullets_left / player.max_bullets

    health_bar.update(health_part_filled)
    bullets_bar.update(bullets_part_filled)

    screen.fill((0,0,0))
    player_bullet_sprites.draw(screen)
    enemy_bullet_sprites.draw(screen)
    all_sprites.draw(screen)

    health_bar.draw(screen)
    bullets_bar.draw(screen)

    draw_score()

    pygame.display.flip()
    clock.tick(60)
