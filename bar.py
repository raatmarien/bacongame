import pygame

class Bar():
    def __init__(self, x, y, width, height
                , part_filled, color
                , filled_opacity, background_opacity):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.color = color
        self.background_opacity = background_opacity
        self.filled_opacity = filled_opacity

        self.background_bar = pygame.sprite.Sprite()
        self.background_bar.image = pygame.Surface([width, height])
        self.background_bar.image.fill(color)
        self.background_bar.image.set_alpha(background_opacity)
        self.background_bar.rect = self.background_bar.image.get_rect()
        self.background_bar.rect.x = x
        self.background_bar.rect.y = y
        
        self.filled_bar = pygame.sprite.Sprite()
        filled_bar_width =  width * part_filled
        self.filled_bar.image = pygame.Surface([filled_bar_width, height])
        self.filled_bar.image.fill(color)
        self.filled_bar.image.set_alpha(filled_opacity)
        self.filled_bar.rect = self.filled_bar.image.get_rect()
        self.filled_bar.rect.x = x
        self.filled_bar.rect.y = y

        self.bar_group = pygame.sprite.Group()
        self.bar_group.add(self.background_bar,self.filled_bar)

    def update(self, part_filled):
        if part_filled <= 0.01:
            self.filled_bar.image.set_alpha(0)
        else:
            self.filled_bar.image = pygame.Surface([ part_filled * self.width
                                                   , self.height])
            self.filled_bar.image.fill(self.color)
            self.filled_bar.image.set_alpha(self.filled_opacity)
            self.filled_bar.rect = self.filled_bar.image.get_rect()
            self.filled_bar.rect.x = self.x
            self.filled_bar.rect.y = self.y

    def draw(self, screen):
        self.bar_group.draw(screen)
