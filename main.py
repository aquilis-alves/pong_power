import pygame
from player import player

# pygame setup
screen_size = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True
dt = 0
background_color = "black"

player1 = player(100, (50, 360), screen_size)
player2 = player(100, (1230, 360), screen_size)

players = [player1, player2]

while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background_color)
    
    for player in players:
        player.update(dt)
        player.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()