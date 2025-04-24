import pygame
import random
import math
from menu import show_menu 

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 850))
    pygame.display.set_caption("Kẻ_cướp_không_gian")
    icon = pygame.image.load('D:/Python/Game/images/Logo.png')
    pygame.display.set_icon(icon)

    backgroundImg = pygame.image.load('D:/Python/Game/images/background.png')
    backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))

    playerImg = pygame.image.load('D:/Python/Game/images/arcade_space.png')
    playerImg = pygame.transform.scale(playerImg, (100, 100))
    playerX = (1200 - 100) // 2
    playerY = 693
    player_speed = 1.5
    move_direction = {'left': False, 'right': False, 'up': False, 'down': False}

    def player(x, y):
        screen.blit(playerImg, (x, y))

    bulletImg = pygame.image.load('D:/Python/Game/images/bullet.png')
    bulletImg = pygame.transform.scale(bulletImg, (34, 34))
    bulletX = 0
    bulletY = 800
    bulletY_change = 5
    bullet_state = "ready"

    def fire_bullet(x, y):
        nonlocal bullet_state, bulletX, bulletY
        bullet_state = "fire"
        bulletX = x + playerImg.get_width() // 2 - bulletImg.get_width() // 2
        bulletY = y - bulletImg.get_height()

    enemyImg = pygame.image.load('D:/Python/Game/images/ghost.png')
    enemyImg = pygame.transform.scale(enemyImg, (65, 65))

    bossImg = pygame.image.load('D:/Python/Game/images/robot.png')
    bossImg = pygame.transform.scale(bossImg, (100, 100))

    boss_bullets = []
    boss_bullet_speed = 1.5

    enemies = []
    bosses = []

    def get_enemy_stats(level):
        health = 1 + level // 2
        speed = 0.25 + (level - 1) * 0.06
        return health, min(speed, 1.2)

    def get_boss_stats(level):
        health = 10 + level * 2
        speed = 0.3 + (level - 1) * 0.04
        return health, min(speed, 0.8)

    def spawn_enemy(level):
        health, speed = get_enemy_stats(level)
        return {'x': random.randint(50, 1150), 'y': -random.randint(100, 300), 'speed': speed, 'health': health}

    def spawn_boss(level):
        health, speed = get_boss_stats(level)
        return {'x': random.randint(100, 1100), 'y': -200, 'speed': speed, 'health': health, 'shoot_timer': 0}

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
        pygame.draw.line(screen, (255, 255, 255), (0, boundary_y), (1200, boundary_y), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = show_menu()
                    if choice == "quit":
                        running = False
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

        if bullet_state == "fire":
            bulletY -= bulletY_change
            screen.blit(bulletImg, (bulletX, bulletY))
            if bulletY <= 0:
                bullet_state = "ready"

        max_enemies = min(3 + level * 2, 25)
        spawn_counter += 1
        if spawn_counter >= spawn_delay and spawned_this_level < max_enemies:
            spawn_counter = 0
            new_enemy = spawn_enemy(level)
            while any(abs(e['x'] - new_enemy['x']) < 70 for e in enemies):
                new_enemy['x'] = random.randint(50, 1150)
            enemies.append(new_enemy)
            spawned_this_level += 1

        if level >= 3 and not bosses:
            bosses.append(spawn_boss(level))

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

        for boss in bosses[:]:
            boss['y'] += boss['speed']
            screen.blit(bossImg, (boss['x'], boss['y']))
            boss['shoot_timer'] += 1
            if boss['shoot_timer'] >= 120:
                boss['shoot_timer'] = 0
                for i in range(3):
                    angle = math.atan2(playerY - boss['y'], playerX - boss['x']) + random.uniform(-0.4, 0.4)
                    dx = math.cos(angle) * boss_bullet_speed
                    dy = math.sin(angle) * boss_bullet_speed
                    boss_bullets.append({'x': boss['x'] + 40, 'y': boss['y'] + 50, 'dx': dx, 'dy': dy})

            if bullet_state == "fire" and abs(bulletX - boss['x']) < 40 and abs(bulletY - boss['y']) < 50:
                boss['health'] -= 1
                bullet_state = "ready"
                if boss['health'] <= 0:
                    bosses.remove(boss)
                    score += 10

        for b in boss_bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)
            if b['y'] > 900 or b['x'] < 0 or b['x'] > 1200:
                boss_bullets.remove(b)

        player(playerX, playerY)
        draw_text(f"Level {level}", 10, 10)
        draw_text(f"Score: {score}", 10, 40)

        level_timer += 1
        if level_timer >= level_duration:
            level_timer = 0
            if level < max_level:
                level += 1
                enemies.clear()
                bosses.clear()
                boss_bullets.clear()
                spawned_this_level = 0

        pygame.display.update()
        clock.tick(240)

    pygame.quit()
