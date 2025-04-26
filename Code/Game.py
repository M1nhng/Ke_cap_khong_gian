import pygame  # Thư viện game
import random  # Thư viện random
import math    # Thư viện toán học
from Menu import show_menu  # Hàm hiện menu
from items import Item, check_collision_and_apply  # Class Item và hàm check item
from player import Player  # Class người chơi

def run_game():
    pygame.init()  # Khởi tạo pygame
    screen = pygame.display.set_mode((1200, 850))  # Tạo màn hình 1200x850
    pygame.display.set_caption("Kẻ_cướp_không_gian")  # Đặt tên cửa sổ

    icon = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\Logo.png")  # Load icon
    pygame.display.set_icon(icon)  # Đặt icon

    backgroundImg = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\background.jpg")  # Load background
    backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))  # Resize background

    player = Player(550, 693)  # Tạo nhân vật ở vị trí (550, 693)
    bullets = []  # Danh sách đạn người chơi
    bulletImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\bullet.png"), (34, 34))  # Load và resize hình viên đạn

    enemyImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\ghost.png"), (65, 65))  # Load và resize hình địch thường

    bossImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\favicon.png"), (100, 100))  # Load và resize hình boss

    boss_bullets = []  # Danh sách đạn của boss
    boss_bullet_speed = 1.5  # Tốc độ đạn boss

    enemies = []  # Danh sách quái thường
    bosses = []  # Danh sách boss
    items = []  # Danh sách item rơi ra
    move_direction = {'left': False, 'right': False, 'up': False, 'down': False}  # Trạng thái di chuyển người chơi

    running = True  # Biến kiểm soát vòng lặp game
    clock = pygame.time.Clock()  # Đồng hồ game để FPS ổn định
    boundary_y = 650  # Biên giới để xóa địch

    level = 1  # Level hiện tại
    level_timer = 0  # Đồng hồ tính thời gian qua level
    level_duration = 3000  # Thời gian mỗi level
    max_level = 5  # Level tối đa
    spawn_delay = 240  # Thời gian delay spawn enemy
    spawn_counter = 0  # Counter để spawn enemy
    spawned_this_level = 0  # Số lượng spawn trong level hiện tại
    score = 0  # Điểm số
    font = pygame.font.SysFont(None, 36)  # Font chữ

    def draw_text(text, x, y, color=(255, 255, 255)):  # Hàm vẽ chữ
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def fire_bullet():  # Hàm bắn đạn
        if player.triple_shot_timer > 0:  # Nếu có buff bắn 3 viên
            for dx in [-2, 0, 2]:
                bullets.append({'x': player.x + player.width // 2 - bulletImg.get_width() // 2,
                                'y': player.y, 'dx': dx, 'dy': -5})
        else:  # Nếu bắn thường
            bullets.append({'x': player.x + player.width // 2 - bulletImg.get_width() // 2,
                            'y': player.y, 'dx': 0, 'dy': -5})

    def spawn_enemy(level):  # Hàm tạo enemy mới
        health = 1 + level // 2  # Máu enemy theo level
        speed = min(0.25 + (level - 1) * 0.06, 1.2)  # Tốc độ enemy theo level
        return {'x': random.randint(50, 1150), 'y': -random.randint(100, 300), 'speed': speed, 'health': health}

    def spawn_boss(level):  # Hàm tạo boss mới
        health = 10 + level * 2  # Máu boss theo level
        speed = min(0.3 + (level - 1) * 0.04, 0.8)  # Tốc độ boss theo level
        return {'x': random.randint(100, 1100), 'y': -200, 'speed': speed, 'health': health, 'shoot_timer': 0}

    while running:  # Vòng lặp chính của game
        screen.blit(backgroundImg, (0, 0))  # Vẽ background

        for event in pygame.event.get():  # Xử lý sự kiện
            if event.type == pygame.QUIT:
                running = False  # Đóng game nếu bấm X
            elif event.type == pygame.KEYDOWN:  # Nhấn phím
                if event.key == pygame.K_ESCAPE:
                    if show_menu() == "quit":  # Hiện menu tạm dừng
                        running = False
                if event.key in [pygame.K_LEFT, pygame.K_a]: move_direction['left'] = True
                if event.key in [pygame.K_RIGHT, pygame.K_d]: move_direction['right'] = True
                if event.key in [pygame.K_UP, pygame.K_w]: move_direction['up'] = True
                if event.key in [pygame.K_DOWN, pygame.K_s]: move_direction['down'] = True
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]: fire_bullet()  # Bắn đạn
            elif event.type == pygame.KEYUP:  # Thả phím
                if event.key in [pygame.K_LEFT, pygame.K_a]: move_direction['left'] = False
                if event.key in [pygame.K_RIGHT, pygame.K_d]: move_direction['right'] = False
                if event.key in [pygame.K_UP, pygame.K_w]: move_direction['up'] = False
                if event.key in [pygame.K_DOWN, pygame.K_s]: move_direction['down'] = False

        player.move(move_direction, boundary_y)  # Cập nhật vị trí player
        player.update_buffs()  # Cập nhật buff còn hiệu lực

        for b in bullets[:]:  # Vòng lặp vẽ và di chuyển đạn
            b['x'] += b['dx']
            b['y'] += b['dy']
            screen.blit(bulletImg, (b['x'], b['y']))
            if b['y'] < 0:  # Đạn ra khỏi màn hình
                bullets.remove(b)

        # ... (phần sau mình sẽ chú thích tiếp nếu bạn muốn)

