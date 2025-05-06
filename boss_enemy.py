import pygame
import random
import math

class BossEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thông số cơ bản của BossEnemy
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Cấp độ hiện tại của game

        # Tải và scale hình ảnh boss (boss.png)
        self.image = pygame.image.load('D:/Python/Game/images/boss.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()

        # Đặt vị trí ban đầu ở giữa phía trên màn hình
        self.rect.x = (screen_width - self.rect.width) // 2
        self.rect.y = 0

        # Tốc độ di chuyển
        self.speed = 0.5

        # Máu của boss (tăng theo level)
        self.health = 50 + level * 5

        # Thiết lập chế độ chiến đấu
        self.mode = 1  # Chế độ 1: Bắn đạn, Chế độ 2: Laser
        self.mode_timer = 0
        self.mode_switch_time = 10 * 240  # Thời gian chuyển đổi chế độ

        # Thiết lập bắn đạn
        self.shoot_timer = 0
        self.bullet_speed = 2.0  # Tốc độ đạn
        self.bullets = []  # Danh sách đạn

        self.player_pos = player_pos  # Vị trí của người chơi

        # Thiết lập laser
        self.laser_width = screen_width // 5  # Chiều rộng laser
        self.laser_left_x = random.randint(100, screen_width - 2 * self.laser_width - 100)  # Vị trí laser trái
        self.laser_right_x = self.laser_left_x + self.laser_width + 100  # Vị trí laser phải
        self.laser_left_center = self.laser_left_x + self.laser_width // 2
        self.laser_right_center = self.laser_right_x + self.laser_width // 2
        self.laser_timer = 0
        self.laser_warning_time = 3 * 240  # Thời gian cảnh báo laser
        self.laser_active = False  # Trạng thái laser
        self.laser_narrow_speed = 0.5  # Tốc độ thu hẹp laser
        self.boundary_y = 850  # Chiều cao laser
        self.laser_duration = 7 * 240  # Thời gian tồn tại laser

    def update(self):
        # Cập nhật vị trí boss
        if self.rect.y < 100:
            self.rect.y += self.speed  # Di chuyển xuống đến y=100

        # Cập nhật chế độ chiến đấu
        self.mode_timer += 1
        if self.mode_timer >= self.mode_switch_time:
            self.mode = 2 if self.mode == 1 else 1  # Chuyển đổi chế độ
            self.mode_timer = 0
            if self.mode == 2:
                # Khởi tạo lại laser
                self.laser_width = self.screen_width // 5
                self.laser_left_x = random.randint(100, self.screen_width - 2 * self.laser_width - 100)
                self.laser_right_x = self.laser_left_x + self.laser_width + 100
                self.laser_left_center = self.laser_left_x + self.laser_width // 2
                self.laser_right_center = self.laser_right_x + self.laser_width // 2
                self.laser_timer = 0
                self.laser_active = False

        # Cập nhật thời gian bắn
        self.shoot_timer += 1
        if self.mode == 1:
            # Chế độ bắn đạn
            if self.shoot_timer >= 60:
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
        elif self.mode == 2:
            # Chế độ laser
            self.laser_timer += 1
            if self.laser_timer < self.laser_warning_time:
                # Giai đoạn cảnh báo
                pass
            elif self.laser_timer < self.laser_duration:
                # Giai đoạn laser hoạt động
                self.laser_active = True
                self.laser_width -= self.laser_narrow_speed * 2  # Thu hẹp laser
                if self.laser_width < 50:
                    self.laser_width = 50  # Giới hạn chiều rộng tối thiểu
                self.laser_left_x = self.laser_left_center - self.laser_width // 2
                self.laser_right_x = self.laser_right_center - self.laser_width // 2
                if self.shoot_timer >= 10:
                    self.shoot_timer = 0
                    # Bắn đạn từ laser
                    for laser_x in [self.laser_left_x + self.laser_width // 2, self.laser_right_x + self.laser_width // 2]:
                        self.bullets.append({
                            'x': laser_x,
                            'y': 100,
                            'dx': 0,
                            'dy': self.bullet_speed
                        })
            else:
                # Kết thúc laser, khởi tạo lại
                self.laser_active = False
                self.laser_timer = 0
                self.laser_width = self.screen_width // 5
                self.laser_left_x = random.randint(100, self.screen_width - 2 * self.laser_width - 100)
                self.laser_right_x = self.laser_left_x + self.laser_width + 100
                self.laser_left_center = self.laser_left_x + self.laser_width // 2
                self.laser_right_center = self.laser_right_x + self.laser_width // 2

        # Cập nhật vị trí các viên đạn
        for b in self.bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            # Xóa đạn nếu ra khỏi màn hình
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def draw(self, screen):
        # Vẽ boss lên màn hình
        screen.blit(self.image, self.rect.topleft)

        # Vẽ các viên đạn của boss
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

        # Vẽ laser
        if self.mode == 2 and self.laser_timer < self.laser_duration:
            color = (255, 0, 0, 128) if self.laser_timer < self.laser_warning_time else (255, 0, 0)
            pygame.draw.rect(screen, color, (self.laser_left_x, 0, self.laser_width, self.boundary_y), 2 if self.laser_timer < self.laser_warning_time else 0)
            pygame.draw.rect(screen, color, (self.laser_right_x, 0, self.laser_width, self.boundary_y), 2 if self.laser_timer < self.laser_warning_time else 0)

    def hit_by(self, bullet_x, bullet_y):
        # K подъpytorchKiểm tra xem boss có bị trúng đạn không
        if abs(bullet_x - self.rect.centerx) < 75 and abs(bullet_y - self.rect.centery) < 75:
            if self.mode == 1:
                return False  # Không nhận sát thương ở chế độ 1
            self.health -= 1  # Giảm máu khi bị trúng ở chế độ 2
            return True
        return False

    def reflect_bullet(self, bullet_x, bullet_y):
        # Kiểm tra xem boss có phản xạ đạn không
        if self.mode == 1 and abs(bullet_x - self.rect.centerx) < 75 and abs(bullet_y - self.rect.centery) < 75:
            return True
        return False

    def is_dead(self):
        # Kiểm tra xem boss có chết không
        return self.health <= 0