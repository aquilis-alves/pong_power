import pygame

class player:
    def __init__(self, height, position, screen_size, max_speed=500, color="white", is_player1=True):
        self.height = height
        self.position = pygame.Vector2(position)
        self.screen_size = screen_size
        self.color = color
        self.max_speed = max_speed
        self.speed = pygame.Vector2(0, 0)
        self.width = 15
        self.form = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        self.score = 0
        self.increase_speed = 1
        self.free = True
        self.is_player1 = is_player1

        # --- dash ---
        self.dash_speed = 1500          # velocidade durante o dash
        self.dash_duration = 0.12       # segundos que o dash dura
        self.dash_cooldown = 1.0        # segundos até poder dar dash de novo
        self.double_tap_window = 0.25   # tempo máximo entre os dois toques
        self.dash_timer = 0.0           # > 0 enquanto está em dash
        self.dash_cooldown_timer = 0.0
        self.time_since_tap = float("inf")
        self.forward_was_pressed = False

    def update(self, dt, screen):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if self.is_player1:
            up, down, left, right = pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d
            forward_key, forward_dir = pygame.K_d, 1
        else:
            up, down, left, right = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
            forward_key, forward_dir = pygame.K_LEFT, -1

        # --- timers ---
        self.time_since_tap += dt
        self.dash_timer = max(0, self.dash_timer - dt)
        self.dash_cooldown_timer = max(0, self.dash_cooldown_timer - dt)

        # --- detecta duplo toque na tecla de frente ---
        forward_pressed = keys[forward_key]
        just_pressed = forward_pressed and not self.forward_was_pressed
        self.forward_was_pressed = forward_pressed

        if just_pressed and self.free:
            if self.time_since_tap <= self.double_tap_window and self.dash_cooldown_timer <= 0:
                self.dash_timer = self.dash_duration
                self.dash_cooldown_timer = self.dash_cooldown
                self.time_since_tap = float("inf")  # evita triplo toque disparar outro dash
            else:
                self.time_since_tap = 0

        # --- movimento ---
        if self.dash_timer > 0:
            # durante o dash, ignora o input horizontal e vai reto pra frente
            self.speed = pygame.Vector2(forward_dir * self.dash_speed, 0)
            # ainda permite mover em y normalmente
            if keys[up]:
                self.speed.y -= self.max_speed
            if keys[down]:
                self.speed.y += self.max_speed
        else:
            if keys[up]:
                direction.y -= 1
            if keys[down]:
                direction.y += 1
            if keys[left] and self.free:
                direction.x -= 1
            if keys[right] and self.free:
                direction.x += 1

            if direction.length() > 0:
                direction = direction.normalize()

            self.speed = direction * self.max_speed

        self.position += self.speed * dt
        self.position.x = max(0, min(self.position.x, self.screen_size[0] - self.width))
        self.position.y = max(50, min(self.position.y, self.screen_size[1] - self.height))

        self.form = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.form)