import pygame
import random
import math
from Menu import show_menu
from items import Item, check_collision_and_apply, ITEM_TYPES
from player import Player

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 850))
    pygame.display.set_caption("Kẻ_cướp_không_gian")
    hit_sound = pygame.mixer.Sound(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\get_shoot.mp3")

    icon = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\Logo.png")
    pygame.display.set_icon(icon)

    backgroundImg = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\background.jpg")
    backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))

    player = Player(550, 693)
    bullets = []
    bulletImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\bullet.png"),
        (34, 34)
    )

    enemyImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\ghost.png"),
        (65, 65)
    )
    bossImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\favicon.png"),
        (100, 100)
    )

    boss_bullets = []
    boss_bullet_speed = 1.5

    enemies = []
    bosses = []
    items = []

    move_direction = {'left': False, 'right': False, 'up': False, 'down': False}

    clock = pygame.time.Clock()
    boundary_y = 650

    level = 1
    level_timer = 0
    level_duration = 3000
    max_level = 5
    spawn_delay = 240
    spawn_counter = 0
    score = 0

    font = pygame.font.SysFont(None, 36)

    def draw_text(text, x, y, color=(255, 255, 255)):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def fire_bullet():
        # Nếu đang có laser, vẽ tia và hủy kẻ địch trên đường
        if player.laser_timer > 0:
            # Tọa độ giữa tàu
            x_mid = player.x + player.width // 2

            # Vẽ tia laser (cyan) lên đầu màn hình
            pygame.draw.line(
                screen,
                (0, 255, 255),
                (x_mid, player.y),
                (x_mid, 0),
                4
            )

            # Hủy enemy trúng tia
            for e in enemies[:]:
                # e['x'] + 32 ≈ center x của enemy
                if abs((e['x'] + 32) - x_mid) < 20:
                    enemies.remove(e)
                    score += 1
                    # rơi item (laser chỉ từ level>=3)
                    possible = ITEM_TYPES.copy()
                    if level < 3 and 'laser' in possible:
                        possible.remove('laser')
                    items.append(Item(e['x'], e['y'], random.choice(possible)))

            # Hủy boss trúng tia
            for boss in bosses[:]:
                if abs((boss['x'] + 50) - x_mid) < 25:
                    boss['health'] -= 1
                    if boss['health'] <= 0:
                        bosses.remove(boss)
                        score += 10

            return  # thoát luôn, không bắn đạn thường

        # --- Ngược lại: bắn đạn thường ---
        dxs = [-2, 0, 2] if player.triple_shot_timer > 0 else [0]
        for dx in dxs:
            bullets.append({
                'x': player.x + player.width//2 - bulletImg.get_width()//2,
                'y': player.y,
                'dx': dx,
                'dy': -5
            })
    



    def spawn_enemy(level):
        health = 1 + level // 2
        speed = min(0.25 + (level - 1) * 0.06, 1.2)
        return {'x': random.randint(50, 1150), 'y': -random.randint(100, 300), 'speed': speed, 'health': health}

    def spawn_boss(level):
        health = 10 + level * 2
        speed = min(0.3 + (level - 1) * 0.04, 0.8)
        return {'x': random.randint(100, 1100), 'y': -200, 'speed': speed, 'health': health, 'shoot_timer': 0}

    running = True
    while running:
        screen.blit(backgroundImg, (0, 0))

        # --- Xử lý sự kiện ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    if show_menu() == "quit":
                        running = False
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_direction['left'] = True
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_direction['right'] = True
                if event.key in (pygame.K_UP, pygame.K_w):
                    move_direction['up'] = True
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    move_direction['down'] = True
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_direction['left'] = False
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_direction['right'] = False
                if event.key in (pygame.K_UP, pygame.K_w):
                    move_direction['up'] = False
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    move_direction['down'] = False

        # --- Cập nhật player ---
        player.move(move_direction, boundary_y)
        player.update_buffs()
        if player.hp <= 0:
            break  # kết thúc game khi hết máu

        # --- Vẽ và di chuyển đạn player ---
        for b in bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            screen.blit(bulletImg, (b['x'], b['y']))
            if b['y'] < 0:
                bullets.remove(b)

        # --- Sinh spawn enemy/boss ---
        if len(enemies) < min(3 + level * 2, 25) and spawn_counter >= spawn_delay:
            enemies.append(spawn_enemy(level))
            spawn_counter = 0
        else:
            spawn_counter += 1

        if level >= 3 and not bosses:
            bosses.append(spawn_boss(level))

        # --- Cập nhật và vẽ enemy ---
        for e in enemies[:]:
            e['y'] += e['speed']
            enemy_rect = pygame.Rect(e['x'], e['y'], 65, 65)
            screen.blit(enemyImg, (e['x'], e['y']))

            # va chạm player <-> enemy
            if player.get_rect().colliderect(enemy_rect):
                damage = 10
                if player.invulnerable_timer == 0:
                    # trừ giáp trước
                    if player.shield > 0:
                        used = min(player.shield, damage)
                        player.shield -= used
                        damage -= used
                    if damage > 0:
                        player.hp = max(0, player.hp - damage)
                    player.invulnerable_timer = 20
                    trigger_hit_effects(screen, backgroundImg, font, hit_sound, player, damage)
                    enemies.remove(e)
                    continue
            # player đạn bắn trúng enemy
            for b in bullets[:]:
                if enemy_rect.collidepoint(b['x'], b['y']):
                    e['health'] -= 1
                    bullets.remove(b)
                    if e['health'] <= 0:
                        enemies.remove(e)
                        score += 1
                        # rơi item ngẫu nhiên từ ITEM_TYPES
                        itype = random.choice(ITEM_TYPES)
                        # rơi item ngẫu nhiên, laser chỉ xuất hiện từ level >=3
                        possible = ITEM_TYPES.copy()
                        if level < 3 and 'laser' in possible:
                            possible.remove('laser')
                        itype = random.choice(possible)
                        items.append(Item(e['x'], e['y'], itype))
                    break

            if e['y'] > boundary_y:
                enemies.remove(e)

        # --- Cập nhật và vẽ boss (tương tự) ---
        for boss in bosses[:]:
            boss['y'] += boss['speed']
            boss_rect = pygame.Rect(boss['x'], boss['y'], 100, 100)
            screen.blit(bossImg, (boss['x'], boss['y']))
            boss['shoot_timer'] += 1

            if boss['shoot_timer'] >= 120:
                boss['shoot_timer'] = 0
                for _ in range(3):
                    ang = math.atan2(player.y - boss['y'], player.x - boss['x']) + random.uniform(-0.4, 0.4)
                    boss_bullets.append({
                        'x': boss['x'] + 40, 'y': boss['y'] + 50,
                        'dx': math.cos(ang) * boss_bullet_speed,
                        'dy': math.sin(ang) * boss_bullet_speed
                    })

            # đạn player trúng boss
            for b in bullets[:]:
                if boss_rect.collidepoint(b['x'], b['y']):
                    boss['health'] -= 1
                    bullets.remove(b)
                    if boss['health'] <= 0:
                        bosses.remove(boss)
                        score += 10
                        itype = random.choice(ITEM_TYPES)
                        # rơi item ngẫu nhiên, laser chỉ xuất hiện từ level >=3
                        possible = ITEM_TYPES.copy()
                        if level < 3 and 'laser' in possible:
                            possible.remove('laser')
                        itype = random.choice(possible)
                        items.append(Item(e['x'], e['y'], itype))
                    break

        # --- Cập nhật và vẽ đạn boss ---
        for b in boss_bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)
            if player.get_rect().collidepoint(b['x'], b['y']):
                boss_bullets.remove(b)
                damage = 10
                if player.invulnerable_timer == 0:
                    if player.shield > 0:
                        used = min(player.shield, damage)
                        player.shield -= used
                        damage -= used
                    if damage > 0:
                        player.hp = max(0, player.hp - damage)
                    player.invulnerable_timer = 20
                    trigger_hit_effects(screen, backgroundImg, font, hit_sound, player, damage)
            elif b['y'] > 900 or b['x'] < 0 or b['x'] > 1200:
                boss_bullets.remove(b)

        # --- Cập nhật và vẽ items ---
        for item in items[:]:
            item.update()
            item.draw(screen)

        # Kiểm tra va chạm và áp dụng
        check_collision_and_apply(player, items, enemies, boss_bullets)

        # Vẽ player và HUD
        player.draw(screen)
        player.draw_status_bars(screen)
        draw_text(f"Level {level}", 10, 30)
        draw_text(f"Score: {score}", 10, 60)

        # Tăng level theo thời gian
        level_timer += 1
        if level_timer >= level_duration:
            level_timer = 0
            if level < max_level:
                level += 1
                enemies.clear()
                bosses.clear()
                boss_bullets.clear()

        pygame.display.update()
        clock.tick(240)

    pygame.quit()

def trigger_hit_effects(screen, backgroundImg, font, hit_sound, player, damage):
    for _ in range(5):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.blit(backgroundImg, (offset_x, offset_y))
        pygame.display.update()
        pygame.time.delay(15)

    red_flash = pygame.Surface((1200, 850))
    red_flash.fill((255, 0, 0))
    red_flash.set_alpha(80)
    screen.blit(red_flash, (0, 0))
    pygame.display.update()
    pygame.time.delay(60)

    if hit_sound:
        hit_sound.play()

    dmg_text = font.render(f"-{damage} HP", True, (255, 0, 0))
    screen.blit(dmg_text, (player.x + player.width // 2 - 20, player.y - 30))
    pygame.display.update()
    pygame.time.delay(400)

    player.invulnerable_timer = 12
    pass
