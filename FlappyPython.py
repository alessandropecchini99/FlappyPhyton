# Importazione Librerie
import pygame
import random
import sys

# Inizializzazione PyGame
pygame.init()

# Associo le immagini a delle variabili
playBtn = pygame.image.load('images/PLAY.png')
background_img = pygame.image.load('images/background.png')
bird = pygame.image.load('images/bird.png')
base = pygame.image.load('images/base.png')
gameover = pygame.image.load('images/gameover.png')
tube_down = pygame.image.load('images/tube.png')
tube_up = pygame.transform.flip(tube_down, False, True)

# Imposta l'icona della finestra
pygame.display.set_icon(bird)

# Cambia il nome della finestra
pygame.display.set_caption('Flappy_Bird.py')

# Costanti Globali ----------------------------------------------------------
SCREEN = pygame.display.set_mode((288, 512))
FPS = 50
VEL_BASE = 3
SCOREFONT = pygame.font.SysFont('Lato', 50, bold=True)
FONT = pygame.font.SysFont('Lato', 25, bold=True)
TOPSCORE = 0


def initialize():
    global birdx, birdy, bird_vely
    global tubes
    global between_tubes
    global score
    birdx, birdy = 60, 150
    bird_vely = 0
    score = 0
    between_tubes = False
    tubes = []
    tubes.append(tube_class())
    drawObj()
    countdown()


def click_play():
    global basex
    basex = 0
    play = False
    while not play:
        # Disegna lo sfondo
        SCREEN.blit(background_img, (0, 0))
        SCREEN.blit(base, (basex, 400))
        SCREEN.blit(playBtn, ((SCREEN.get_width() // 2 - playBtn.get_width() //
                    2), (SCREEN.get_height() // 2 - playBtn.get_height() // 2) - 20))
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                initialize()
                play = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()


def countdown():
    start_time = pygame.time.get_ticks()
    countdown_duration = 3  # Durata del countdown in secondi

    while True:
        current_time = pygame.time.get_ticks()
        # Tempo trascorso in secondi
        elapsed_time = (current_time - start_time) // 1000

        if elapsed_time >= countdown_duration:
            break  # Esce dal ciclo quando il countdown è completo

        # Calcola il numero rimanente
        remaining_time = countdown_duration - elapsed_time

        # Crea un testo per il countdown
        countdown_text = SCOREFONT.render(
            str(remaining_time), 1, (255, 255, 255))

        # Posiziona il testo al centro dello schermo
        text_x = SCREEN.get_width() // 2 - countdown_text.get_width() // 2
        text_y = SCREEN.get_height() // 2 - countdown_text.get_height() // 2 - 30

        # Disegna lo sfondo
        SCREEN.blit(background_img, (0, 0))
        SCREEN.blit(bird, (birdx, birdy))
        SCREEN.blit(base, (basex, 400))

        # Disegna il testo a schermo
        SCREEN.blit(countdown_text, (text_x, text_y))

        # Aggiorna lo schermo
        pygame.display.flip()

        # Attendi 1 secondo prima di aggiornare il countdown
        pygame.time.delay(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Pulisci solo il testo del countdown
    SCREEN.blit(background_img, (0, 0))
    pygame.display.flip()


def drawObj():
    SCREEN.blit(background_img, (0, 0))
    for tube in tubes:
        tube.go_and_spawn()
    SCREEN.blit(bird, (birdx, birdy))
    SCREEN.blit(base, (basex, 400))
    score_render = SCOREFONT.render(str(score), 1, (255, 255, 255))
    SCREEN.blit(score_render, ((SCREEN.get_width() //
                2 - score_render.get_width() // 2), 10))


def update():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)


def you_lose():
    global TOPSCORE
    SCREEN.blit(
        gameover, ((SCREEN.get_width() // 2 - gameover.get_width() // 2), 180))
    if score > TOPSCORE:
        TOPSCORE = score
    topScore_render = FONT.render(
        "Top Score: " + str(TOPSCORE), 1, (255, 255, 255))
    SCREEN.blit(topScore_render, ((SCREEN.get_width() //
                2 - topScore_render.get_width() // 2), 235))
    update()
    restart = False
    while not restart:
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3)):
                initialize()
                restart = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class tube_class:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)

    def go_and_spawn(self):
        self.x -= VEL_BASE
        SCREEN.blit(tube_down, (self.x, self.y+210))
        SCREEN.blit(tube_up, (self.x, self.y-210))

    def collision(self, bird, birdx, birdy):
        tolerance = 5
        bird_right = birdx + bird.get_width() - tolerance
        bird_left = birdx - tolerance
        tube_right = self.x + tube_down.get_width()
        tube_left = self.x
        bird_up = birdy + tolerance
        bird_bottom = birdy + bird.get_height() - tolerance
        tube_up = self.y + 110
        tube_bottom = self.y + 210
        if bird_right > tube_left and bird_left < tube_right:
            if bird_up < tube_up or bird_bottom > tube_bottom:
                you_lose()

    def between_tubes_method(self, bird, birdx):
        tolerance = 5
        bird_right = birdx + bird.get_width() - tolerance
        bird_left = birdx - tolerance
        tube_right = self.x + tube_down.get_width()
        tube_left = self.x
        if bird_right > tube_left and bird_left < tube_right:
            return True


# Inizio Gioco --------------------------------------------------------------
click_play()

# CICLO GENERALE
while True:
    # Gestione della Base
    basex -= VEL_BASE
    if basex < -45:
        basex = 0

    # Gravità
    bird_vely += 0.85
    birdy += bird_vely

    # Gestione Comandi
    for event in pygame.event.get():
        if ((event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
            bird_vely = -10
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gestione Tubi
    if tubes[-1].x < 130:
        tubes.append(tube_class())

    # Gestione Collisione con i Tubi
    for tube in tubes:
        tube.collision(bird, birdx, birdy)

    # Gestione Punteggio
    if not between_tubes:
        for tube in tubes:
            if tube.between_tubes_method(bird, birdx):
                between_tubes = True
                break
    if between_tubes:
        between_tubes = False
        for tube in tubes:
            if tube.between_tubes_method(bird, birdx):
                between_tubes = True
                break
        if not between_tubes:
            score += 1

    # Gestione della collisione con la Base
    if birdy > 380:
        you_lose()

    # Aggiornamento Schermo
    drawObj()
    update()
