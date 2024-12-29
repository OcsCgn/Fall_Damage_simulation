import pygame
import Player

class Platform:
    def __init__(self, x, y, width, height, color, colision, ressort,objectif):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.colision = colision
        self.ressort = ressort
        self.objectif = objectif

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_player_above(self, player):
        # Vérifie si le joueur est au-dessus de la plateforme (en tombant)
        return (player.rect.bottom >= self.rect.top and
                self.rect.left < player.rect.centerx < self.rect.right and
                player.velocity_y > 0)
    
    def is_player_below(self, player):
        # Vérifie si le joueur est en dessous de la plateforme (en sautant)
        return (player.rect.top <= self.rect.bottom and
                self.rect.left < player.rect.centerx < self.rect.right and
                player.velocity_y < 0)
