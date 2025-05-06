import pygame
import random
import math
from items import Item, ITEM_TYPES

class BombEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thông số cơ bản của BombEnemy
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Cấp độ hiện tại của game

        # Tải và scale hình ảnh enemy (enemy_bom.png)
        self.image = pygame.image.load('D:/Python/Game/images/enemy_bom.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # Đặt vị trí ban đầu
        self.rect.x = 50
        self.rect.y = 50

        # Tốc độ di chuyển
        self.speed = 1.0
        self.dx = self.speed  # Vận tốc theo trục x

        # Thiết lập bắn đạn
        self.shoot_timer = 0
        self.shoot_cooldown = 2.5 * 240  # Thời gian chờ giữa các lần bắn
        self.bullet_speed = 3.0  # Tốc độ đạn
        self.bullets = []  # Danh sách đạn

        # Máu của enemy
        self.health = 60

        self.player_pos = player_pos  # Vị trí của người chơi

    def update(self):
        # Cập nhật vị trí enemy
        self.rect.x += self.dx  # Di chuyển theo trục x

        # Xử lý va chạm với biên màn hình
        if self.rect.right > self.screen_width:
            self.dx = -self.speed  # Đổi hướng sang trái
            self.rect.right = self.screen_width
        elif self.rect.left < 0:
            self.dx = self.speed  # Đổi hướng sang phải
            self.rect.left = 0

        # Cập nhật thời gian bắn
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            # Bắn đạn về phía người chơi
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

        # Cập nhật vị trí các viên đạn
        for b in self.bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            # Xóa đạn nếu ra khỏi màn hình
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def draw(self, screen):
        # Vẽ enemy lên màn hình
        screen.blit(self.image, self.rect.topleft)

        # Vẽ các viên đạn của enemy
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        # Kiểm tra xem enemy có bị trúng đạn không
        bullet_rect = pygame.Rect(bullet_x, bullet_y, 34, 34)
        if self.rect.colliderect(bullet_rect):
            self.health -= 1  # Giảm máu khi bị trúng
            return True
        return False

    def is_dead(self):
        # Kiểm tra xem enemy có chết không
        return self.health <= 0

    def drop_item(self):
        # Xử lý rơi vật phẩm khi enemy chết
        if random.random() < 0.5:  # 50% xác suất rơi vật phẩm
            item_type = random.choice(ITEM_TYPES)  # Chọn ngẫu nhiên loại vật phẩm
            radius = 50  # Bán kính sinh vật phẩm
            angle = random.uniform(0, 2 * math.pi)  # Góc ngẫu nhiên
            offset_x = math.cos(angle) * random.uniform(0, radius)  # Offset x
            offset_y = math.sin(angle) * random.uniform(0, radius)  # Offset y
            spawn_x = self.rect.centerx + offset_x  # Vị trí x của vật phẩm
            spawn_y = self.rect.centery + offset_y  # Vị trí y của vật phẩm
            player_x, player_y = self.player_pos()  # Lấy vị trí người chơi
            return Item(spawn_x, spawn_y, item_type, player_x, player_y)  # Tạo vật phẩm
        return None