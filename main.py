import pygame
import os
from Config import Config as cg
from player import player
from Ball import Ball


pygame.init()
screen = pygame.display.set_mode(cg.TELA)
clock = pygame.time.Clock()
running = True

ball = Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO)
player1 = player(cg.JOGADOR_TAMANHO, cg.JOGADOR1_POS, cg.TELA)
player2 = player(cg.JOGADOR_TAMANHO, cg.JOGADOR2_POS, cg.TELA)

players = [player1, player2]

# sounds 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hit_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "hit_1.wav"))
point_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "point_1.wav"))
font = pygame.font.SysFont('consolas', 30)


def scored(ball):
    if ball.position.x > cg.LARGURA:
        player2.score+=1
        return True

    elif ball.position.x < 0:
        player1.score+=1
        return True
    
    print(ball)

def colidir(ball, p):
    # verifica colisao da bola com player
    
    if not ball.form.colliderect(p.form):
        return

    sobre_x = min(ball.form.right, p.form.right) - max(ball.form.left, p.form.left)
    sobre_y = min(ball.form.bottom, p.form.bottom) - max(ball.form.top, p.form.top)

    if sobre_x < sobre_y:
        # batida na lateral da raquete
        hit_sound.play()
        
        if ball.form.centerx < p.form.centerx:
            ball.position.x = p.form.left - ball.radius
            ball.speed[0] = -abs(ball.speed[0])
        else:
            ball.position.x = p.form.right
            ball.speed[0] = abs(ball.speed[0])
    else:
        # batida em cima ou embaixo da raquete
        hit_sound.play()
        
        if ball.form.centery < p.form.centery:
            ball.position.y = p.form.top - ball.radius
            ball.speed[1] = -abs(ball.speed[1])
        else:
            ball.position.y = p.form.bottom
            ball.speed[1] = abs(ball.speed[1])

while running:
    dt = clock.tick(cg.FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(cg.COR_FUNDO)
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect((cg.LARGURA // 2), 0, 5, cg.ALTURA))

    ball.update(screen)

    for p in players:  
        p.update(dt, screen)
        colidir(ball, p)
        
    if scored(ball):
        point_sound.play()
        ball = Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO)

    pygame.draw.line(screen, (255,255,255), (0, 50), (1280, 50), 4)
    screen.blit(pygame.font.SysFont('consolas', 30).render(f'{player1.score}', True, (255,255,255), None), [(cg.LARGURA//2)+30, 15])
    screen.blit(pygame.font.SysFont('consolas', 30).render(f'{player2.score}', True, (255,255,255), None), [(cg.LARGURA//2)-40, 15])

    pygame.display.flip()

pygame.quit()