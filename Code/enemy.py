import pygame
import random
import math

class Enemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level

        # Load và chỉnh kích thước ảnh kẻ địch
        self.image = pygame.image.load('D:/Python/Game/images/ghost.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()  # Hình chữ nhật để định vị và va chạm

        # Spawn địch từ bên trái hoặc phải màn hình
        self.spawn_side = random.choice(['left', 'right'])
        self.rect.y = random.randint(100, screen_height // 2)  # Tọa độ Y ngẫu nhiên ở nửa trên
        self.rect.x = -100 if self.spawn_side == 'left' else screen_width + 100  # Ngoài màn hình

        # Xác định vị trí mục tiêu enemy sẽ bay tới
        self.target_x = random.randint(200, screen_width - 200)
        self.target_y = self.rect.y # + random.randint(100, 200) Nếu muốn đi chéo thì cộng thêm
        self.speed = 1.5 + level * 0.1  # Tốc độ tăng theo level
        self.health = 1 + level // 2    # Máu tăng theo level
        self.stop_moving = False        # Khi nào đến mục tiêu thì dừng

        # Các thuộc tính liên quan đến bắn đạn
        self.shoot_cooldown = 90 - level * 5  # Thời gian giữa các lần bắn (cấp cao bắn nhanh hơn)
        self.shoot_timer = 0  # Đếm thời gian để bắn
        self.bullets = []     # Danh sách đạn đã bắn ra
        self.bullet_speed = 0.1 + level * 0.2  # Tốc độ viên đạn
        self.player_pos = player_pos  # Hàm trả về vị trí người chơi (dùng khi ngắm bắn)

    def update(self):
        # Nếu chưa đến mục tiêu → tiếp tục di chuyển
        if not self.stop_moving:
            dx = self.target_x - self.rect.x
            dy = self.target_y - self.rect.y
            dist = math.hypot(dx, dy)  # Tính khoảng cách đến điểm đích

            if dist < 5:
                self.stop_moving = True  # Khi tới đủ gần thì dừng lại
            else:
                dx /= dist  # Chuẩn hóa hướng
                dy /= dist
                self.rect.x += dx * self.speed  # Di chuyển theo hướng đã chuẩn hóa
                self.rect.y += dy * self.speed
        else:
            # Khi dừng lại → bắt đầu bắn sau mỗi khoảng thời gian
            self.shoot_timer += 0.3
            if self.shoot_timer >= self.shoot_cooldown:
                self.shoot_timer = 0
                self.shoot()

        # Cập nhật vị trí đạn đã bắn ra
        for b in self.bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            # Xóa đạn nếu ra khỏi màn hình
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def shoot(self):
        # Bắn đạn theo chiều thẳng đứng xuống
        bullet = {
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'dx': 0,  # Không di chuyển theo x
            'dy': self.bullet_speed  # Di chuyển xuống dưới
        }
        self.bullets.append(bullet)

    def draw(self, screen):
        # Vẽ kẻ địch
        screen.blit(self.image, self.rect.topleft)
        # Vẽ các viên đạn
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        # Tạo rect cho đạn (kích thước 34x34, như trong lớp Bullet)
        bullet_rect = pygame.Rect(bullet_x, bullet_y, 34, 34)
        # Kiểm tra va chạm với rect của kẻ thù
        if self.rect.colliderect(bullet_rect):
            self.health -= 1
            return True
        return False

    def is_dead(self):
        return self.health <= 0

