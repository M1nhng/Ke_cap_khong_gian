import pygame
import random
import math
from items import Item, ITEM_TYPES

class Enemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thông số cơ bản của enemy
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Cấp độ hiện tại của game

        # Tải và scale hình ảnh enemy (ghost.png)
        self.image = pygame.image.load('D:/Python/Game/images/ghost.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()

        # Đặt vị trí ban đầu ngẫu nhiên ở phía trên màn hình
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -100

        # Tốc độ di chuyển (tăng theo level)
        self.speed = 0.9 if level == 1 else 1.2
        self.dy = self.speed  # Vận tốc theo trục y

        # Máu của enemy (tăng theo level)
        self.health = 1 + level // 2

        # Danh sách đạn của enemy
        self.bullets = []
        self.shoot_cooldown = 90 - level * 5  # Thời gian chờ giữa các lần bắn
        self.shoot_timer = 0  # Bộ đếm thời gian bắn
        self.bullet_speed = 0.1 + level * 0.2  # Tốc độ đạn
        self.player_pos = player_pos  # Vị trí của người chơi

    def update(self):
        # Cập nhật vị trí enemy
        self.rect.y += self.dy  # Di chuyển xuống dưới

        # Nếu enemy ra khỏi màn hình, đánh dấu là đã chết
        if self.rect.y > self.screen_height:
            self.health = 0

    def shoot(self):
        # Phương thức bắn (hiện tại không được sử dụng)
        pass

    def draw(self, screen):
        # Vẽ enemy lên màn hình
        screen.blit(self.image, self.rect.topleft)

        # Vẽ các viên đạn của enemy
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

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
        drop_chance = 0.3 if self.level == 1 else 0.4  # Xác suất rơi vật phẩm
        if random.random() < drop_chance:
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