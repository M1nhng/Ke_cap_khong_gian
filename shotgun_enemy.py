import pygame
import random
import math
from items import Item, ITEM_TYPES

class ShotgunEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thông số cơ bản của ShotgunEnemy
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Cấp độ hiện tại của game

        # Tải và scale hình ảnh enemy (robot.png)
        try:
            self.image = pygame.image.load('D:/Python/Game/images/robot.png')
            self.image = pygame.transform.scale(self.image, (100, 100))
        except pygame.error as e:
            print(f"Error loading robot.png: {e}")
            self.image = pygame.Surface((100, 100))  # Hình ảnh mặc định nếu không tải được
            self.image.fill((255, 0, 0))  # Màu đỏ để dễ nhận biết lỗi
        self.rect = self.image.get_rect()

        # Đặt vị trí ban đầu ngẫu nhiên ở phía trên
        self.rect.x = random.randint(100, screen_width - 100)
        self.rect.y = 100  # Vị trí cố định để lơ lửng ở trên

        # Tốc độ di chuyển ngang để lơ lửng
        self.horizontal_speed = 1  # Tốc độ dao động ngang
        self.direction = random.choice(['left', 'right'])
        self.dx = -self.horizontal_speed if self.direction == 'left' else self.horizontal_speed

        # Máu của enemy (cao hơn BombEnemy)
        self.health = 15 + level * 3

        # Thiết lập bắn đạn
        self.shoot_timer = 0
        self.shoot_cooldown = 300  # Thời gian chờ giữa các lần bắn
        self.bullet_speed = 1  # Tốc độ đạn
        self.bullets = []  # Danh sách đạn

        self.player_pos = player_pos  # Vị trí của người chơi

    def update(self):
        # Cập nhật vị trí enemy (dao động ngang, giữ y cố định)
        print(f"ShotgunEnemy updating: dx={self.dx}, pos={self.rect.topleft}")  # Debug log
        self.rect.x += self.dx

        # Xử lý va chạm với biên màn hình
        if self.rect.right > self.screen_width:
            self.dx = -abs(self.horizontal_speed)  # Đổi hướng sang trái
            self.rect.right = self.screen_width
            print(f"ShotgunEnemy hit right wall, new dx={self.dx}")
        elif self.rect.left < 0:
            self.dx = abs(self.horizontal_speed)  # Đổi hướng sang phải
            self.rect.left = 0
            print(f"ShotgunEnemy hit left wall, new dx={self.dx}")

        # Cập nhật thời gian bắn
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            # Bắn 3 viên đạn với góc ngẫu nhiên
            player_x, player_y = self.player_pos()
            for i in range(3):
                angle = math.atan2(player_y - self.rect.y, player_x - self.rect.x) + random.uniform(-0.4, 0.4)
                dx = math.cos(angle) * self.bullet_speed
                dy = math.sin(angle) * self.bullet_speed
                self.bullets.append({'x': self.rect.x + 40, 'y': self.rect.y + 50, 'dx': dx, 'dy': dy})

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
        if abs(bullet_x - self.rect.centerx) < 40 and abs(bullet_y - self.rect.centery) < 50:
            self.health -= 1  # Giảm máu khi bị trúng
            return True
        return False

    def is_dead(self):
        # Kiểm tra xem enemy có chết không
        return self.health <= 0

    def drop_item(self):
        # Xử lý rơi vật phẩm khi enemy chết (50% cơ hội)
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