import pygame
import random
import math

class ShadowEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thông số cơ bản của ShadowEnemy
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Cấp độ hiện tại của game

        # Tải và scale hình ảnh enemy (devil.png)
        self.image = pygame.image.load('D:/Python/Game/images/devil.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()

        # Đặt vị trí ban đầu ngẫu nhiên trên màn hình
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = random.randint(50, screen_height - 50)

        # Tốc độ di chuyển (tăng theo level)
        self.speed = 2.0 + level * 0.1

        # Máu của enemy (tăng theo level)
        self.health = 2 + level // 2

        # Thiết lập cơ chế dịch chuyển và lao vào người chơi
        self.timer = 0
        self.charge_time = 7 * 240  # Thời gian chờ trước khi lao
        self.is_charging = False  # Trạng thái lao vào người chơi

        # Danh sách đạn của enemy
        self.bullets = []

        self.player_pos = player_pos  # Vị trí của người chơi

    def teleport(self):
        # Dịch chuyển ngẫu nhiên đến vị trí mới
        self.rect.x = random.randint(50, self.screen_width - 50)
        self.rect.y = random.randint(50, self.screen_height - 50)

    def update(self):
        # Cập nhật trạng thái enemy
        if not self.is_charging:
            self.timer += 1
            if self.timer >= self.charge_time:
                self.is_charging = True  # Bắt đầu lao vào người chơi
        else:
            # Lao vào người chơi
            player_x, player_y = self.player_pos()
            dx = player_x - self.rect.centerx
            dy = player_y - self.rect.centery
            dist = math.hypot(dx, dy)  # Khoảng cách đến người chơi
            if dist > 5:
                dx /= dist
                dy /= dist
                self.rect.x += dx * self.speed  # Di chuyển theo trục x
                self.rect.y += dy * self.speed  # Di chuyển theo trục y

    def draw(self, screen):
        # Vẽ enemy lên màn hình
        screen.blit(self.image, self.rect.topleft)

        # Vẽ các viên đạn của enemy
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        # Kiểm tra xem enemy có bị trúng đạn không
        if abs(bullet_x - self.rect.centerx) < 30 and abs(bullet_y - self.rect.centery) < 30:
            self.health -= 1  # Giảm máu khi bị trúng
            if not self.is_dead():
                self.teleport()  # Dịch chuyển nếu chưa chết
            return True
        return False

    def is_dead(self):
        # Kiểm tra xem enemy có chết không
        return self.health <= 0