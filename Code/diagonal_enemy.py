# import pygame
# import random
# import math
# from items import Item, ITEM_TYPES

# class DiagonalEnemy:
#     def __init__(self, level, screen_width, screen_height, player_pos):
#         # Khởi tạo thông số cơ bản của DiagonalEnemy
#         self.screen_width = screen_width  # Chiều rộng màn hình
#         self.screen_height = screen_height  # Chiều cao màn hình
#         self.level = level  # Cấp độ hiện tại của game

#         # Tải và scale hình ảnh enemy (enemy_cheo.png)
#         try:
#             self.image = pygame.image.load('D:/Python/Game/images/enemy_cheo.png')
#             self.image = pygame.transform.scale(self.image, (65, 65))
#         except pygame.error as e:
#             print(f"Error loading enemy_cheo.png: {e}")
#             self.image = pygame.Surface((65, 65))
#             self.image.fill((255, 0, 0))  # Hình chữ nhật đỏ để debug
#         self.rect = self.image.get_rect()

#         # Đặt vị trí ban đầu ngẫu nhiên trong màn hình
#         self.rect.x = random.randint(50, screen_width - 50)
#         self.rect.y = 50  # Đặt trong màn hình để kiểm tra

#         # Xác định hướng di chuyển ngẫu nhiên (trái hoặc phải)
#         self.direction = random.choice(['left', 'right'])
#         self.dx = -0.3 if self.direction == 'left' else 0.3  # Vận tốc theo trục x (tăng để rõ hơn)
#         self.dy = 0.3  # Vận tốc theo trục y (tăng để rõ hơn)

#         # Máu của enemy
#         self.health = 1

#         # Danh sách đạn của enemy
#         self.bullets = []
#         self.player_pos = player_pos  # Vị trí của người chơi

#     def update(self):
#         # Cập nhật vị trí enemy
#         print(f"DiagonalEnemy updating: dx={self.dx}, dy={self.dy}, pos={self.rect.topleft}")  # Debug log
#         self.rect.x += self.dx  # Di chuyển theo trục x
#         self.rect.y += self.dy  # Di chuyển theo trục y

#         # Xử lý va chạm với biên màn hình
#         if self.rect.right > self.screen_width:
#             self.dx = -abs(self.dx)  # Đổi hướng sang trái
#             self.rect.right = self.screen_width
#             print(f"DiagonalEnemy hit right wall, new dx={self.dx}")
#         elif self.rect.left < 0:
#             self.dx = abs(self.dx)  # Đổi hướng sang phải
#             self.rect.left = 0
#             print(f"DiagonalEnemy hit left wall, new dx={self.dx}")

#         # Nếu enemy ra khỏi màn hình, đánh dấu là đã chết
#         if self.rect.y > self.screen_height:
#             self.health = 0

#     def draw(self, screen):
#         # Vẽ enemy lên màn hình
#         screen.blit(self.image, self.rect.topleft)

#         # Vẽ các viên đạn của enemy
#         for b in self.bullets:
#             pygame.draw.circle(screen, (255, 0, 0), (int(b['x']), int(b['y'])), 5)

#     def hit_by(self, bullet_x, bullet_y):
#         # Kiểm tra xem enemy có bị trúng đạn không
#         bullet_rect = pygame.Rect(bullet_x, bullet_y, 34, 34)
#         if self.rect.colliderect(bullet_rect):
#             self.health -= 1  # Giảm máu khi bị trúng
#             return True
#         return False

#     def is_dead(self):
#         # Kiểm tra xem enemy có chết không
#         return self.health <= 0

#     def drop_item(self):
#         # Xử lý rơi vật phẩm khi enemy chết
#         item_type = random.choice(ITEM_TYPES)  # Chọn ngẫu nhiên loại vật phẩm
#         radius = 50  # Bán kính sinh vật phẩm
#         angle = random.uniform(0, 2 * math.pi)  # Góc ngẫu nhiên
#         offset_x = math.cos(angle) * random.uniform(0, radius)  # Offset x
#         offset_y = math.sin(angle) * random.uniform(0, radius)  # Offset y
#         spawn_x = self.rect.centerx + offset_x  # Vị trí x của vật phẩm
#         spawn_y = self.rect.centery + offset_y  # Vị trí y của vật phẩm
#         player_x, player_y = self.player_pos()  # Lấy vị trí người chơi
#         return Item(spawn_x, spawn_y, item_type, player_x, player_y)  # Tạo vật phẩm