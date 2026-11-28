import pygame
import os
from Config import Config as cg
from player import player
from Ball import Ball
from powers import GeneralPower, PlayerPower
from game_over import Game_over
from menu import Menu
import random


pygame.init()
screen = pygame.display.set_mode(cg.TELA)
clock = pygame.time.Clock()
running = True

menu = Menu(screen, clock)
max_points = 0

# sounds 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hit_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "hit_1.wav"))
point_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "point_1.wav"))
font = pygame.font.SysFont('consolas', 30)


duration_power = 7000  

power_time = 0


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

            case 'Many_balls':
                if activate:
                    plus_balls=GeneralPower.many_balls()
                    for i in range(plus_balls):
                        balls_in_game.append(Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO))
                        balls_in_game[-1].speed[0]-=abs(random.choice([1,1.3,1.5]))                
                        balls_in_game[-1].speed[1]-=abs(random.choice([1,1.3,1.5]))                
                else:
                    pass

            case 'Small_player1' | 'Small_player2':
                if activate:
                    PlayerPower.small_player(player1, player2)
                else:
                    if PlayerPower.players_small_debuff:
                        PlayerPower.players_small_debuff.pop(0).height=cg.JOGADOR_TAMANHO
                    
            case 'Lock_player1' | 'Lock_player2':
                if activate:
                    PlayerPower.lock_player(player1, player2)
                else:
                    if PlayerPower.players_with_lock_debuff:
                        PlayerPower.players_with_lock_debuff.pop(0).free=True
    @staticmethod
    def manage_powers(power_type):
        match power_type:
            case 'Fast_ball':
                main_ball.color=(255,0,0)
            case 'Lock_player1' | 'Lock_player2':
                for player_locked in PlayerPower.players_with_lock_debuff:
                    pygame.draw.line(screen, (255,0,0), (player_locked.position.x, cg.ALTURA), (player_locked.position.x, 50), 2)

def false_scored_extra_balls(ball):    
    if ball.position.x > cg.LARGURA or ball.position.x < 0:
            return True
    return False
    
def scored(ball):
    
    if ball.position.x > cg.LARGURA:
        player2.score+=1
        return True

    elif ball.position.x < 0:
        player1.score+=1
        return True

    return False
    

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
            
def who_win(player1, player2, max_points):
    if (player1.score >= player2.score + 2) and max(player1.score, player2.score) >= max_points:
        return player1.nome
    elif (player2.score >= player1.score + 2) and max(player1.score, player2.score) >= max_points:
        return player2.nome
    
    return False

while running:
    menu_option = menu.run()

    wait_time = random.choice([3000,4000,5000]) 
    inicial_time = pygame.time.get_ticks()

    if menu_option == "jogar 5":
        max_points = 5
        
    elif menu_option == "jogar 10":
        max_points = 10
        
    elif menu_option == "jogar inf":
        max_points = -1
        
    elif menu_option == 'sair':
        pygame.quit()
        
    ball = Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO)
    player1 = player(menu.nome1, cg.JOGADOR_TAMANHO, cg.JOGADOR1_POS, cg.TELA)
    player2 = player(menu.nome2, cg.JOGADOR_TAMANHO, cg.JOGADOR2_POS, cg.TELA, is_player1=False)

    players = [player1, player2]
    balls_in_game=[ball]
    main_ball=balls_in_game[0]
    possible_powers=['Fast_ball','Lock_player1','Lock_player2','Small_ball','Small_player1','Small_player2', 'Many_balls']
    powers_in_game={}
        
    while max_points != 0:
        dt = clock.tick(cg.FPS) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                max_points = 0
                running = False
                    
        
        screen.fill(cg.COR_FUNDO)
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect((cg.LARGURA // 2), 0, 5, cg.ALTURA))

        actual_time = pygame.time.get_ticks()

        if actual_time - inicial_time >= wait_time:

            available_powers = [power for power in possible_powers if power not in powers_in_game ]

            if available_powers:
                new_power = random.choice(available_powers)
                Power.select_power(new_power, True)
                powers_in_game[new_power] = actual_time

            inicial_time = actual_time
            wait_time = random.choice([2000, 3000, 4000, 5000])

        for power, start_time in list(powers_in_game.items()):

            Power.manage_powers(power)

            if actual_time - start_time >= duration_power:
                Power.select_power(power, False)

                del powers_in_game[power]


        vel_bola = pygame.Vector2(ball.speed).length() * cg.FPS

        for p in players:  
            p.update(dt, screen)
            colidir(main_ball, p)
            p.speed = vel_bola
        
        for ball in balls_in_game[:]:
            ball.update(screen)
            if ball==main_ball:
                if scored(ball):
                    point_sound.play()
                    balls_in_game.remove(ball)
                    balls_in_game.append(Ball(cg.BOLA_POS_INICIAL, cg.TELA, cg.BOLA_TAMANHO))
                    main_ball=balls_in_game[-1]
            else:
                if false_scored_extra_balls(ball):
                    balls_in_game.remove(ball)

            
        keys = pygame.key.get_pressed()
        winner = who_win(player1, player2, max_points)

        if (winner != False and max_points > 0) or keys[pygame.K_ESCAPE]:
            it_is_over = Game_over(screen, clock, winner)
            it_is_over.run()
            player1.score = 0
            player2.score = 0
            max_points = 0
        
        pygame.draw.line(screen, (255,255,255), (0, 50), (1280, 50), 4)
        screen.blit(pygame.font.SysFont('consolas', 30).render(f'{player1.score}', True, (255,255,255), None), [(cg.LARGURA//2)+30, 15])
        screen.blit(pygame.font.SysFont('consolas', 30).render(f'{player2.score}', True, (255,255,255), None), [(cg.LARGURA//2)-40, 15])

        pygame.display.flip()

pygame.quit()