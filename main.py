import pygame
from Config import Config
from player import player
from Ball import Ball

pygame.init()
screen = pygame.display.set_mode(Config.TELA)
clock = pygame.time.Clock()
running = True

ball = Ball(Config.BOLA_POS_INICIAL, Config.TELA, Config.BOLA_TAMANHO)
player1 = player(Config.JOGADOR_TAMANHO, Config.JOGADOR1_POS, Config.TELA)
player2 = player(Config.JOGADOR_TAMANHO, Config.JOGADOR2_POS, Config.TELA)

players = [player1, player2]

while running:
    dt = clock.tick(Config.FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(Config.COR_FUNDO)

    ball.update(screen)          

    for p in players:  
        p.update(dt, screen)

        if ball.form.colliderect(p.form):
            ball.speed[0] *= -1

    pygame.display.flip()

pygame.quit()