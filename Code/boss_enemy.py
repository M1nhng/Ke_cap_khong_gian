import pygame
import math
import random

class BossEnemy:
    def __init__(self, level, screen_width, screen_height, get_player_pos):
        self.level = level
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.get_player_pos = get_player_pos
        self.image = pygame.image.load('D:/Python/Game/images/boss.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2 - self.rect.width // 2
        self.rect.y = 50
        self.health = 5000  # Reduced from 10000
        self.max_health = 5000  # Reduced from 10000
        self.bullets = []
        self.shoot_timer = 0
        self.phase = 1
        self.phase_timer = 0
        self.phase_duration = 12000  # Increased to 12 seconds
        self.start_time = pygame.time.get_ticks()
        self.invulnerable_timer = 0
        self.zigzag_speed = 2  # Reduced from 5
        self.zigzag_direction = 1
        self.orbit_angle = 0
        self.flash_timer = 0

    def update(self):
        # Update invulnerability
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

        # Update phase based on time or health
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        health_percentage = self.health / self.max_health
        if elapsed_time >= self.phase_duration or (health_percentage <= 0.85 and self.phase == 1) or \
           (health_percentage <= 0.65 and self.phase == 2) or (health_percentage <= 0.45 and self.phase == 3):
            self.phase = (self.phase % 4) + 1  # Continuous cycling through phases 1-4
            self.start_time = current_time
            self.shoot_timer = 0
            self.invulnerable_timer = 480  # Increased to 2 seconds
            self.flash_timer = 480  # Flash for 2 seconds

        # Update flash timer for transition effect
        if self.flash_timer > 0:
            self.flash_timer -= 1

        # Movement based on phase
        if self.phase == 1:
            # Phase 1: Smooth side-to-side sine wave
            center_x = self.screen_width // 2 - self.rect.width // 2
            amplitude = 150  # Reduced from 300
            omega = 0.001
            self.rect.x = center_x + amplitude * math.sin(omega * current_time)
            self.rect.y = 50
        elif self.phase == 2:
            # Phase 2: Zigzag movement
            self.rect.x += self.zigzag_speed * self.zigzag_direction
            self.rect.y += 1  # Reduced from 2
            if self.rect.x <= 50 or self.rect.x >= self.screen_width - self.rect.width - 50:
                self.zigzag_direction *= -1
            if self.rect.y > 200:
                self.rect.y = 50
        elif self.phase == 3:
            # Phase 3: Circular orbit around screen center
            center_x = self.screen_width // 2
            center_y = self.screen_height // 4
            radius = 200  # Increased from 150
            self.orbit_angle += 0.01  # Reduced from 0.02
            self.rect.x = center_x + radius * math.cos(self.orbit_angle) - self.rect.width // 2
            self.rect.y = center_y + radius * math.sin(self.orbit_angle) - self.rect.height // 2
        elif self.phase == 4:
            # Phase 4: Slow approach toward player
            player_x, player_y = self.get_player_pos()
            angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
            speed = 1.5  # Reduced from 3
            self.rect.x += speed * math.cos(angle)
            self.rect.y += speed * math.sin(angle)

        # Ensure boss stays within screen bounds
        self.rect.x = max(50, min(self.rect.x, self.screen_width - self.rect.width - 50))
        self.rect.y = max(50, min(self.rect.y, self.screen_height // 2))

        # Shoot based on phase
        self.shoot()

    def shoot(self):
        self.shoot_timer += 1
        player_x, player_y = self.get_player_pos()

        if self.phase == 1 and self.shoot_timer >= 150:  # Increased to ~0.625s
            # Phase 1: Aimed bullets with slight random variation
            angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx) + random.uniform(-0.1, 0.1)
            bullet = {
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'speed': 4,  # Reduced from 6
                'angle': angle,
                'color': (255, 0, 0)  # Red
            }
            self.bullets.append(bullet)
            self.shoot_timer = 0

        elif self.phase == 2 and self.shoot_timer >= 210:  # Increased to ~0.875s
            # Phase 2: Wide spread shot with varying speeds
            for i in range(-2, 3):  # Reduced from 7 to 5 bullets
                angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx) + i * 0.25
                speed = 3 + abs(i) * 0.5  # Reduced base speed from 4
                bullet = {
                    'x': self.rect.centerx,
                    'y': self.rect.centery,
                    'speed': speed,
                    'angle': angle,
                    'color': (0, 255, 0)  # Green
                }
                self.bullets.append(bullet)
            self.shoot_timer = 0

        elif self.phase == 3 and self.shoot_timer >= 120:  # Increased to ~0.5s
            # Phase 3: Player-biased wave pattern
            base_angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
            for i in range(-2, 3):
                angle = base_angle + i * 0.15  # Narrow spread
                bullet = {
                    'x': self.rect.centerx,
                    'y': self.rect.centery,
                    'speed': 3,  # Slow speed
                    'angle': angle,
                    'color': (0, 0, 255)  # Blue
                }
                self.bullets.append(bullet)
            self.shoot_timer = 0

        elif self.phase == 4 and self.shoot_timer >= 300:  # Increased to ~1.25s
            # Phase 4: Homing missiles
            angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
            bullet = {
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'speed': 2,  # Reduced from 3
                'angle': angle,
                'color': (255, 255, 0),  # Yellow
                'homing': True,
                'target_x': player_x,
                'target_y': player_y,
                'homing_timer': 120  # Reduced to 0.5s
            }
            self.bullets.append(bullet)
            self.shoot_timer = 0

        # Update bullet positions
        for bullet in self.bullets[:]:
            if bullet.get('homing') and bullet.get('homing_timer', 0) > 0:
                player_x, player_y = self.get_player_pos()
                bullet['target_x'] = player_x
                bullet['target_y'] = player_y
                angle = math.atan2(bullet['target_y'] - bullet['y'], bullet['target_x'] - bullet['x'])
                bullet['angle'] = angle
                bullet['homing_timer'] -= 1
            bullet['x'] += bullet['speed'] * math.cos(bullet['angle'])
            bullet['y'] += bullet['speed'] * math.sin(bullet['angle'])
            if (bullet['x'] < 0 or bullet['x'] > self.screen_width or
                bullet['y'] < 0 or bullet['y'] > self.screen_height):
                self.bullets.remove(bullet)

    def draw(self, screen):
        # Flash effect during phase transition
        if self.flash_timer % 8 < 4:
            screen.blit(self.image, self.rect)
        # Draw health bar
        bar_width = 200
        bar_height = 20
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x - 25, self.rect.y - 30, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x - 25, self.rect.y - 30, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        # Draw bullets with phase-specific colors
        for bullet in self.bullets:
            pygame.draw.circle(screen, bullet['color'], (int(bullet['x']), int(bullet['y'])), 5)

    def hit_by(self, x, y):
        if self.invulnerable_timer > 0:
            return False
        return self.rect.collidepoint(x, y)

    def is_dead(self):
        return self.health <= 0

    def drop_item(self):
        return None  # Boss drops item in Game.run