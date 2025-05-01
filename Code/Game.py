import pygame
import random
import math
from Menu import show_menu
from enemy import Enemy, DiagonalEnemy, ShotgunEnemy, ShadowEnemy, BossEnemy

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 850))
    pygame.display.set_caption("Kẻ_cướp_không_gian")
    try:
        icon = pygame.image.load('D:/Python/Game/images/Logo.png')
        pygame.display.set_icon(icon)
    except pygame.error as e:
        print(f"Error loading icon: {e}")

    try:
        backgroundImg = pygame.image.load('D:/Python/Game/images/background.png')
        backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))
    except pygame.error as e:
        print(f"Error loading background: {e}")
        backgroundImg = pygame.Surface((1200, 850))
        backgroundImg.fill((0, 0, 0))

    try:
        playerImg = pygame.image.load('D:/Python/Game/images/arcade_space.png')
        playerImg = pygame.transform.scale(playerImg, (100, 100))
    except pygame.error as e:
        print(f"Error loading player image: {e}")
        playerImg = pygame.Surface((100, 100))
        playerImg.fill((255, 255, 255))

    playerX = (1200 - 100) // 2
    playerY = 693
    player_speed = 1.5
    move_direction = {'left': False, 'right': False, 'up': False, 'down': False}

    def player(x, y):
        screen.blit(playerImg, (x, y))

    try:
        bulletImg = pygame.image.load('D:/Python/Game/images/bullet.png')
        bulletImg = pygame.transform.scale(bulletImg, (34, 34))
    except pygame.error as e:
        print(f"Error loading bullet image: {e}")
        bulletImg = pygame.Surface((34, 34))
        bulletImg.fill((255, 255, 0))

    bulletX = 0
    bulletY = 800
    bulletY_change = 5
    bullet_state = "ready"
    reflected_bullets = []  # Store reflected bullets

    try:
        enemyImg = pygame.image.load('D:/Python/Game/images/ghost.png')
        enemyImg = pygame.transform.scale(enemyImg, (65, 65))
    except pygame.error as e:
        print(f"Error loading enemy image: {e}")
        enemyImg = pygame.Surface((65, 65))
        enemyImg.fill((255, 0, 0))

    try:
        shotgun_enemy_img = pygame.image.load('D:/Python/Game/images/robot.png')
        shotgun_enemy_img = pygame.transform.scale(shotgun_enemy_img, (100, 100))
    except pygame.error as e:
        print(f"Error loading shotgun enemy image: {e}")
        shotgun_enemy_img = pygame.Surface((100, 100))
        shotgun_enemy_img.fill((255, 0, 0))

    try:
        shadow_enemy_img = pygame.image.load('D:/Python/Game/images/devil.png')  # Fixed to use devil.png
        shadow_enemy_img = pygame.transform.scale(shadow_enemy_img, (65, 65))
    except pygame.error as e:
        print(f"Error loading shadow enemy image: {e}")
        shadow_enemy_img = pygame.Surface((65, 65))
        shadow_enemy_img.fill((255, 0, 0))

    shotgun_enemy_bullets = []
    shotgun_enemy_bullet_speed = 1.5
    smart_enemies = []
    enemies = []
    diagonal_enemies = []
    shotgun_enemies = []
    shadow_enemies = []
    boss = None
    boss_spawn_timer = 0
    boss_spawn_time = 10 * 240  # 10 seconds at 240 FPS

    def get_enemy_stats(level):
        health = 1 + level // 2
        speed = 0.25 + (level - 1) * 0.06
        return health, min(speed, 1.2)

    def get_shotgun_enemy_stats(level):
        health = 10 + level * 2
        speed = 0.3 + (level - 1) * 0.04
        return health, min(speed, 0.8)

    def spawn_enemy(level):
        health, speed = get_enemy_stats(level)
        return {'x': random.randint(50, 1150), 'y': -random.randint(100, 300), 'speed': speed, 'health': health}

    def spawn_shotgun_enemy(level):
        health, speed = get_shotgun_enemy_stats(level)
        return {'x': random.randint(100, 1100), 'y': -200, 'speed': speed, 'health': health, 'shoot_timer': 0}

    def fire_bullet(x, y):
        nonlocal bullet_state, bulletX, bulletY
        bullet_state = "fire"
        bulletX = x + playerImg.get_width() // 2 - bulletImg.get_width() // 2
        bulletY = y - bulletImg.get_height()

    running = True
    clock = pygame.time.Clock()
    boundary_y = 650

    level = 1
    level_timer = 0
    level_duration = 3000
    max_level = 5
    spawn_delay = 240
    spawn_counter = 0
    spawned_this_level = 0
    score = 0
    font = pygame.font.SysFont(None, 36)

    def draw_text(text, x, y, color=(255, 255, 255)):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    while running:
        screen.blit(backgroundImg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = show_menu(screen)
                    if choice == "quit":
                        running = False
                    elif choice == "main_menu":
                        return "main_menu"
                if event.key in [pygame.K_LEFT, pygame.K_a]: move_direction['left'] = True
                if event.key in [pygame.K_RIGHT, pygame.K_d]: move_direction['right'] = True
                if event.key in [pygame.K_UP, pygame.K_w]: move_direction['up'] = True
                if event.key in [pygame.K_DOWN, pygame.K_s]: move_direction['down'] = True
                if event.key in [pygame.K_SPACE, pygame.K_RETURN] and bullet_state == "ready":
                    fire_bullet(playerX, playerY)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_a]: move_direction['left'] = False
                if event.key in [pygame.K_RIGHT, pygame.K_d]: move_direction['right'] = False
                if event.key in [pygame.K_UP, pygame.K_w]: move_direction['up'] = False
                if event.key in [pygame.K_DOWN, pygame.K_s]: move_direction['down'] = False

        if move_direction['left']: playerX -= player_speed
        if move_direction['right']: playerX += player_speed
        if move_direction['up']: playerY -= player_speed
        if move_direction['down']: playerY += player_speed

        playerX = max(0, min(playerX, 1200 - playerImg.get_width()))
        playerY = max(boundary_y, min(playerY, 850 - playerImg.get_height()))

        # Handle player bullet
        if bullet_state == "fire":
            bulletY -= bulletY_change
            if boss and boss.reflect_bullet(bulletX, bulletY):
                reflected_bullets.append({'x': bulletX, 'y': bulletY, 'dy': bulletY_change})
                bullet_state = "ready"
            else:
                screen.blit(bulletImg, (bulletX, bulletY))
                if bulletY <= 0:
                    bullet_state = "ready"

        # Handle reflected bullets
        for rb in reflected_bullets[:]:
            rb['y'] += rb['dy']
            screen.blit(bulletImg, (rb['x'], rb['y']))
            if rb['y'] > 850:
                reflected_bullets.remove(rb)

        # Spawn boss in level 5 after 10 seconds
        if level == max_level:
            boss_spawn_timer += 1
            print(f"[DEBUG] Level: {level}, Boss Spawn Timer: {boss_spawn_timer}/{boss_spawn_time}, Boss Exists: {boss is not None}")
            if boss_spawn_timer >= boss_spawn_time and not boss:
                try:
                    boss = BossEnemy(level, 1200, 850, lambda: (playerX, playerY))
                    print("[DEBUG] Boss spawned successfully")
                except pygame.error as e:
                    print(f"Error spawning boss: {e}")
                    boss = None

        # Handle boss
        if boss:
            boss.update()
            boss.draw(screen)
            if bullet_state == "fire" and boss.hit_by(bulletX, bulletY):
                bullet_state = "ready"
                if boss.is_dead():
                    boss = None
                    score += 50
                    print("[DEBUG] Boss defeated")

        if level >= 2 and len(smart_enemies) < 5:
            smart_enemies.append(Enemy(level, 1200, 850, lambda: (playerX, playerY)))
        for e in smart_enemies[:]:
            e.update()
            e.draw(screen)
            if e.hit_by(bulletX, bulletY) and bullet_state == "fire":
                bullet_state = "ready"
                if e.is_dead():
                    smart_enemies.remove(e)
                    score += 2

        max_enemies = min(3 + level * 2, 25)
        spawn_counter += 1

        if spawn_counter >= spawn_delay and spawned_this_level < max_enemies:
            print(f"[DEBUG] Level: {level} | Spawned: {spawned_this_level}/{max_enemies} | Enemies alive: {len(enemies)}")
            spawn_counter = 0
            if random.random() < 0.5:
                new_enemy = spawn_enemy(level)
                while any(abs(e['x'] - new_enemy['x']) < 70 for e in enemies):
                    new_enemy['x'] = random.randint(50, 1150)
                enemies.append(new_enemy)
            else:
                new_diagonal_enemy = DiagonalEnemy(level, 1200, 850, lambda: (playerX, playerY))
                diagonal_enemies.append(new_diagonal_enemy)
            spawned_this_level += 1

        if level >= 3 and not shotgun_enemies:
            shotgun_enemies.append(spawn_shotgun_enemy(level))

        if level >= 3 and len(shadow_enemies) < 1:
            shadow_enemies.append(ShadowEnemy(level, 1200, 850, lambda: (playerX, playerY)))

        for e in enemies[:]:
            e['y'] += e['speed']
            screen.blit(enemyImg, (e['x'], e['y']))
            if bullet_state == "fire" and abs(bulletX - e['x']) < 30 and abs(bulletY - e['y']) < 40:
                e['health'] -= 1
                bullet_state = "ready"
                if e['health'] <= 0:
                    enemies.remove(e)
                    score += 1
            elif e['y'] > boundary_y:
                enemies.remove(e)

        for de in diagonal_enemies[:]:
            de.update()
            de.draw(screen)
            if bullet_state == "fire" and de.hit_by(bulletX, bulletY):
                bullet_state = "ready"
                if de.is_dead():
                    diagonal_enemies.remove(de)
                    score += 1

        for shotgun_enemy in shotgun_enemies[:]:
            shotgun_enemy['y'] += shotgun_enemy['speed']
            screen.blit(shotgun_enemy_img, (shotgun_enemy['x'], shotgun_enemy['y']))
            shotgun_enemy['shoot_timer'] += 1
            if shotgun_enemy['shoot_timer'] >= 120:
                shotgun_enemy['shoot_timer'] = 0
                for i in range(3):
                    angle = math.atan2(playerY - shotgun_enemy['y'], playerX - shotgun_enemy['x']) + random.uniform(-0.4, 0.4)
                    dx = math.cos(angle) * shotgun_enemy_bullet_speed
                    dy = math.sin(angle) * shotgun_enemy_bullet_speed
                    shotgun_enemy_bullets.append({'x': shotgun_enemy['x'] + 40, 'y': shotgun_enemy['y'] + 50, 'dx': dx, 'dy': dy})

            if bullet_state == "fire" and abs(bulletX - shotgun_enemy['x']) < 40 and abs(bulletY - shotgun_enemy['y']) < 50:
                shotgun_enemy['health'] -= 1
                bullet_state = "ready"
                if shotgun_enemy['health'] <= 0:
                    shotgun_enemies.remove(shotgun_enemy)
                    score += 10

        for b in shotgun_enemy_bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)
            if b['y'] > 900 or b['x'] < 0 or b['x'] > 1200:
                shotgun_enemy_bullets.remove(b)

        for se in shadow_enemies[:]:
            se.update()
            se.draw(screen)
            if bullet_state == "fire" and se.hit_by(bulletX, bulletY):
                bullet_state = "ready"
                if se.is_dead():
                    shadow_enemies.remove(se)
                    score += 5

        player(playerX, playerY)
        draw_text(f"Level {level}", 10, 10)
        draw_text(f"Score: {score}", 10, 40)
        draw_text(f"Smart Enemies: {len(smart_enemies)}", 10, 70)
        draw_text(f"Diagonal Enemies: {len(diagonal_enemies)}", 10, 100)
        draw_text(f"Shadow Enemies: {len(shadow_enemies)}", 10, 130)
        if boss:
            draw_text(f"Boss Health: {boss.health}", 10, 160)

        level_timer += 1
        if level_timer >= level_duration:
            level_timer = 0
            if level < max_level:
                level += 1
                enemies.clear()
                diagonal_enemies.clear()
                shotgun_enemies.clear()
                shotgun_enemy_bullets.clear()
                shadow_enemies.clear()
                spawned_this_level = 0
                smart_enemies.clear()
                print(f"[DEBUG] Advanced to Level {level}")

        pygame.display.update()
        clock.tick(240)

    return "main_menu"
