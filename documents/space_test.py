import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

# lancement des modules inclus dans pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600)) # création d'une fenêtre de 800 par 600
pygame.display.set_caption("Space Invaders")
fond = pygame.image.load('background.png') # chargement de l'image de fond

def reset_game():
    global player, tir, listeEnnemis, victoire
    player = space.Joueur()
    tir = space.Balle(player)
    tir.etat = "chargee"
    listeEnnemis = [space.Ennemi() for _ in range(space.Ennemi.NbEnnemis)]
    victoire = False  # Réinitialiser la victoire

player = space.Joueur() # creation du joueur
tir = space.Balle(player) # creation de la balle
tir.etat = "chargee"
listeEnnemis = []
for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)

### BOUCLE DE JEU  ###
reset_game()
running = True # variable pour laisser la fenêtre ouverte
paused = False  # Variable pour gérer l'état de pause
victoire = False # Initialisation de la variable de victoire

while running: # boucle infinie pour laisser la fenêtre ouverte
    screen.blit(fond, (0, 0)) # dessin du fond
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT: # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement
        
        # gestion du clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.sens = "gauche"
            if event.key == pygame.K_RIGHT:
                player.sens = "droite"
            if event.key == pygame.K_SPACE:
                player.tirer()
                tir.etat = "tiree"
            if event.key == pygame.K_k:  # Touche pour mettre en pause
                paused = not paused  # Alterne l'état de pause


    ### Actualisation de la scene ###
    # Gestions des collisions
    if not paused:  # Vérifie si le jeu n'est pas en pause
        for ennemi in listeEnnemis:
            if tir.toucher(ennemi):
                ennemi.disparaitre()
                player.marquer()
                player.kills += 1
        
        # Vérification de la victoire par rapport au score
        if player.score >= 6: # Condition de victoire
            victoire = True
        
        print(f"Score = {player.score} points")
        player.deplacer()
        screen.blit(tir.image, [tir.depart, tir.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur
        tir.bouger()
        screen.blit(player.image, [player.position, 500]) # appel de la fonction qui dessine le vaisseau du joueur
        
        for ennemi in listeEnnemis:
            ennemi.avancer()
            screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur
        
        font_path = "Lobster-Regular.ttf" #importation de la police d'écriture
        font = pygame.font.Font(font_path, 36) # Police par défaut de taille 36
        font_victoire = pygame.font.Font(None, 74) #le chiffre 74 représente la taille de la police de caractères en pixels
        text_kills = font.render(f'Kills: {player.kills}', True, (255, 255, 255)) # Texte en blanc
        screen.blit(text_kills, (10, 10)) # Affiche le compteur en haut à gauche
        if victoire:
            message_victoire = font_victoire.render('Passage au niveau suivant', True, (255, 255, 255))
            screen.blit(message_victoire, (70, 250)) # Afficher le message de victoire
            # Attendre 10 secondes
            pygame.display.update()  # Mettre à jour l'affichage avant d'attendre
            pygame.time.wait(5000)  # Attendre 5 000 millisecondes (5 secondes)
            
            reset_game()  # Réinitialiser le jeu
            
    else:
        # Affiche un message de pause

        pause_message = font.render('Pause', True, (255, 255, 255))
        screen.blit(pause_message, (350, 250))
    
    pygame.display.update()
    clock.tick(65)
