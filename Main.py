import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Classe pour les plateformes
class Platform:
    def __init__(self, x, y, width, height, color, colision, ressort):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.colision = colision
        self.ressort = ressort

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

# Classe pour le joueur
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

    def update(self, dt, floor, platforms):
        # Mise à jour de la position et des collisions
        keys = pygame.key.get_pressed()

        # Déplacement horizontal
        if keys[pygame.K_q] and self.rect.left > 0:
            self.pos.x -= 300 * dt
        if keys[pygame.K_d]and self.rect.right < screen.get_width():
            self.pos.x += 300 * dt
        if keys[pygame.K_r]:
            self.pos.x = self.radius
            self.velocity_y = 0
            self.on_ground = True

        # Saut
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -20
            self.on_ground = False

        # Mise à jour de la position verticale
        self.velocity_y += self.gravity
        self.pos.y += self.velocity_y
        self.on_ground = False

        # Gestion des collisions avec le sol
        if self.pos.y >= floor:
            self.pos.y = floor
            self.velocity_y = 0
            self.on_ground = True
            self.rebont = 0
            for platform in platforms:
                if self.pos.x > platform.rect.left and self.pos.x < platform.rect.right :
                    self.pos.y = platform.rect.top - self.radius


        # Gestion des collisions avec les plateformes
        for platform in platforms:
            if platform.colision:
                # Vérification des collisions verticales
                if self.rect.colliderect(platform.rect):
                    if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                        # Collision en tombant
                        self.pos.y = platform.rect.top - self.radius
                        self.velocity_y = 0
                        self.on_ground = True
                    elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 10:
                        # Collision en sautant
                        self.pos.y = platform.rect.bottom + self.radius
                        self.velocity_y = 0
                
                if self.rect.right > platform.rect.left - 10 and self.rect.left < platform.rect.left:
                    # Collision côté gauche de la plateforme
                    if not (self.rect.bottom <= platform.rect.top + 5 or self.rect.top >= platform.rect.bottom - 5):
                        self.pos.x = platform.rect.left - self.radius
                elif self.rect.left < platform.rect.right + 10 and self.rect.right > platform.rect.right:
                    # Collision côté droit de la plateforme
                    if not (self.rect.bottom <= platform.rect.top + 5 or self.rect.top >= platform.rect.bottom - 5):
                        self.pos.x = platform.rect.right + self.radius 
                 



        # Mise à jour du rectangle de collision
        self.rect.topleft = (self.pos.x - self.radius, self.pos.y - self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.rect(screen, "white", self.rect, 2) 

# Initialisation des objets
floor = screen.get_height() - 40
player = Player(100, floor, 40, "red")
platforms = [
    Platform(screen.get_width() / 2, 500, 200, 35, "blue", True, False),
    Platform(screen.get_width() / 5, floor, 700 / 3, screen.get_height() / 3, "green", True, True),
]

# Boucle principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran
    screen.fill("black")

    # Mise à jour et affichage du joueur
    player.update(dt, floor, platforms)
    player.draw(screen)

    # Affichage des plateformes
    for platform in platforms:
        platform.draw(screen)

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter les FPS à 60
    dt = clock.tick(60) / 1000

pygame.quit()
