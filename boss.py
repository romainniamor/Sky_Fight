import pygame
from laser import Laser
from random import randint
from explose import Explose


class Boss(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.image.load("assets/vehicule/fighter.png")
        self.image = pygame.transform.scale(self.image, (200, 200))

        self.rect = self.image.get_rect()
        self.rect.x = randint(10, 900)
        self.rect.y = 0

        self.velocity = 1

        self.attack = 25

        self.health = 1000
        self.max_health = 1000

        self.laser = Laser(self)
        self.all_lasers = pygame.sprite.Group()

        self.game = game

        self.objective_x = randint(0, (1080 - self.rect.width))
        self.objective_y = - randint(0, 350)

    def random_move(self):
        if self.rect.x < self.objective_x:
            self.rect.x += self.velocity
        elif self.rect.x > self.objective_x:
            self.rect.x -= self.velocity
        if abs(self.rect.x - self.objective_x) < self.velocity:
            self.objective_x = randint(0, (1080 - self.rect.width))
        if self.rect.y < self.objective_y:
             self.rect.y += self.velocity
        elif self.rect.y > self.objective_y:
            self.rect.y -= self.velocity
        if abs(self.rect.y - self.objective_y) < self.velocity:
            self.objective_y = - randint(0, 350)

        self.launch_laser()

    def launch_laser(self):
        self.all_lasers.add(Laser(self))

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (165, 165, 165), [self.rect.x + 5, self.rect.y - 4, self.max_health / 2, 2])
        pygame.draw.rect(surface, (0, 0, 0), [self.rect.x + 5, self.rect.y - 4, self.health / 2, 2])

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.score += 1000
            self.game.all_exploses.add(Explose(self.rect.x, self.rect.y))
