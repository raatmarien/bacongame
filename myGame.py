from __future__ import division
import os, sys
import pygame
import math
from pygame.locals import *
import random
import bar
import bullet

Bullet = bullet.Bullet

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

    hit_score = 50


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
            color_list[0] = int(color_list[0] + ((255 - orig_color_list[0])
                                                  / self.tot_lifes * damage))
            if color_list[0] > 255:
                color_list[0] = 255
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

        Enemy.__init__(self, x, y, speed_x, speed_y,5)

        self.image = pygame.Surface([self.width, self.height])
        self.orig_color = (0,255,68)
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
        self.orig_color = (0,147,255)
        self.color = self.orig_color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.shoot_interval = random.randrange(200,300)

        self.hit_score = enemy_two_score

    def update(self):
        Enemy.update(self)
        if self.frames_since_shot > self.shoot_interval:
            self.shoot()
            self.frames_since_shot = 0
            self.shoot_interval = random.randrange(200,300)
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
                       , self.bullet_color, 4, 4)
        enemy_bullet_sprites.add(bullet)
        moving_sprites.add(bullet)


        

class EnemyThree(EnemyOne):
    bursted = False

    def __init__(self, x, y, width, height, bursted, speed_x, speed_y):
        self.hit_score = enemy_three_score
        self.bursted = bursted
        if not self.bursted:
            EnemyOne.__init__(self)
        else:
            self.image = pygame.Surface([width, height])
            self.rect = self.image.get_rect()
            Enemy.__init__(self, x, y, width, height, 1)
            self.speed_x = speed_x
            self.speed_y = speed_y

        self.orig_color = (255,255,0)
        self.color = self.orig_color

            
    def hit(self, damage):
        Enemy.hit(self, damage)
        if not self.bursted:
            if self.lifes <= 2:
                e1 = EnemyThree(self.x - 10,  self.y - 10, 10, 10, True, -5, -5)
                all_sprites.add(e1)
                moving_sprites.add(e1)
                e2 = EnemyThree(self.x + 10,  self.y - 10, 10, 10, True, +5, -5)
                all_sprites.add(e2)
                moving_sprites.add(e2)
                e3 = EnemyThree(self.x - 10,  self.y + 10, 10, 10, True, -5, +5)
                all_sprites.add(e3)
                moving_sprites.add(e3)
                e4 = EnemyThree(self.x + 10,  self.y + 10, 10, 10, True, +5, +5)
                all_sprites.add(e4)
                moving_sprites.add(e4)
                self.kill()


class PowerUp(EnemyOne):
    def __init__(self):
        EnemyOne.__init__(self)
        self.speed_x = 0
        self.speed_y = 0
        self.lifes = 1
        self.tot_lifes = 1
        self.hit_score = 0
        self.width = 30
        self.height = 30

    def update(self):
        self.speed_x = 0
        self.speed_y = 0


class BulletPowerUp(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.image = pygame.image.load("pu_max_bullets.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def hit(self):
        player.bullets_per_frame = player.bullets_per_frame + 0.35
        player.max_bullets = player.max_bullets + 8
        self.kill()

class HealthPowerUp(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.image = pygame.image.load("pu_health.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def hit(self):
        player.lifes = player.lifes + 25
        if player.lifes > player.orig_lifes:
            player.lifes = player.orig_lifes
        self.kill()

class ShieldPowerUp(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.image = pygame.image.load("pu_shield.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def hit(self):
        if not player.shield:
            player.shield = True
            shield_obj = Shield()
            all_sprites.add(shield_obj)
            moving_sprites.add(shield_obj)
            shield_group.add(shield_obj)
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pu_shield_36.png")
        self.rect = self.image.get_rect()
        self.rect.x = player.x
        self.rect.y = player.y

    def update(self):
        self.rect.x = player.x
        self.rect.y = player.y

    def hit(self):
        player.shield = False
        self.kill()


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

    max_bullets = 30
    bullets_per_frame = 2
    bullets_left = max_bullets
    bullet_color = (255,255,128)

    orig_lifes = 100
    lifes = orig_lifes

    shield = False

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
            for i in range(0,int(math.floor(self.bullets_per_frame))):
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
            direction = direction + r_dir - 0.10 # <- to middle it out

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
                      , speed_x, speed_y, life_length, self.bullet_color, 2, 2)
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
        if not self.shield:
            self.lifes = self.lifes - damage
            if self.lifes <= 0:
                game_over()
            global score_multiplier
            score_multiplier = 1

            global hit_flash_opacity
            hit_flash_opacity = 120
        else:
            shield = False


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
           player.hit(3)
           for shield in shield_group:
               if collides( bullet.x, bullet.y, bullet.width, bullet.height
                          , shield.rect.x, shield.rect.y, player_width
                          , player_height):
                   shield.hit()
    enemy_list = enemy_sprites.sprites()
    for enemy in enemy_list:
        if collides( enemy.x, enemy.y, enemy.width, enemy.height
                   , player_x, player_y, player_width, player_height ):
            enemy.kill()
            player.hit(10)
            for shield in shield_group:
               if collides( enemy.x, enemy.y, enemy.width, enemy.height
                          , shield.rect.x, shield.rect.y, player_width
                          , player_height):
                   shield.hit()

    pup_list = pup_sprites.sprites()
    for pup in pup_list:
        if collides( pup.rect.x, pup.rect.y, pup.width, pup.height
                   , player_x, player_y, player_width, player_width):
            pup.hit()

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
    retry_screen()

def spawn_enemy_one():
    e = EnemyOne()
    all_sprites.add(e)
    moving_sprites.add(e)

def spawn_enemy_two():
    e = EnemyTwo()
    all_sprites.add(e)
    moving_sprites.add(e)

def spawn_enemy_three():
    e_3 = EnemyThree(0,0,0,0,False,0,0)
    all_sprites.add(e_3)
    moving_sprites.add(e_3)

def spawn_max_bullets_pu():
    pu = BulletPowerUp()
    all_sprites.add(pu)
    moving_sprites.add(pu)
    pup_sprites.add(pu) 

def spawn_health_pu():
    pu = HealthPowerUp()
    all_sprites.add(pu)
    moving_sprites.add(pu)
    pup_sprites.add(pu)

def spawn_shield_pu():
    pu = ShieldPowerUp()
    all_sprites.add(pu)
    moving_sprites.add(pu)
    pup_sprites.add(pu)


def draw_score():
    #change highscore color if same as current score
    if highscore == score:
        highscore_color = (255,255,128)
    else:
        highscore_color = (150,150,150)
    score_text = score_font.render(str(score),1,(245,245,245))
    multiplier_text = multiplier_font.render( "x" + str(score_multiplier)
                                            , 1 , (150,150,150))
    highscore_text = multiplier_font.render( "Highscore: " + str(highscore)
                                      , 1, highscore_color)
    screen.blit(score_text,(750 - score_text.get_width() / 2,850))
    screen.blit(multiplier_text,
               ((746 - multiplier_text.get_width() / 2, 820)))
    screen.blit(highscore_text,( 1490 - highscore_text.get_width()
                               , 860))

def retry_screen():
    ldone = False
    global done

    # Save highscore
    highscore_file = open(".highscore", 'w')
    highscore_file.write(str(highscore))
    
    end_transparancy = 230
    transparancy_now = 0

    orig_color = 120
    color = orig_color

    fade = pygame.sprite.Sprite()
    fade.image = pygame.Surface([screen_width,screen_height])
    fade.image.set_alpha(transparancy_now)
    fade.rect = fade.image.get_rect()
    fade_g = pygame.sprite.Group()
    fade_g.add(fade)
    while not ldone:
        fade.image.set_alpha(transparancy_now)
        if transparancy_now < end_transparancy:
            transparancy_now = transparancy_now + 12

        if color <= orig_color:
            up = True
        if color >= 255:
            up = False
        if up:
            color = color + 10
        else:
            color = color - 10
        if color > 255:
            color = 255

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ldone = True
                done = True
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                ldone = True
                done = True
    
        fade_g.update()
        health_bar.update(0)

        screen.fill((0,0,0))
        player_bullet_sprites.draw(screen)
        enemy_bullet_sprites.draw(screen)
        all_sprites.draw(screen)
        health_bar.draw(screen)
        bullets_bar.draw(screen)

        fade_g.draw(screen)
        draw_retry_score((color,color,color))

        pygame.display.flip()

        clock.tick(60)

def controls_screen():
    controls_information = pygame.sprite.Sprite()
    controls_information.image = pygame.image.load("controls.png").convert_alpha()
    controls_information.rect = controls_information.image.get_rect()
    controls_group = pygame.sprite.Group()
    controls_group.add(controls_information)

    orig_color = 150
    color = orig_color
    play = False
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                play = True
            if event.type == pygame.QUIT:
                sys.exit()

        health_bar.update(1)
        bullets_bar.update(1)
    
        screen.fill((0,0,0))
        controls_group.draw(screen)
    
        health_bar.draw(screen)
        bullets_bar.draw(screen)

        if color <= orig_color:
            up = True
        if color >= 255:
            up = False
        if up:
            color = color + 5
        else:
            color = color - 5

        press_space_text = score_font.render("Press space to play..."
                           , 1, (color,color,color))
        screen.blit(press_space_text, ( 750 - press_space_text.get_width() / 2
                                      , 700))

        pygame.display.flip()
        clock.tick(60)



def draw_retry_score(color):
    score_text = score_font.render( "You scored: " + str(score)
                                  , 1, (255,255,255))
    press_space_text = multiplier_font.render("Press space to continue..."
                       , 1, color)
    screen.blit(score_text, ( 750 - score_text.get_width() / 2
                            , 450 - score_text.get_height() / 2))
    screen.blit(press_space_text, (750 - press_space_text.get_width() / 2
                                  , 480))
    if score == highscore:
        highscore_text = score_font.render("You scored a new highscore!", 1
                                          , (255, 255, 255))
        screen.blit(highscore_text, (750 - highscore_text.get_width() / 2
                                  , 375 - highscore_text.get_height() / 2))


def pause():
    space = False
    while not space:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_SPACE:
                space = True


while True:
    pygame.init()
    screen_width = 1500
    screen_height = 900
    
    score = 0
    score_multiplier = 1
    score_font = pygame.font.Font("Munro.ttf", 48)
    multiplier_font = pygame.font.Font("Munro.ttf", 24)

    # Get the highscore
    highscore_fname = ".highscore"
    if os.path.isfile(highscore_fname):
        highscore_file = open(highscore_fname, 'r')
        highscore = int(highscore_file.read())
        highscore_file.close()
    else:
        highscore = 0
        highscore_file = open(highscore_fname, 'w')
        highscore_file.write("0")
        highscore_file.close()
    
    enemy_one_score = 5
    enemy_two_score = 10
    enemy_three_score = 8
    
    screen = pygame.display.set_mode([screen_width,screen_height])
    pygame.display.set_caption('myGame')
    background = pygame.Surface(screen.get_size())
    background = background.convert();
    background.fill((0,0,0))
    
    all_sprites = pygame.sprite.Group()
    player_bullet_sprites = pygame.sprite.Group()
    enemy_bullet_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    pup_sprites = pygame.sprite.Group() #All Power Ups should also be part of the
                                       #enemy_sprites group for
                                       #collision detection
    moving_sprites = pygame.sprite.Group()
    shield_group = pygame.sprite.Group()
    
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
    frames_till_first_enemy_3 = 1200
    frames_since_start = 0
    spawn_2_started = False
    spawn_3_started = False
    chance_enemy_1 = 0.004
    chance_enemy_2 = 0.002
    chance_enemy_3 = 0.0004
    chance_mb_pu = 0.0
    chance_health_pu = 0.0
    chance_shield_pu = 0.0
    chance_mb_pu_add =     0.00000008
    chance_health_pu_add = 0.00000036
    chance_shield_pu_add = 0.00000020
    chance_multiplier_1 = 0.0000012
    chance_multiplier_2 = 0.0000007
    chance_multiplier_3 = 0.00000008
    
    # GUI
    health_color = (231,27,0)
    health_filled_opacity = 144
    health_background_opacity = 71
    health_bar = bar.Bar( 0,0, 750, 16, player.lifes / player.orig_lifes
                        , health_color, health_filled_opacity
                        , health_background_opacity)
    
    bullets_bar_color = (255,255,28)
    bullets_filled_opacity = 139
    bullets_background_opacity = 62
    bullets_bar = bar.Bar( 750, 0, 750, 16, player.bullets_left / player.max_bullets
                         , bullets_bar_color, bullets_filled_opacity
                         , bullets_background_opacity)

    # Hit flash sprite
    hit_flash = pygame.sprite.Sprite()
    hit_flash.image = pygame.Surface([screen_width,screen_height])
    hit_flash.image.set_alpha(0)
    hit_flash.image.fill((255,100,100))
    hit_flash.rect = hit_flash.image.get_rect()
    hit_flash_opacity = 0

    flash_group = pygame.sprite.Group()
    moving_sprites.add(hit_flash)
    flash_group.add(hit_flash)

    clock = pygame.time.Clock()

    controls_screen()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            #Input handling
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pause()
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
                
            if event.type == pygame.KEYDOWN and event.key == K_p: #Debug
                player.hit(1000)
    
    
        check_collisions()
    
        #spawning logic
        if not spawn_2_started or not spawn_3_started:
            frames_since_start = frames_since_start + 1
            if frames_since_start > frames_till_first_enemy_2:
                spawn_2_started = True
            if frames_since_start> frames_till_first_enemy_3:
                spawn_3_started = True
        if random.random() <= chance_enemy_1:
            spawn_enemy_one()
        if spawn_2_started and random.random() <= chance_enemy_2:
            spawn_enemy_two()
        if spawn_3_started and random.random() <= chance_enemy_3:
            spawn_enemy_three()
        if random.random() <= chance_mb_pu:
            spawn_max_bullets_pu()
            chance_mb_pu = 0.0
        else:
            chance_mb_pu = chance_mb_pu + chance_mb_pu_add
        if random.random() <= chance_health_pu:
            spawn_health_pu()
            chance_health_pu = 0.0
        else:
            chance_health_pu = chance_health_pu + chance_health_pu_add
        if random.random() <= chance_shield_pu:
            spawn_shield_pu()
            chance_shield_pu = 0.0
        else:
            chance_shield_pu = chance_shield_pu + chance_shield_pu_add
    
        chance_enemy_3 = chance_enemy_3 + chance_multiplier_3
        chance_enemy_2 = chance_enemy_2 + chance_multiplier_2
        chance_enemy_1 = chance_enemy_1 + chance_multiplier_1
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

        if score > highscore:
            highscore = score
    
        draw_score()

        if hit_flash_opacity > 0:
            hit_flash_opacity = hit_flash_opacity - 5

        hit_flash.image.set_alpha(hit_flash_opacity)
        flash_group.draw(screen)
    
        pygame.display.flip()
        clock.tick(60)
    
