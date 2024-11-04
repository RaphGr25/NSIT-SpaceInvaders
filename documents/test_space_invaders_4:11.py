import pygame  # importation de la librairie pygame
import space
import sys  # pour fermer correctement l'application
import time

# Initialisation de Pygame et de l'écran
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
fond = pygame.image.load('background.png')

# Chargement de la police Lobster
font_path = "Lobster-Regular.ttf"  # Assurez-vous que ce fichier est dans le même dossier que votre script
font = pygame.font.Font(font_path, 28)  # Taille de police réduite
font_large = pygame.font.Font(font_path, 64)  # Pour le message Game Over et de niveau

# Variables de niveau, durée avant game over et timer pour le dernier tir réussi
niveau = 1
game_over_duration = 10  # Durée avant Game Over au niveau 1
last_hit_time = time.time()
show_level_up_message = False  # Variable pour contrôler l'affichage du message de niveau
level_up_message_displayed_time = 0  # Temps écoulé depuis l'affichage du message de niveau
level_up_wait_time = 3  # Temps d'attente avant de passer au niveau suivant
level_up_waiting = False  # Variable pour indiquer si on attend avant de passer au niveau suivant

def reset_game():
    """Réinitialise les variables et crée de nouveaux ennemis avec une vitesse accrue en fonction du niveau."""
    global player, tir, listeEnnemis, victoire, last_hit_time, game_over_duration, niveau, show_level_up_message, level_up_message_displayed_time, level_up_waiting
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

reset_game()
running = True
paused = False

def game_over():
    """Affiche 'Game Over' et réinitialise le jeu et le niveau."""
    message_game_over = font_large.render('Game Over', True, (255, 0, 0))
    message_width = message_game_over.get_width()
    screen.blit(message_game_over, ((800 - message_width) // 2, 250))  # Centrer horizontalement
    pygame.display.update()
    pygame.time.wait(3000)
    global niveau
    niveau = 1  # Réinitialise le niveau au Game Over
    reset_game()

while running:
    screen.blit(fond, (0, 0))

    # Vérifie si le Game Over est déclenché (si aucun ennemi n'est touché dans le délai défini)
    elapsed_time = time.time() - last_hit_time
    if elapsed_time > game_over_duration:
        game_over()
        continue

    # Gestion des événements de jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    # Gestions des collisions et mise à jour des ennemis
    if not paused:
        tous_tues = True  # Vérifie si tous les ennemis sont éliminés
        for ennemi in listeEnnemis:
            if tir.toucher(ennemi):
                ennemi.disparaitre()
                player.marquer()
                player.kills += 1
                last_hit_time = time.time()  # Reset du timer car un ennemi a été touché
            elif ennemi.hauteur > 600:  # Si un ennemi dépasse la limite de l'écran, il réapparaît en haut
                ennemi.disparaitre()
                tous_tues = False  # Il reste des ennemis non touchés
            else:
                tous_tues = False  # Il reste des ennemis en jeu
            ennemi.avancer()
            screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur])

        # Vérification de la victoire pour passer au niveau suivant
        if player.score >= 15 + (niveau - 1) * 5:  # Passer au niveau suivant à chaque 5 points de plus
            niveau += 1  # Augmenter le niveau
            show_level_up_message = True  # Activer le message de niveau
            level_up_message_displayed_time = time.time()  # Démarrer le timer pour le message
            reset_game()  # Recharger les ennemis avec la nouvelle vitesse
        elif tous_tues:
            niveau += 1  # Augmenter le niveau
            reset_game()  # Recharger les ennemis avec la nouvelle vitesse

        # Affiche le vaisseau du joueur
        player.deplacer()
        screen.blit(player.image, [player.position, 500])

        # Affiche la balle (tir) si elle est active
        tir.bouger()
        screen.blit(tir.image, [tir.depart, tir.hauteur])

    # Affiche le score et le niveau actuel
    text_score = font.render(f'Score: {player.score}', True, (255, 255, 255))
    
    # Calcul du temps restant avant Game Over et affichage en haut à droite
    time_remaining = max(0, int(game_over_duration - elapsed_time))
    text_timer = font.render(f'Timer: {time_remaining}s', True, (255, 255, 255))
    
    # Affichage des textes
    screen.blit(text_score, (5, 5))        # Score en haut à gauche
    screen.blit(text_timer, (680, 5))      # Timer affiché en haut à droite
    text_level = font.render(f'Niveau: {niveau}', True, (255, 255, 255))  # Afficher le niveau
    screen.blit(text_level, (680, 40))     # Niveau affiché juste en dessous du timer

    # Affiche le message de niveau si actif
    if show_level_up_message:
        level_up_message = font_large.render(f'Niveau {niveau}!', True, (0, 255, 0))  # Message de niveau
        message_width = level_up_message.get_width()
        screen.blit(level_up_message, ((800 - message_width) // 2, 250))  # Centrer horizontalement

    # Affiche le message "Pause" si le jeu est en pause
    if paused:
        pause_message = font_large.render('PAUSE', True, (255, 255, 0))
        message_width = pause_message.get_width()
        screen.blit(pause_message, ((800 - message_width) // 2, 250))  # Centrer horizontalement

    pygame.display.update()
    clock.tick(65)

pygame.quit()
