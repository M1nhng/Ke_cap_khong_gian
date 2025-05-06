import pygame
import random
import math
from items import Item, ITEM_TYPES

class Enemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level

        self.image = pygame.image.load('D:/Python/Game/images/ghost.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -100
        self.speed = 0.9 if level == 1 else 1.2
        self.dy = self.speed
        self.health = 1 + level // 2
        self.bullets = []
        self.shoot_cooldown = 90 - level * 5
        self.shoot_timer = 0
        self.bullet_speed = 0.1 + level * 0.2
        self.player_pos = player_pos

    def update(self):
        self.rect.y += self.dy
        if self.rect.y > self.screen_height:
            self.health = 0

    def shoot(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        bullet_rect = pygame.Rect(bullet_x, bullet_y, 34, 34)
        if self.rect.colliderect(bullet_rect):
            self.health -= 1
            return True
        return False

    def is_dead(self):
        return self.health <= 0

    def drop_item(self):
        drop_chance = 0.3 if self.level == 1 else 0.4
        if random.random() < drop_chance:
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

class DiagonalEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.image = pygame.image.load('D:/Python/Game/images/enemy_cheo.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -100
        self.direction = random.choice(['left', 'right'])
        self.dx = -0.4 if self.direction == 'left' else 0.4
        self.dy = 0.4
        self.health = 1
        self.bullets = []
        self.player_pos = player_pos

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right > self.screen_width:
            self.dx = -abs(self.dx)
            self.rect.right = self.screen_width
        elif self.rect.left < 0:
            self.dx = abs(self.dx)
            self.rect.left = 0
        if self.rect.y > self.screen_height:
            self.health = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        bullet_rect = pygame.Rect(bullet_x, bullet_y, 34, 34)
        if self.rect.colliderect(bullet_rect):
            self.health -= 1
            return True
        return False

    def is_dead(self):
        return self.health <= 0

    def drop_item(self):
        item_type = random.choice(ITEM_TYPES)
        radius = 50
        angle = random.uniform(0, 2 * math.pi)
        offset_x = math.cos(angle) * random.uniform(0, radius)
        offset_y = math.sin(angle) * random.uniform(0, radius)
        spawn_x = self.rect.centerx + offset_x
        spawn_y = self.rect.centery + offset_y
        player_x, player_y = self.player_pos()
        return Item(spawn_x, spawn_y, item_type, player_x, player_y)

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
        self.shoot_cooldown = 1.5 * 240
        self.bullet_speed = 3.0
        self.bullets = []
        self.player_pos = player_pos
        self.health = 30

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
            self.health -= 1
            return True
        return False

    def is_dead(self):
        if self.health <= 0:
            return True
        return False

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

class ShotgunEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.image = pygame.image.load('D:/Python/Game/images/robot.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, screen_width - 100)
        self.rect.y = -200
        self.speed = 0.3 + (level - 1) * 0.04
        self.health = 10 + level * 2
        self.shoot_timer = 0
        self.shoot_cooldown = 240  # Tăng từ 120 lên 240 (1 giây ở 240 FPS)
        self.bullet_speed = 1.0  # Giảm từ 1.5 xuống 1.0 để làm chậm đạn
        self.bullets = []
        self.player_pos = player_pos

    def update(self):
        self.rect.y += self.speed
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
        screen.blit(self.image, self.rect.topleft)  # Đảm bảo hiển thị hình ảnh
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        if abs(bullet_x - self.rect.centerx) < 40 and abs(bullet_y - self.rect.centery) < 50:
            self.health -= 1
            return True
        return False

    def is_dead(self):
        return self.health <= 0

class ShadowEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.image = pygame.image.load('D:/Python/Game/images/devil.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = random.randint(50, screen_height - 50)
        self.speed = 2.0 + level * 0.1
        self.health = 2 + level // 2
        self.timer = 0
        self.charge_time = 7 * 240
        self.is_charging = False
        self.bullets = []
        self.player_pos = player_pos

    def teleport(self):
        self.rect.x = random.randint(50, self.screen_width - 50)
        self.rect.y = random.randint(50, self.screen_height - 50)

    def update(self):
        if not self.is_charging:
            self.timer += 1
            if self.timer >= self.charge_time:
                self.is_charging = True
        else:
            player_x, player_y = self.player_pos()
            dx = player_x - self.rect.centerx
            dy = player_y - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 5:
                dx /= dist
                dy /= dist
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        if abs(bullet_x - self.rect.centerx) < 30 and abs(bullet_y - self.rect.centery) < 30:
            self.health -= 1
            if not self.is_dead():
                self.teleport()
            return True
        return False

    def is_dead(self):
        return self.health <= 0

class BossEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.image = pygame.image.load('D:/Python/Game/images/boss.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - self.rect.width) // 2
        self.rect.y = 0
        self.speed = 0.5
        self.health = 50 + level * 5
        self.mode = 1
        self.mode_timer = 0
        self.mode_switch_time = 10 * 240
        self.shoot_timer = 0
        self.bullet_speed = 2.0
        self.bullets = []
        self.player_pos = player_pos
        self.laser_width = screen_width // 5
        self.laser_left_x = random.randint(100, screen_width - 2 * self.laser_width - 100)
        self.laser_right_x = self.laser_left_x + self.laser_width + 100
        self.laser_left_center = self.laser_left_x + self.laser_width // 2
        self.laser_right_center = self.laser_right_x + self.laser_width // 2
        self.laser_timer = 0
        self.laser_warning_time = 3 * 240
        self.laser_active = False
        self.laser_narrow_speed = 0.5
        self.boundary_y = 850
        self.laser_duration = 7 * 240

    def update(self):
        if self.rect.y < 100:
            self.rect.y += self.speed
        self.mode_timer += 1
        if self.mode_timer >= self.mode_switch_time:
            self.mode = 2 if self.mode == 1 else 1
            self.mode_timer = 0
            if self.mode == 2:
                self.laser_width = self.screen_width // 5
                self.laser_left_x = random.randint(100, self.screen_width - 2 * self.laser_width - 100)
                self.laser_right_x = self.laser_left_x + self.laser_width + 100
                self.laser_left_center = self.laser_left_x + self.laser_width // 2
                self.laser_right_center = self.laser_right_x + self.laser_width // 2
                self.laser_timer = 0
                self.laser_active = False

        self.shoot_timer += 1
        if self.mode == 1:
            if self.shoot_timer >= 60:
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
        elif self.mode == 2:
            self.laser_timer += 1
            if self.laser_timer < self.laser_warning_time:
                pass
            elif self.laser_timer < self.laser_duration:
                self.laser_active = True
                self.laser_width -= self.laser_narrow_speed * 2
                if self.laser_width < 50:
                    self.laser_width = 50
                self.laser_left_x = self.laser_left_center - self.laser_width // 2
                self.laser_right_x = self.laser_right_center - self.laser_width // 2
                if self.shoot_timer >= 10:
                    self.shoot_timer = 0
                    for laser_x in [self.laser_left_x + self.laser_width // 2, self.laser_right_x + self.laser_width // 2]:
                        self.bullets.append({
                            'x': laser_x,
                            'y': 100,
                            'dx': 0,
                            'dy': self.bullet_speed
                        })
            else:
                self.laser_active = False
                self.laser_timer = 0
                self.laser_width = self.screen_width // 5
                self.laser_left_x = random.randint(100, self.screen_width - 2 * self.laser_width - 100)
                self.laser_right_x = self.laser_left_x + self.laser_width + 100
                self.laser_left_center = self.laser_left_x + self.laser_width // 2
                self.laser_right_center = self.laser_right_x + self.laser_width // 2

        for b in self.bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)
        if self.mode == 2 and self.laser_timer < self.laser_duration:
            color = (255, 0, 0, 128) if self.laser_timer < self.laser_warning_time else (255, 0, 0)
            pygame.draw.rect(screen, color, (self.laser_left_x, 0, self.laser_width, self.boundary_y), 2 if self.laser_timer < self.laser_warning_time else 0)
            pygame.draw.rect(screen, color, (self.laser_right_x, 0, self.laser_width, self.boundary_y), 2 if self.laser_timer < self.laser_warning_time else 0)

    def hit_by(self, bullet_x, bullet_y):
        if abs(bullet_x - self.rect.centerx) < 75 and abs(bullet_y - self.rect.centery) < 75:
            if self.mode == 1:
                return False
            self.health -= 1
            return True
        return False

    def reflect_bullet(self, bullet_x, bullet_y):
        if self.mode == 1 and abs(bullet_x - self.rect.centerx) < 75 and abs(bullet_y - self.rect.centery) < 75:
            return True
        return False

    def is_dead(self):
        return self.health <= 0