import pygame

class player:
    def __init__(self, height, position, screen_size ,max_speed=300, color="white"):
        self.height = height
        self.position = pygame.Vector2(position)
        self.screen_size = screen_size
        self.color = color
        self.max_speed = max_speed
        self.speed=pygame.Vector2(0,0)
        self.width = 15
        self.form=pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        self.score=0
        self.free=False

    def update(self, dt, screen):

        
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        # checa se o player esta na esquerda ou na direita
        if self.position.x < (self.screen_size[0] / 2):
            if keys[pygame.K_w]:
                direction.y -= 1
            if keys[pygame.K_s]:
                direction.y += 1
            if keys[pygame.K_a] and self.free:
                direction.x -= 1
            if keys[pygame.K_d] and self.free:
                direction.x += 1
        
        else:
            if keys[pygame.K_UP]:
                direction.y -= 1
            if keys[pygame.K_DOWN]:
                direction.y += 1
            if keys[pygame.K_LEFT] and self.free:
                direction.x -= 1
            if keys[pygame.K_RIGHT] and self.free:
                direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()  # evita andar mais rápido na diagonal

        self.position += direction * self.speed * dt

        self.speed=direction*self.max_speed
        
        self.position.x = max(0, min(self.position.x, self.screen_size[0] - self.width))
        self.position.y = max(50, min(self.position.y, self.screen_size[1] - self.height))

        self.form=pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.form)

    
        