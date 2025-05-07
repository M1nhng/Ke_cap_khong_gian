import pygame
import random
import math
from items import Item, ITEM_TYPES

class ShotgunEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        try:
            self.image = pygame.image.load('D:/Python/Game/images/robot.png')
            self.image = pygame.transform.scale(self.image, (100, 100))
        except pygame.error as e:
            print(f"Error loading robot.png: {e}")
            self.image = pygame.Surface((100, 100))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, screen_width - 100)
        self.rect.y = 100
        self.horizontal_speed = 1
        self.direction = random.choice(['left', 'right'])
        self.dx = -self.horizontal_speed if self.direction == 'left' else self.horizontal_speed
        self.shoot_timer = 0
        self.shoot_cooldown = 300
        self.bullet_speed = 1
        self.bullets = []
        self.player_pos = player_pos
        self.health = 15  # Default health, can be overridden by Game.py

    def update(self):
        print(f"ShotgunEnemy updating: dx={self.dx}, pos={self.rect.topleft}")
        self.rect.x += self.dx
        if self.rect.right > self.screen_width:
            self.dx = -abs(self.horizontal_speed)
            self.rect.right = self.screen_width
            print(f"ShotgunEnemy hit right wall, new dx={self.dx}")
        elif self.rect.left < 0:
            self.dx = abs(self.horizontal_speed)
            self.rect.left = 0
            print(f"ShotgunEnemy hit left wall, new dx={self.dx}")
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            player_x, player_y = self.player_pos()
            for i in range(3):
                angle = math.atan2(player_y - self.rect.y, player_x - self.rect.x) + random.uniform(-0.4, 0.4)
                dx = math.cos(angle) * self.bullet_speed
                dy = math.sin(angle) * self.bullet_speed
                self.bullets.append({'x': self.rect.x + 40, 'y': self.rect.y + 50, 'dx': dx, 'dy': dy})
        for b in self.bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        if abs(bullet_x - self.rect.centerx) < 40 and abs(bullet_y - self.rect.centery) < 50:
            return True
        return False

    def is_dead(self):
        return self.health <= 0

    def drop_item(self):
        if random.random() < 0.5:
            item_type = random.choice(ITEM_TYPES)
            radius = 50
            angle = random.uniform(0, 2 * math.pi)
            offset_x = math.cos(angle) * random.uniform(0, radius)
            offset_y = math.sin(angle) * random.uniform(0, radius)
            spawn_x = self.rect.centerx + offset_x
            spawn_y = self.rect.centery + offset_y
            player_x, player_y = self.player_pos()
            return Item(spawn_x, spawn_y, item_type, player_x, player_y)
        return None