import pygame
import random
import math
from items import Item, ITEM_TYPES

class BombEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.image = pygame.image.load('D:/Python/Game/images/enemy_bom.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.speed = 1.0
        self.dx = self.speed
        self.shoot_timer = 0
        self.shoot_cooldown = 2.5 * 240
        self.bullet_speed = 3.0
        self.bullets = []
        self.player_pos = player_pos
        self.health = 60  # Default health, can be overridden by Game.py

    def update(self):
        self.rect.x += self.dx
        if self.rect.right > self.screen_width:
            self.dx = -self.speed
            self.rect.right = self.screen_width
        elif self.rect.left < 0:
            self.dx = self.speed
            self.rect.left = 0
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            player_x, player_y = self.player_pos()
            angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
            dx = math.cos(angle) * self.bullet_speed
            dy = math.sin(angle) * self.bullet_speed
            self.bullets.append({
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'dx': dx,
                'dy': dy
            })
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
        bullet_rect = pygame.Rect(bullet_x, bullet_y, 34, 34)
        if self.rect.colliderect(bullet_rect):
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