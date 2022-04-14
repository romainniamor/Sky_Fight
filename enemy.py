import pygame
from laser import Laser
from random import randint
from explose import Explose

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.image.load("assets/vehicule/vessel.png")
        self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()
        self.rect.x = randint(10, 900)
        self.rect.y = - randint(0, 1000)

        self.velocity = randint(1, 3)

        self.attack = 20

        self.health = 100
        self.max_health = 100

        self.laser = Laser(self)
        self.all_lasers = pygame.sprite.Group()

        self.game = game


    def move(self):
        if self.rect.y < 720:
            self.rect.y += self.velocity
            for player in self.game.collision(self, self.game.all_players):
                self.game.all_exploses.add(Explose(self.rect.x, self.rect.y))
                self.remove()
                self.game.score += 10
                player.damage(self.attack)
            if self.rect.y == randint(0, 175):
                self.launch_laser()
        else:
            self.remove()
            self.game.earth_damage(self.attack)


    def remove(self):
        self.rect.x = randint(10, 900)
        self.rect.y = - randint(1000, 3000)
        self.health = self.max_health

    def launch_laser(self):
        self.all_lasers.add(Laser(self))

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (165, 165, 165), [self.rect.x + 5, self.rect.y - 4, self.max_health / 2, 2])
        pygame.draw.rect(surface, (0, 0, 0), [self.rect.x + 5, self.rect.y - 4, self.health / 2, 2])

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.score += 15
            self.game.all_exploses.add(Explose(self.rect.x, self.rect.y))
            self.remove()
            self.game.spawn_enemy()


