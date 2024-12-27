import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

radius = 40
velocity_y = 0            # Vitesse verticale initiale
gravity = 0.5             # Gravité (accélération)
floor = screen.get_height() - radius   	  # Limite du sol
rebont = 0                # Compteur de rebond (temps passé dans l'air)

player_pos = pygame.Vector2(radius, floor)

# Fonction pour vérifier si le joueur est au sol
def on_ground():
    return player_pos.y >= floor

# Fonction pour vérifier si le joueur est sur le rectangle bleu
def on_blue_rectangle():
    # Vérifie si le joueur est dans la zone du rectangle bleu
    # et si sa vitesse verticale (velocity_y) est positive (ce qui signifie qu'il descend)
    return (player_pos.y >= 500 - radius and 
            screen.get_width() / 2 < player_pos.x < screen.get_width() / 2 + 200 and
            velocity_y > 0)


# Fonction pour vérifier si le joueur est sur le rectangle vert
def on_green_rectangle():
    return player_pos.y >= floor and screen.get_width() / 5 < player_pos.x < screen.get_width() / 5 + 700 / 3

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec une couleur
    screen.fill("black")

    pygame.draw.circle(screen, "red", player_pos, radius)
    pygame.draw.rect(screen, "blue", (screen.get_width() / 2, 500, 200, 35))
    pygame.draw.rect(screen, "green", (screen.get_width() / 5, floor, 700 / 3, screen.get_height() / 3))

    # Déplacements gauche/droite
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Saut si le joueur est au sol
    if keys[pygame.K_SPACE] and player_pos.y == floor or (keys[pygame.K_SPACE] and player_pos.y >= 600 - radius and screen.get_width() / 2 < player_pos.x < screen.get_width() / 2 + 200):
        velocity_y = -15  # Vitesse initiale pour le saut
        player_pos.y += velocity_y
        rebont = 1  # Démarre le compteur de rebond lorsqu'on saute

    # Appliquer la gravité
    if player_pos.y < floor:
        velocity_y += gravity
        player_pos.y += velocity_y
        rebont += dt  # Augmente rebont pendant que le joueur est en l'air

    # Si le joueur est au sol
    if on_ground():
        player_pos.y = floor
        # Calcul de la puissance du rebond en fonction du temps passé en l'air
        rebond_power = min(rebont * 10, 30)  # Facteur limitant pour éviter des rebonds trop puissants
        velocity_y = -rebond_power  # Applique le rebond
        rebont = 0  # Réinitialiser le compteur de rebond

    # Si le joueur est sur le rectangle bleu
    if on_blue_rectangle():  
        player_pos.y = 500 - radius
        velocity_y = 0
        rebont = 0

    # Si le joueur est sur le rectangle vert, il rebondit comme un ressort
    if on_green_rectangle():
        print(rebont, rebond_power)
        rebond_power = min(rebont * 10, 30)  # Applique la même logique pour le rebond
        velocity_y = -rebond_power  # Applique la puissance du rebond
        player_pos.y = floor  # Assurez-vous que le joueur ne dépasse pas la surface du sol
        player_pos.x += 1000 * dt  # Vous pouvez ajouter un petit déplacement horizontal

    # Afficher
    pygame.display.flip()

    # Limiter les FPS à 60
    dt = clock.tick(60) / 1000

pygame.quit()
