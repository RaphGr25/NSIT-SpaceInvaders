import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

# lancement des modules inclus dans pygame
pygame.init() 
clock = pygame.time.Clock()
# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders") 
# chargement de l'image de fond
fond = pygame.image.load('background.png')

# creation du joueur
player = space.Joueur()
# creation de la balle
tir = space.Balle(player)
tir.etat = "chargee"
# creation des ennemis
listeEnnemis = []
for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)
    
### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte
victoire = False  # Initialisation de la variable de victoire

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement
       
       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.sens = "gauche" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.sens = "droite" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_SPACE : # espace pour tirer
                player.tirer()
                tir.etat = "tiree"

    ### Actualisation de la scene ###
    # Gestions des collisions
    for ennemi in listeEnnemis:
        if tir.toucher(ennemi):
            ennemi.disparaitre()
            player.marquer()
            player.kills += 1
    
    # Vérification de la victoire par rapport au score
    if player.score >= 6:  # Condition de victoire
        victoire = True
    
    print(f"Score = {player.score} points")
    # placement des objets
    # le joueur
    player.deplacer()
    screen.blit(tir.image,[tir.depart,tir.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur        
    # la balle
    tir.bouger()
    screen.blit(player.image,[player.position,500]) # appel de la fonction qui dessine le vaisseau du joueur
    # les ennemis
    for ennemi in listeEnnemis:
        ennemi.avancer()
        screen.blit(ennemi.image,[ennemi.depart, ennemi.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur
    
    
    font_path = "Lobster-Regular.ttf"
    font = pygame.font.Font(font_path, 36)  # Police par défaut de taille 36
    font_victoire = pygame.font.Font(None, 74) #le chiffre 74 représente la taille de la police de caractères en pixels
    text_kills = font.render(f'Kills: {player.kills}', True, (255, 255, 255))  # Texte en blanc
    screen.blit(text_kills, (10, 10))  # Affiche le compteur en haut à gauche
    
    if victoire:
        message_victoire = font_victoire.render('Vous avez gagné !', True, (255, 255, 255))
        screen.blit(message_victoire, (200, 250)) # Afficher le message de victoire
        running = False
    
    pygame.display.update() # pour ajouter tout changement à l'écran
    clock.tick(65)
    
    
    """if victoire:
            message_victoire = font_victoire.render('Vous avez gagné !', True, (255, 255, 255))
            screen.blit(message_victoire, (200, 250)) # Afficher le message de victoire
            listeEnnemis.clear()  # Supprime tous les ennemis de la liste
            running = True # rester dans la boule de jeu
            """wait 10sec and reload the game""" """