import pygame
import random
import math

# Class đại diện cho enemy cơ bản với hành vi di chuyển và bắn đạn
class Enemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo các thuộc tính cơ bản của enemy
        self.screen_width = screen_width  # Chiều rộng màn hình game
        self.screen_height = screen_height  # Chiều cao màn hình game
        self.level = level  # Level hiện tại, ảnh hưởng đến tốc độ và sức khỏe
        # Tải và scale hình ảnh enemy (ghost.png) về kích thước 65x65
        self.image = pygame.image.load('D:/Python/Game/images/ghost.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()  # Tạo hình chữ nhật để quản lý vị trí và va chạm
        # Chọn ngẫu nhiên phía xuất hiện (trái hoặc phải)
        self.spawn_side = random.choice(['left', 'right'])
        # Đặt vị trí Y ngẫu nhiên trong nửa trên màn hình
        self.rect.y = random.randint(100, screen_height // 2)
        # Đặt vị trí X ngoài màn hình (bên trái hoặc phải)
        self.rect.x = -100 if self.spawn_side == 'left' else screen_width + 100
        # Đặt mục tiêu di chuyển ngẫu nhiên trong khoảng X hợp lệ
        self.target_x = random.randint(200, screen_width - 200)
        self.target_y = self.rect.y  # Mục tiêu Y giống vị trí xuất hiện ban đầu
        self.speed = 1.5 + level * 0.1  # Tốc độ di chuyển, tăng theo level
        self.health = 1 + level // 2  # Sức khỏe, tăng mỗi 2 level
        self.stop_moving = False  # Cờ để dừng di chuyển khi đến mục tiêu
        self.shoot_cooldown = 90 - level * 5  # Thời gian chờ giữa các lần bắn, giảm theo level
        self.shoot_timer = 0  # Bộ đếm thời gian để kiểm soát bắn
        self.bullets = []  # Danh sách chứa các viên đạn của enemy
        self.bullet_speed = 0.1 + level * 0.2  # Tốc độ đạn, tăng theo level
        self.player_pos = player_pos  # Hàm trả về vị trí người chơi (chưa sử dụng trong class này)

    def update(self):
        # Cập nhật trạng thái và vị trí của enemy
        if not self.stop_moving:
            # Di chuyển đến vị trí mục tiêu nếu chưa dừng
            dx = self.target_x - self.rect.x  # Khoảng cách X đến mục tiêu
            dy = self.target_y - self.rect.y  # Khoảng cách Y đến mục tiêu
            dist = math.hypot(dx, dy)  # Tính khoảng cách Euclidean
            if dist < 5:
                # Dừng di chuyển nếu đã gần mục tiêu (khoảng cách < 5)
                self.stop_moving = True
            else:
                # Chuẩn hóa vector hướng và di chuyển
                dx /= dist
                dy /= dist
                self.rect.x += dx * self.speed  # Cập nhật vị trí X
                self.rect.y += dy * self.speed  # Cập nhật vị trí Y
        else:
            # Nếu đã dừng, xử lý bắn đạn
            self.shoot_timer += 0.3  # Tăng bộ đếm (điều chỉnh theo tốc độ khung hình)
            if self.shoot_timer >= self.shoot_cooldown:
                self.shoot_timer = 0  # Reset bộ đếm
                self.shoot()  # Gọi hàm bắn
        # Cập nhật vị trí các viên đạn
        for b in self.bullets[:]:
            b['x'] += b['dx']  # Di chuyển đạn theo hướng X
            b['y'] += b['dy']  # Di chuyển đạn theo hướng Y
            # Xóa đạn nếu ra ngoài màn hình
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def shoot(self):
        # Tạo một viên đạn di chuyển thẳng xuống dưới
        bullet = {
            'x': self.rect.centerx,  # Vị trí X bắt đầu từ tâm enemy
            'y': self.rect.centery,  # Vị trí Y bắt đầu từ tâm enemy
            'dx': 0,  # Không di chuyển ngang
            'dy': self.bullet_speed  # Di chuyển xuống với tốc độ bullet_speed
        }
        self.bullets.append(bullet)  # Thêm đạn vào danh sách

    def draw(self, screen):
        # Vẽ enemy và các viên đạn của nó lên màn hình
        screen.blit(self.image, self.rect.topleft)  # Vẽ hình ảnh enemy
        for b in self.bullets:
            # Vẽ mỗi viên đạn là một hình tròn màu đỏ
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        # Kiểm tra xem enemy có bị trúng đạn của người chơi không
        if abs(bullet_x - self.rect.centerx) < 30 and abs(bullet_y - self.rect.centery) < 30:
            self.health -= 1  # Giảm sức khỏe nếu bị trúng
            return True  # Xác nhận bị trúng
        return False  # Không bị trúng

    def is_dead(self):
        # Kiểm tra xem enemy đã chết chưa (sức khỏe <= 0)
        return self.health <= 0

# Class đại diện cho enemy di chuyển chéo và bật lại khi chạm biên
class DiagonalEnemy(Enemy):
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Kế thừa từ class Enemy
        super().__init__(level, screen_width, screen_height, player_pos)
        # Ghi đè vị trí xuất hiện: ngẫu nhiên trên đầu màn hình
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -100
        # Chọn hướng di chuyển chéo (trái xuống hoặc phải xuống)
        self.direction = random.choice(['left', 'right'])
        self.dx = -0.5 if self.direction == 'left' else 0.5  # Tốc độ ngang
        self.dy = 0.5  # Tốc độ dọc (luôn xuống)
        self.speed = 1.5 + level * 0.1  # Tốc độ tổng, giống Enemy cơ bản
        self.health = 1 + level // 2  # Sức khỏe, giống Enemy cơ bản
        self.stop_moving = False  # Luôn di chuyển, không dừng

    def update(self):
        # Cập nhật vị trí với chuyển động chéo
        self.rect.x += self.dx * self.speed  # Di chuyển ngang
        self.rect.y += self.dy * self.speed  # Di chuyển dọc
        # Đổi hướng ngang khi chạm biên màn hình
        if self.rect.right > self.screen_width:
            self.dx = -abs(self.dx)  # Quay sang trái
            self.rect.right = self.screen_width  # Ngăn vượt biên
        elif self.rect.left < 0:
            self.dx = abs(self.dx)  # Quay sang phải
            self.rect.left = 0  # Ngăn vượt biên
        # Đánh dấu là chết nếu ra khỏi đáy màn hình
        if self.rect.y > self.screen_height:
            self.health = 0

    def shoot(self):
        # Vô hiệu hóa bắn đạn (DiagonalEnemy không bắn)
        pass

# Class đại diện cho enemy mạnh với khả năng bắn nhiều đạn theo hướng người chơi
class ShotgunEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thuộc tính
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Level hiện tại
        # Tải và scale hình ảnh (robot.png) về kích thước 100x100
        self.image = pygame.image.load('D:/Python/Game/images/robot.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()  # Tạo hình chữ nhật cho vị trí
        # Xuất hiện ngẫu nhiên ở phía trên màn hình
        self.rect.x = random.randint(100, screen_width - 100)
        self.rect.y = -200
        self.speed = 0.3 + (level - 1) * 0.04  # Tốc độ di chuyển, tăng nhẹ theo level
        self.health = 10 + level * 2  # Sức khỏe cao, tăng theo level
        self.shoot_timer = 0  # Bộ đếm thời gian bắn
        self.bullet_speed = 1.5  # Tốc độ đạn cố định
        self.bullets = []  # Danh sách chứa đạn
        self.player_pos = player_pos  # Hàm trả về vị trí người chơi

    def update(self):
        # Cập nhật vị trí và hành vi bắn
        self.rect.y += self.speed  # Di chuyển xuống dưới
        self.shoot_timer += 1  # Tăng bộ đếm bắn
        if self.shoot_timer >= 120:
            self.shoot_timer = 0  # Reset bộ đếm
            player_x, player_y = self.player_pos()  # Lấy vị trí người chơi
            # Bắn 3 viên đạn với góc ngẫu nhiên quanh hướng người chơi
            for i in range(3):
                angle = math.atan2(player_y - self.rect.y, player_x - self.rect.x) + random.uniform(-0.4, 0.4)
                dx = math.cos(angle) * self.bullet_speed  # Tốc độ ngang của đạn
                dy = math.sin(angle) * self.bullet_speed  # Tốc độ dọc của đạn
                self.bullets.append({'x': self.rect.x + 40, 'y': self.rect.y + 50, 'dx': dx, 'dy': dy})
        # Cập nhật vị trí đạn
        for b in self.bullets[:]:
            b['x'] += b['dx']  # Di chuyển đạn ngang
            b['y'] += b['dy']  # Di chuyển đạn dọc
            # Xóa đạn nếu ra ngoài màn hình
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def draw(self, screen):
        # Vẽ enemy và đạn lên màn hình
        screen.blit(self.image, self.rect.topleft)  # Vẽ hình ảnh enemy
        for b in self.bullets:
            # Vẽ đạn là hình tròn đỏ
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)

    def hit_by(self, bullet_x, bullet_y):
        # Kiểm tra va chạm với đạn người chơi
        if abs(bullet_x - self.rect.centerx) < 40 and abs(bullet_y - self.rect.centery) < 50:
            self.health -= 1  # Giảm sức khỏe
            return True  # Xác nhận bị trúng
        return False  # Không bị trúng

    def is_dead(self):
        # Kiểm tra xem enemy đã chết chưa
        return self.health <= 0

# Class đại diện cho enemy đặc biệt với khả năng dịch chuyển và lao vào người chơi
class ShadowEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        # Khởi tạo thuộc tính
        self.screen_width = screen_width  # Chiều rộng màn hình
        self.screen_height = screen_height  # Chiều cao màn hình
        self.level = level  # Level hiện tại
        # Tải và scale hình ảnh (devil.png) về kích thước 65x65
        self.image = pygame.image.load('D:/Python/Game/images/devil.png')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()  # Tạo hình chữ nhật cho vị trí
        # Xuất hiện ngẫu nhiên trên màn hình
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = random.randint(50, screen_height - 50)
        self.speed = 2.0 + level * 0.1  # Tốc độ cao, tăng theo level
        self.health = 2 + level // 2  # Sức khỏe, nhỉnh hơn Enemy cơ bản
        self.timer = 0  # Bộ đếm thời gian tồn tại
        self.charge_time = 7 * 240  # 7 giây tại 240 FPS để bắt đầu lao vào người chơi
        self.is_charging = False  # Cờ để kiểm soát trạng thái lao vào
        self.player_pos = player_pos  # Hàm trả về vị trí người chơi

    def teleport(self):
        # Dịch chuyển ngẫu nhiên đến vị trí mới trên màn hình
        self.rect.x = random.randint(50, self.screen_width - 50)
        self.rect.y = random.randint(50, self.screen_height - 50)

    def update(self):
        # Cập nhật trạng thái và hành vi
        if not self.is_charging:
            self.timer += 1  # Tăng bộ đếm thời gian
            if self.timer >= self.charge_time:
                self.is_charging = True  # Chuyển sang trạng thái lao vào sau 7 giây
        else:
            # Lao thẳng đến vị trí người chơi
            player_x, player_y = self.player_pos()  # Lấy vị trí người chơi
            dx = player_x - self.rect.centerx  # Khoảng cách X đến người chơi
            dy = player_y - self.rect.centery  # Khoảng cách Y đến người chơi
            dist = math.hypot(dx, dy)  # Tính khoảng cách
            if dist > 5:
                # Di chuyển nếu chưa quá gần người chơi
                dx /= dist  # Chuẩn hóa vector hướng
                dy /= dist
                self.rect.x += dx * self.speed  # Cập nhật vị trí X
                self.rect.y += dy * self.speed  # Cập nhật vị trí Y

    def draw(self, screen):
        # Vẽ enemy lên màn hình
        screen.blit(self.image, self.rect.topleft)

    def hit_by(self, bullet_x, bullet_y):
        # Kiểm tra va chạm với đạn người chơi
        if abs(bullet_x - self.rect.centerx) < 30 and abs(bullet_y - self.rect.centery) < 30:
            self.health -= 1  # Giảm sức khỏe
            if not self.is_dead():
                self.teleport()  # Dịch chuyển nếu chưa chết
            return True  # Xác nhận bị trúng
        return False  # Không bị trúng

    def is_dead(self):
        # Kiểm tra xem enemy đã chết chưa
        return self.health <= 0

# Class đại diện cho boss với hai chế độ bắn đặc biệt
class BossEnemy:
    def __init__(self, level, screen_width, screen_height, player_pos):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        # Tải và scale hình ảnh boss
        self.image = pygame.image.load('D:/Python/Game/images/boss.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        # Xuất hiện ở giữa đỉnh màn hình
        self.rect.x = (screen_width - self.rect.width) // 2
        self.rect.y = 0
        self.speed = 0.5  # Tốc độ di chuyển xuống
        self.health = 50 + level * 5  # Sức khỏe cao
        self.mode = 1  # Bắt đầu ở chế độ 1
        self.mode_timer = 0
        self.mode_switch_time = 10 * 240  # 10 giây tại 240 FPS
        self.shoot_timer = 0
        self.bullet_speed = 2.0
        self.bullets = []
        self.player_pos = player_pos
        # Laser cho chế độ 2
        self.laser_width = screen_width // 5  # 240px
        self.laser_left_x = random.randint(100, screen_width - 2 * self.laser_width - 100)
        self.laser_right_x = self.laser_left_x + self.laser_width + 100
        self.laser_timer = 0
        self.laser_warning_time = 3 * 240  # 3 giây cảnh báo
        self.laser_active = False
        self.laser_narrow_speed = 0.5  # Tốc độ thu hẹp laser
        self.boundary_y = 650

    def update(self):
        # Di chuyển xuống cho đến khi đạt y = 100
        if self.rect.y < 100:
            self.rect.y += self.speed
        # Cập nhật chế độ
        self.mode_timer += 1
        if self.mode_timer >= self.mode_switch_time:
            self.mode = 2 if self.mode == 1 else 1
            self.mode_timer = 0
            if self.mode == 2:
                # Reset laser cho chế độ 2
                self.laser_left_x = random.randint(100, self.screen_width - 2 * self.laser_width - 100)
                self.laser_right_x = self.laser_left_x + self.laser_width + 100
                self.laser_timer = 0
                self.laser_active = False

        # Xử lý bắn
        self.shoot_timer += 1
        if self.mode == 1:
            if self.shoot_timer >= 60:  # Bắn mỗi 0.25s
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
            if self.laser_timer >= self.laser_warning_time:
                self.laser_active = True
                # Thu hẹp laser
                self.laser_left_x += self.laser_narrow_speed
                self.laser_right_x -= self.laser_narrow_speed
                # Giữ laser trong giới hạn
                if self.laser_right_x - self.laser_left_x < 50:
                    self.laser_right_x = self.laser_left_x + 50
                # Bắn đạn từ laser
                if self.shoot_timer >= 10:  # Bắn nhanh
                    self.shoot_timer = 0
                    for laser_x in [self.laser_left_x + self.laser_width // 2, self.laser_right_x + self.laser_width // 2]:
                        self.bullets.append({
                            'x': laser_x,
                            'y': 100,
                            'dx': 0,
                            'dy': self.bullet_speed
                        })

        # Cập nhật đạn
        for b in self.bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            if b['y'] > self.screen_height or b['x'] < 0 or b['x'] > self.screen_width:
                self.bullets.remove(b)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # Vẽ đạn
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)
        # Vẽ laser ở chế độ 2
        if self.mode == 2:
            color = (255, 0, 0, 128) if self.laser_timer < self.laser_warning_time else (255, 0, 0)
            pygame.draw.rect(screen, color, (self.laser_left_x, 0, self.laser_width, self.boundary_y), 2 if self.laser_timer < self.laser_warning_time else 0)
            pygame.draw.rect(screen, color, (self.laser_right_x, 0, self.laser_width, self.boundary_y), 2 if self.laser_timer < self.laser_warning_time else 0)

    def hit_by(self, bullet_x, bullet_y):
        if abs(bullet_x - self.rect.centerx) < 75 and abs(bullet_y - self.rect.centery) < 75:
            if self.mode == 1:
                return False  # Phản xạ đạn
            self.health -= 1
            return True
        return False

    def reflect_bullet(self, bullet_x, bullet_y):
        if self.mode == 1 and abs(bullet_x - self.rect.centerx) < 75 and abs(bullet_y - self.rect.centery) < 75:
            return True
        return False

    def is_dead(self):
        return self.health <= 0
