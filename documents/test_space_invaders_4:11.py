import pygame  # importation de la librairie pygame
import space
import sys  # pour fermer correctement l'application
import time

# Initialisation de Pygame et de l'écran
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
fond = pygame.image.load('lune.jpg')

# Chargement de la police Lobster
font_path = "Lobster-Regular.ttf"  # Assurez-vous que ce fichier est dans le même dossier que votre script
font = pygame.font.Font(font_path, 28)  # Taille de police réduite
font_large = pygame.font.Font(font_path, 64)  # Pour les grands messages comme "Game Over"

# Variables globales pour le jeu
niveau = 1
game_over_duration = 10
last_hit_time = time.time()
player = None
tir = None
listeEnnemis = []
show_level_up_message = False
level_up_message_displayed_time = 0
level_up_waiting = False

def reset_game():
    """Réinitialise les variables et crée de nouveaux ennemis avec une vitesse accrue en fonction du niveau."""
    global player, tir, listeEnnemis, last_hit_time, game_over_duration, niveau, show_level_up_message, level_up_message_displayed_time, level_up_waiting
    player = space.Joueur()
    tir = space.Balle(player)
    tir.etat = "chargee"
    
    # Ajuste la liste d'ennemis avec une vitesse augmentée en fonction du niveau
    listeEnnemis = [space.Ennemi() for _ in range(space.Ennemi.NbEnnemis)]
    for ennemi in listeEnnemis:
        ennemi.vitesse += niveau - 1  # Augmente la vitesse des ennemis au fur et à mesure des niveaux
    
    victoire = False
    last_hit_time = time.time()
    game_over_duration = 10 - (niveau - 1)  # Diminuer le temps de Game Over de 1 seconde par niveau
    game_over_duration = max(game_over_duration, 1)  # S'assurer que la durée n'est pas inférieure à 1 seconde
    show_level_up_message = False  # Réinitialiser le message de niveau
    level_up_message_displayed_time = 0  # Réinitialiser le timer du message
    level_up_waiting = False  # Réinitialiser l'attente avant de passer au niveau suivant

def afficher_hud(elapsed_time):
    """Affiche le score, le niveau, et le temps restant avant Game Over."""
    text_score = font.render(f'Score: {player.score}', True, (255, 255, 255))
    time_remaining = max(0, int(game_over_duration - elapsed_time))
    text_timer = font.render(f'Timer: {time_remaining}s', True, (255, 255, 255))
    text_level = font.render(f'Niveau: {niveau}', True, (255, 255, 255))
    
    screen.blit(text_score, (5, 5))        # Score en haut à gauche
    screen.blit(text_timer, (680, 5))      # Timer affiché en haut à droite
    screen.blit(text_level, (680, 40))     # Niveau affiché juste en dessous du timer

def afficher_game_over():
    """Affiche l'écran de Game Over et attend un moment avant de retourner au menu."""
    screen.fill((0, 0, 0))
    game_over_text = font_large.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score Final: {player.score}", True, (255, 255, 255))
    continue_text = font.render("Retour au menu...", True, (255, 255, 255))
    
    screen.blit(game_over_text, ((800 - game_over_text.get_width()) // 2, 200))
    screen.blit(score_text, ((800 - score_text.get_width()) // 2, 300))
    screen.blit(continue_text, ((800 - continue_text.get_width()) // 2, 400))
    pygame.display.update()
    pygame.time.wait(3000)  # Attend 3 secondes avant de retourner au menu

def jeu():
    """Boucle principale du jeu."""
    global niveau, last_hit_time, game_over_duration, player, tir, listeEnnemis

    reset_game()
    running = True
    paused = False

    while running:
        screen.blit(fond, (0, 0))
        elapsed_time = time.time() - last_hit_time

        if elapsed_time > game_over_duration:
            afficher_game_over()
            return "menu"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.sens = "gauche"
                if event.key == pygame.K_RIGHT:
                    player.sens = "droite"
                if event.key == pygame.K_SPACE:
                    player.tirer()
                    tir.etat = "tiree"
                if event.key == pygame.K_k:
                    paused = not paused

        if not paused:
            tous_tues = True
            for ennemi in listeEnnemis:
                if tir.toucher(ennemi):
                    ennemi.disparaitre()
                    player.marquer()
                    last_hit_time = time.time()
                elif ennemi.hauteur > 600:
                    ennemi.disparaitre()
                    tous_tues = False
                else:
                    tous_tues = False
                ennemi.avancer()
                screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur])

            if player.score >= 15 + (niveau - 1) * 5:
                niveau += 1
                reset_game()

            player.deplacer()
            screen.blit(player.image, [player.position, 500])

            tir.bouger()
            screen.blit(tir.image, [tir.depart, tir.hauteur])

        afficher_hud(elapsed_time)

        if paused:
            pause_message = font_large.render('PAUSE', True, (255, 255, 0))
            screen.blit(pause_message, ((800 - pause_message.get_width()) // 2, 250))

        pygame.display.update()
        clock.tick(60)

def menu():
    """Affiche le menu principal."""
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 0))
        title = font_large.render("Space Invaders", True, (255, 255, 255))
        play_button = font.render("Jouer", True, (0, 255, 0))
        quit_button = font.render("Quitter", True, (255, 0, 0))
        instructions = font.render("Contrôles: Flèches pour bouger, Espace pour tirer, K pour Pause", True, (200, 200, 200))
        
        screen.blit(title, ((800 - title.get_width()) // 2, 100))
        screen.blit(play_button, ((800 - play_button.get_width()) // 2, 300))
        screen.blit(quit_button, ((800 - quit_button.get_width()) // 2, 400))
        screen.blit(instructions, ((800 - instructions.get_width()) // 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (300 <= x <= 500) and (300 <= y <= 350):  # Bouton "Jouer"
                    return "jeu"
                if (300 <= x <= 500) and (400 <= y <= 450):  # Bouton "Quitter"
                    pygame.quit()
                    sys.exit()

# Boucle principale
while True:
    result = menu()             #La boucle principale dans ce code sert à gérer le passage entre les différents états du jeu, comme le menu principal ou le jeu lui-même.
    if result == "jeu":
        jeu()

