import pygame

screen_width = 1500
screen_height = 900

class Bullet(pygame.sprite.Sprite):
    speed_x = 0.0
    speed_y = 0.0
    width = 2
    height = 2

    transition_period = 25

    def __init__(self, x, y,speed_x, speed_y, life_length, color
            , width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

        self.speed_x = float(speed_x)
        self.speed_y = float(speed_y)

        self.width = width
        self.height = height

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

