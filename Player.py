import pygame
import Platform

class Player:
    def __init__(self, x, y, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color
        self.velocity_y = 0 
        self.gravity = 0.5
        self.rebont = 0
        self.on_ground = True  # Nouveau booléen pour indiquer si le joueur est au sol
        self.rect = pygame.Rect(self.pos.x - radius, self.pos.y - radius, radius * 2, radius * 2)

    def update(self, dt, floor, platforms, screen):
        # Mise à jour de la position et des collisions
        keys = pygame.key.get_pressed()

        # Déplacement horizontal
        if keys[pygame.K_q] and self.rect.left > 0:
            self.pos.x -= 300 * dt
        if keys[pygame.K_d] and self.rect.right < screen.get_width():
            self.pos.x += 300 * dt
        if keys[pygame.K_r]:
            self.pos.x = self.radius
            self.velocity_y = 0
            self.on_ground = True

        # Saut
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -14
            self.on_ground = False

        # Mise à jour de la position verticale
        self.velocity_y += self.gravity
        self.pos.y += self.velocity_y
        self.on_ground = False
        self.rebont = self.velocity_y

        # Gestion des collisions avec le sol
        if self.pos.y >= floor:
            self.pos.y = floor
            self.velocity_y = 0
            self.on_ground = True
            self.rebont = 0

        # Gestion des collisions avec les plateformes
        for platform in platforms:
            if platform.colision:
                # Vérification des collisions verticales
                if self.rect.colliderect(platform.rect):
                    if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10 and not platform.ressort and not platform.objectif:
                        # Collision en tombant
                        self.pos.y = platform.rect.top - self.radius
                        self.velocity_y = 0
                        self.on_ground = True
                    elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 10:
                        # Collision en sautant
                        self.pos.y = platform.rect.bottom + self.radius
                        self.velocity_y = 0

                # Collision côté gauche de la plateforme
                if self.rect.right > platform.rect.left - 10 and self.rect.left < platform.rect.left:
                    if not (self.rect.bottom <= platform.rect.top + 5 or self.rect.top >= platform.rect.bottom - 5):
                        self.pos.x = platform.rect.left - self.radius
                # Collision côté droit de la plateforme
                elif self.rect.left < platform.rect.right + 10 and self.rect.right > platform.rect.right:
                    if not (self.rect.bottom <= platform.rect.top + 5 or self.rect.top >= platform.rect.bottom - 5):
                        self.pos.x = platform.rect.right + self.radius

            if platform.ressort:
                if platform.is_player_above(self):
                    # Rebondir sur la plateforme ressort
                    self.velocity_y = -20 - 0.2 * self.rebont
                    self.on_ground = False
                    # Ne pas laisser le joueur "coller" à la plateforme ressort
                    self.pos.y = platform.rect.top - self.radius  # Juste au-dessus de la plateforme ressort

        # Mise à jour du rectangle de collision
        self.rect.topleft = (self.pos.x - self.radius, self.pos.y - self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.rect(screen, "white", self.rect, 2)
