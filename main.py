import pygame
import os
from Config import Config as cg
from player import player
from Ball import Ball
from powers import GeneralPower, PlayerPower
import random



pygame.init()
screen = pygame.display.set_mode(cg.TELA)
clock = pygame.time.Clock()
running = True

ball = Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO)
player1 = player(cg.JOGADOR_TAMANHO, cg.JOGADOR1_POS, cg.TELA)
player2 = player(cg.JOGADOR_TAMANHO, cg.JOGADOR2_POS, cg.TELA, is_player1=False)

players = [player1, player2]
balls_in_game=[ball]
main_ball=balls_in_game[0]
possible_powers=['Fast_ball','Lock_player','Small_ball','Small_player']


# sounds 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hit_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "hit_1.wav"))
point_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "point_1.wav"))
font = pygame.font.SysFont('consolas', 30)

wait_time = 5000  
duration_power = 5000  

inicial_time = pygame.time.get_ticks()
power_time = 0
actual_power=None
power = False

class Power:
    
    @staticmethod
    def select_power(power_type, activate):
        match power_type:
            case 'Fast_ball':
                if activate:
                    GeneralPower.speed_ball(main_ball)
                else:
                    main_ball.speed[0]/=2
                    main_ball.speed[1]/=2
                    main_ball.color=(255,255,255)
            case 'Small_ball':
                if activate:
                    GeneralPower.small_ball(main_ball)
                else:
                    main_ball.radius=cg.BOLA_TAMANHO
            case 'Small_player':
                if activate:
                    PlayerPower.small_player(player1, player2)
                else:
                    PlayerPower.player_with_debuff.height=cg.JOGADOR_TAMANHO
            case 'Lock_player':
                if activate:
                    PlayerPower.lock_player(player1, player2)
                else:
                    PlayerPower.player_with_debuff.free=True
    @staticmethod
    def manage_powers(power_type):
        match power_type:
            case 'Fast_ball':
                main_ball.color=(255,0,0)
            case 'Lock_player':
                pygame.draw.line(screen, (255,0,0), (PlayerPower.player_with_debuff.position.x, cg.ALTURA), (PlayerPower.player_with_debuff.position.x, 0), 2)
               

def scored(ball):
    if ball.position.x > cg.LARGURA:
        player2.score+=1
        return True

    elif ball.position.x < 0:
        player1.score+=1
        return True

def colidir(ball, p):
    # verifica colisao da bola com player
    if not ball.form.colliderect(p.form):
        return
    
    sobre_x = min(ball.form.right, p.form.right) - max(ball.form.left, p.form.left)
    sobre_y = min(ball.form.bottom, p.form.bottom) - max(ball.form.top, p.form.top)

    if sobre_x < sobre_y:
       
        hit_sound.play()
        
        if ball.form.centerx < p.form.centerx:
            ball.position.x = p.form.left - ball.radius
            ball.speed[0] = -abs(ball.speed[0] - p.speed.x * 0.01)
        else:
            ball.position.x = p.form.right
            ball.speed[0] = abs(ball.speed[0] + p.speed.x * 0.01)
    else:
        # batida em cima ou embaixo da barra
        hit_sound.play()
        
        if ball.form.centery < p.form.centery:
            ball.position.y = p.form.top - ball.radius
            ball.speed[1] = -abs(ball.speed[1] - p.speed.y * 0.01)
        else:
            ball.position.y = p.form.bottom
            ball.speed[1] = abs(ball.speed[1] + p.speed.y * 0.01)

while running:
    dt = clock.tick(cg.FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(cg.COR_FUNDO)
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect((cg.LARGURA // 2), 0, 5, cg.ALTURA))

    actual_time = pygame.time.get_ticks()

    if not power:
        if actual_time - inicial_time >= wait_time:
            power=True
            actual_power=random.choice(possible_powers)
            Power.select_power(actual_power, True)
            power_time = actual_time

    else:
        Power.manage_powers(actual_power)
        if actual_time - power_time >= duration_power:
            power=False
            Power.select_power(actual_power, False)
            inicial_time = actual_time

    main_ball.update(screen)

    vel_bola = pygame.Vector2(ball.speed).length() * cg.FPS

    for p in players:  
        p.update(dt, screen)
        colidir(main_ball, p)
        p.speed = vel_bola
    

    if scored(main_ball):
        point_sound.play()
        balls_in_game.pop(0)
        balls_in_game.append(Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO))
        main_ball=balls_in_game[0]
        

    pygame.draw.line(screen, (255,255,255), (0, 50), (1280, 50), 4)
    screen.blit(pygame.font.SysFont('consolas', 30).render(f'{player1.score}', True, (255,255,255), None), [(cg.LARGURA//2)+30, 15])
    screen.blit(pygame.font.SysFont('consolas', 30).render(f'{player2.score}', True, (255,255,255), None), [(cg.LARGURA//2)-40, 15])

    pygame.display.flip()

pygame.quit()