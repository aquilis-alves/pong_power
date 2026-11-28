import pygame

class player:
    def __init__(self, nome, height, position, screen_size, max_speed=500, color="white", is_player1=True):
        self.nome = nome
        
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

        # teclas de movimento
        if is_player1:
            self.k_up, self.k_down, self.k_left, self.k_right = pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d
            forward_key, forward_vec = pygame.K_d, pygame.Vector2(1, 0)
        else:
            self.k_up, self.k_down, self.k_left, self.k_right = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
            forward_key, forward_vec = pygame.K_LEFT, pygame.Vector2(-1, 0)

        # --- dash ---
        self.dash_speed = 1500
        self.dash_duration = 0.12
        self.dash_cooldown = 1.0
        self.double_tap_window = 0.25
        self.dash_timer = 0.0
        self.dash_cooldown_timer = 0.0
        self.dash_dir = pygame.Vector2(0, 0)

        self.dash_keys = {
            self.k_up: pygame.Vector2(0, -1),
            self.k_down: pygame.Vector2(0, 1),
            forward_key: forward_vec,
        }
        
        self.time_since_tap = {k: float("inf") for k in self.dash_keys}
        self.was_pressed = {k: False for k in self.dash_keys}

    def _check_dash(self, keys, dt):
        for key, vec in self.dash_keys.items():
            self.time_since_tap[key] += dt

            pressed = keys[key]
            just_pressed = pressed and not self.was_pressed[key]
            self.was_pressed[key] = pressed

            if not just_pressed:
                continue

            if vec.x != 0 and not self.free:
                continue

            if self.time_since_tap[key] <= self.double_tap_window and self.dash_cooldown_timer <= 0:
                self.dash_timer = self.dash_duration
                self.dash_cooldown_timer = self.dash_cooldown
                self.dash_dir = vec.copy()
                self.time_since_tap[key] = float("inf")
            else:
                self.time_since_tap[key] = 0

    def update(self, dt, screen):
        keys = pygame.key.get_pressed()

        self.dash_timer = max(0, self.dash_timer - dt)
        self.dash_cooldown_timer = max(0, self.dash_cooldown_timer - dt)

        if self.dash_timer <= 0:
            self._check_dash(keys, dt)

        if self.dash_timer > 0:
            self.speed = self.dash_dir * self.dash_speed
        else:
            direction = pygame.Vector2(0, 0)
            if keys[self.k_up]:
                direction.y -= 1
            if keys[self.k_down]:
                direction.y += 1
            if keys[self.k_left] and self.free:
                direction.x -= 1
            if keys[self.k_right] and self.free:
                direction.x += 1

            if direction.length() > 0:
                direction = direction.normalize()

            self.speed = direction * self.max_speed

        self.position += self.speed * dt
        self.position.x = max(0, min(self.position.x, self.screen_size[0] - self.width))
        self.position.y = max(50, min(self.position.y, self.screen_size[1] - self.height))

        self.form = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

        color = "cyan" if self.dash_timer > 0 else self.color
        pygame.draw.rect(screen, color, self.form)