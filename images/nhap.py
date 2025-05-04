import pygame
import random
import time  


pygame.init()
screen = pygame.display.set_mode((1200,850))

#Title, icon
pygame.display.set_caption("Kẻ_cướp_không_gian")
icon = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\Logo.png")
pygame.display.set_icon(icon)
# Background
backgroundImg = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\background.jpg")
backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))

#Player
playerImg = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\arcade_space.png")
playerImg = pygame.transform.scale(playerImg, (100, 100))  
playerX = (1200 - 100) // 2  
playerY = 693  # Vị trí giữa khoảng (650 + 736) / 2
playerX_change = 0
playerY_change = 0
def player(x, y):
    screen.blit(playerImg, (x, y)) #chèn player vào

# Thêm biến quản lý thời gian và enemy
start_time = time.time()
wave_interval = 1  # Thời gian giữa các đợt enemy (2 giây)
last_wave_time = start_time
max_enemies = 5
current_enemies = []  # List chứa enemy đang active

# Thêm class Score để quản lý điểm số
class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(None, 36)
    
    def increase(self, points=10):
        self.value += points
    
    def draw(self, screen):
        score_text = self.font.render(f'Score: {self.value}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

# Sửa lại class Enemy để thêm thanh máu
class Enemy:
    def __init__(self):
        self.img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\ghost.png")
        self.img = pygame.transform.scale(self.img, (65, 65))
        self.reset_position()
        self.speed = 0.08
        self.active = True
        self.width = 65
        self.height = 65
        self.hitbox_width = 50  # Hitbox nhỏ hơn sprite một chút
        self.hitbox_height = 50
        self.health = 2  # Mỗi enemy có 2 máu
        
    def reset_position(self):
        # Kiểm tra vị trí của các enemy hiện có để tránh chồng lên nhau
        while True:
            self.x = random.randint(0, 1135)  # 1200 - 65 (kích thước enemy)
            self.y = random.randint(-100, -50)
            
            # Kiểm tra khoảng cách với các enemy khác
            valid_position = True
            for enemy in current_enemies:
                if enemy != self:  # Không so sánh với chính nó
                    distance_x = abs(self.x - enemy.x)
                    distance_y = abs(self.y - enemy.y)
                    if distance_x < 80 and distance_y < 80:  # Khoảng cách tối thiểu giữa các enemy
                        valid_position = False
                        break
            
            if valid_position:
                break

    def move(self):
        self.y += self.speed
        # Kiểm tra không cho enemy đi qua vạch trắng
        if self.y >= boundary_y - self.height:
            self.reset_position()

    def check_collision(self, bullet_x, bullet_y):
        # Tính toán vùng hitbox ở giữa enemy
        hitbox_x = self.x + (self.width - self.hitbox_width) // 2
        hitbox_y = self.y + (self.height - self.hitbox_height) // 2
        
        # Kiểm tra va chạm với hitbox đã được điều chỉnh
        if (bullet_x >= hitbox_x and 
            bullet_x <= hitbox_x + self.hitbox_width and
            bullet_y >= hitbox_y and 
            bullet_y <= hitbox_y + self.hitbox_height):
            return True
        return False

    def draw_health_bar(self, screen):
        bar_width = self.width
        bar_height = 5
        health_width = (self.health / 2) * bar_width  # 2 là máu tối đa
        
        # Vẽ thanh máu đỏ (nền)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x, self.y - 10, bar_width, bar_height))
        # Vẽ thanh máu xanh (máu hiện tại)
        pygame.draw.rect(screen, (0, 255, 0),
                        (self.x, self.y - 10, health_width, bar_height))

    def draw(self, screen):
        # Vẽ enemy
        screen.blit(self.img, (self.x, self.y))
        self.draw_health_bar(screen)
        
        # Debug: Vẽ hitbox để dễ nhìn (có thể xóa sau khi đã test xong)
        hitbox_x = self.x + (self.width - self.hitbox_width) // 2
        hitbox_y = self.y + (self.height - self.hitbox_height) // 2
        pygame.draw.rect(screen, (255, 0, 0), 
                        (hitbox_x, hitbox_y, self.hitbox_width, self.hitbox_height), 1)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0  # Trả về True nếu enemy bị tiêu diệt

# Thêm class GameLevel để quản lý độ khó
class GameLevel:
    def __init__(self):
        self.level = 1
        self.enemies_defeated = 0
        self.spawn_timer = 0
        
    def get_enemy_count(self):
        # Tăng số lượng enemy theo level, tối đa 4 con
        return min(self.level + 1, 4)
    
    def get_enemy_speed(self):
        # Tăng tốc độ enemy theo level
        return 0.08 + (self.level * 0.02)
    
    def increase_level(self):
        self.level += 1
        print(f"Level up! Current level: {self.level}")

# Trong phần khởi tạo game, thêm:
score = Score()
game_level = GameLevel()

#Bullet
bulletImg = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\bullet.png")
bulletX = 0
bulletY = 800
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 50 - 16, y - 10))

# Thêm class ComboSystem để làm game thú vị hơn
class ComboSystem:
    def __init__(self):
        self.combo_count = 0
        self.last_kill_time = 0
        self.combo_timeout = 2.0  # 2 giây để duy trì combo
        self.font = pygame.font.Font(None, 36)

    def add_kill(self, current_time):
        if current_time - self.last_kill_time < self.combo_timeout:
            self.combo_count += 1
        else:
            self.combo_count = 1
        self.last_kill_time = current_time
        return self.combo_count * 5  # Điểm thưởng tăng theo combo

    def draw(self, screen):
        if time.time() - self.last_kill_time < self.combo_timeout:
            combo_text = self.font.render(f'Combo x{self.combo_count}!', True, (255, 255, 0))
            screen.blit(combo_text, (10, 50))

# Thêm class FloatingText để hiển thị điểm khi tiêu diệt enemy
class FloatingText:
    def __init__(self, x, y, text, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 60
        self.font = pygame.font.Font(None, 24)

    def update(self):
        self.y -= 1
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.x, self.y))

# Khởi tạo các đối tượng mới
combo_system = ComboSystem()
floating_texts = []

#Game loop
running = True
#Âm thanh
shoot_sound = pygame.mixer.Sound(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\shoot.wav")#nhạc khi bắn
shoot_sound.set_volume(0.5)
pygame.mixer.music.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\background.mp3")
pygame.mixer.music.set_volume(1)  # Âm lượng: 30%
pygame.mixer.music.play(-1)         # Lặp vô hạn


while running:
    current_time = time.time()
    
    # Kiểm tra và tạo wave mới
    if current_time - last_wave_time >= wave_interval:
        if len(current_enemies) < game_level.get_enemy_count():
            new_enemy = Enemy()
            new_enemy.speed = game_level.get_enemy_speed()
            current_enemies.append(new_enemy)
            last_wave_time = current_time

    screen.blit(backgroundImg, (0, 0))

    # Vẽ đường kẻ trắng để phân định giới hạn
    boundary_y = 650  # Đặt giới hạn gần với vị trí ban đầu của player hơn
    pygame.draw.line(screen, (255, 255, 255), (0, boundary_y), (1200, boundary_y), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #điều khiển player bằng phím
        #Sang trái phải
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 1        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        #Lên xuống
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                 playerY_change -= 1
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_DOWN:
                 playerY_change = 1
        if event.type == pygame.KEYUP:
             if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                 playerY_change = 0
    
        #Bắn bằng phím space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    shoot_sound.stop()   # dừng âm cũ nếu đang chạy
                    shoot_sound.play()   # phát lại từ đầu
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
    
    playerX += playerX_change
    playerY += playerY_change

    #Boundary limit
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1100:
        playerX = 1100

    # Giới hạn player chỉ di chuyển bên dưới đường kẻ trắng
    if playerY <= boundary_y:  # Sử dụng biến boundary_y thay vì số cứng
        playerY = boundary_y
    elif playerY >= 736:
        playerY = 736

    # Bullet Movement và kiểm tra va chạm
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        
        # Tạo một biến để kiểm tra xem đạn đã va chạm chưa
        bullet_hit = False
        
        for enemy in current_enemies[:]:
            if not bullet_hit and enemy.check_collision(bulletX + 16, bulletY):  # +16 để lấy giữa đạn
                bullet_hit = True
                if enemy.take_damage():
                    # Tính điểm combo
                    bonus_points = combo_system.add_kill(current_time)
                    score.increase(10 + bonus_points)
                    
                    # Hiển thị điểm nổi
                    floating_texts.append(
                        FloatingText(
                            enemy.x, 
                            enemy.y, 
                            f"+{10 + bonus_points}", 
                            (255, 255, 0)
                        )
                    )
                    
                    game_level.enemies_defeated += 1
                    if game_level.enemies_defeated >= 5:
                        game_level.increase_level()
                        game_level.enemies_defeated = 0
                        floating_texts.append(
                            FloatingText(
                                600, 
                                425, 
                                f"LEVEL UP! {game_level.level}", 
                                (0, 255, 0)
                            )
                        )
                    
                    current_enemies.remove(enemy)
                
                bullet_state = "ready"
                bulletY = 800
                break

        if bulletY <= 0:
            bulletY = 800
            bullet_state = "ready"

    # Cập nhật và vẽ enemies
    for enemy in current_enemies:
        enemy.move()
        if enemy.y < boundary_y:
            enemy.draw(screen)

    # Vẽ điểm số
    score.draw(screen)

    # Cập nhật và vẽ floating texts
    floating_texts = [text for text in floating_texts if text.update()]
    for text in floating_texts:
        text.draw(screen)

    # Vẽ combo
    combo_system.draw(screen)

    player(playerX, playerY)
    pygame.display.update()