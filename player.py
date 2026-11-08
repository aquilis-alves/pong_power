import pygame

class player:
    def __init__(self, height, position, screen_size ,speed=300, color="white"):
        self.height = height
        self.position = pygame.Vector2(position)
        self.screen_size = screen_size
        self.color = color
        self.speed = speed
        self.width = 15
        
    def update(self, dt, free=False):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        # checa se o player esta na esquerda ou na direita
        if self.position.x < self.screen_size[0] / 2:
            if keys[pygame.K_w]:
                direction.y -= 1
            if keys[pygame.K_s]:
                direction.y += 1
            if keys[pygame.K_a] and free:
                direction.x -= 1
            if keys[pygame.K_d] and free:
                direction.x += 1
        
        else:
            if keys[pygame.K_UP]:
                direction.y -= 1
            if keys[pygame.K_DOWN]:
                direction.y += 1
            if keys[pygame.K_LEFT] and free:
                direction.x -= 1
            if keys[pygame.K_RIGHT] and free:
                direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()  # evita andar mais rápido na diagonal

        self.position += direction * self.speed * dt
        
        self.position.x = max(0, min(self.position.x, self.screen_size[0] - self.width))
        self.position.y = max(0, min(self.position.y, self.screen_size[1] - self.height))

    def draw(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        