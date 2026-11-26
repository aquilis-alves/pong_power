import pygame
import random

class Ball:
    speed_XY=(3,-3)

    def __init__(self, position, screen_size, radius, color="white"):
        self.position=pygame.Vector2(position)
        self.screen_size=screen_size
        self.radius=radius
        self.speed=[random.choice(Ball.speed_XY), random.choice(Ball.speed_XY)]
        self.color=color
        self.form=pygame.Rect(self.position.x, self.position.y, self.radius, self.radius)

    def update(self, screen):

        superiorBorder, inferiorBorder = 0, 720
        
        if self.position.y>inferiorBorder or self.position.y<superiorBorder:
            self.speed[1]*=-1

        self.position.x+=self.speed[0]
        self.position.y+=self.speed[1]

        self.form=pygame.Rect(self.position.x, self.position.y, self.radius, self.radius)
        
       
        pygame.draw.ellipse(screen, self.color, self.form)
        

        

   

        
        

        


        