import pygame
import random
import math
from Menu import show_menu
from items import Item, check_collision_and_apply
from player import Player

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 850))
    pygame.display.set_caption("Kẻ_cướp_không_gian")

    icon = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\Logo.png")
    pygame.display.set_icon(icon)

    backgroundImg = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\background.jpg")
    backgroundImg = pygame.transform.scale(backgroundImg, (1200, 850))

    player = Player(550, 693)
    bullets = []
    bulletImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\bullet.png"), (34, 34))

    enemyImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\ghost.png"), (65, 65))

    bossImg = pygame.transform.scale(
        pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\favicon.png"), (100, 100))

    boss_bullets = []
    boss_bullet_speed = 1.5

    enemies = []
    bosses = []
    items = []
    move_direction = {'left': False, 'right': False, 'up': False, 'down': False}

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

    def fire_bullet():
        if player.triple_shot_timer > 0:
            for dx in [-2, 0, 2]:
                bullets.append({'x': player.x + player.width // 2 - bulletImg.get_width() // 2,
                                'y': player.y, 'dx': dx, 'dy': -5})
        else:
            bullets.append({'x': player.x + player.width // 2 - bulletImg.get_width() // 2,
                            'y': player.y, 'dx': 0, 'dy': -5})

    def spawn_enemy(level):
        health = 1 + level // 2
        speed = min(0.25 + (level - 1) * 0.06, 1.2)
        return {'x': random.randint(50, 1150), 'y': -random.randint(100, 300), 'speed': speed, 'health': health}

    def spawn_boss(level):
        health = 10 + level * 2
        speed = min(0.3 + (level - 1) * 0.04, 0.8)
        return {'x': random.randint(100, 1100), 'y': -200, 'speed': speed, 'health': health, 'shoot_timer': 0}

    while running:
        screen.blit(backgroundImg, (0, 0))
        # pygame.draw.line(screen, (255, 255, 255), (0, boundary_y), (1200, boundary_y), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_menu() == "quit":
                        running = False
                if event.key in [pygame.K_LEFT, pygame.K_a]: move_direction['left'] = True
                if event.key in [pygame.K_RIGHT, pygame.K_d]: move_direction['right'] = True
                if event.key in [pygame.K_UP, pygame.K_w]: move_direction['up'] = True
                if event.key in [pygame.K_DOWN, pygame.K_s]: move_direction['down'] = True
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]: fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_a]: move_direction['left'] = False
                if event.key in [pygame.K_RIGHT, pygame.K_d]: move_direction['right'] = False
                if event.key in [pygame.K_UP, pygame.K_w]: move_direction['up'] = False
                if event.key in [pygame.K_DOWN, pygame.K_s]: move_direction['down'] = False

        player.move(move_direction, boundary_y)
        player.update_buffs()

        for b in bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            screen.blit(bulletImg, (b['x'], b['y']))
            if b['y'] < 0:
                bullets.remove(b)

        if len(enemies) < min(3 + level * 2, 25) and spawn_counter >= spawn_delay:
            new_enemy = spawn_enemy(level)
            enemies.append(new_enemy)
            spawn_counter = 0
            spawned_this_level += 1
        else:
            spawn_counter += 1

        if level >= 3 and not bosses:
            bosses.append(spawn_boss(level))

        for e in enemies[:]:
            e['y'] += e['speed']
            screen.blit(enemyImg, (e['x'], e['y']))
            for b in bullets[:]:
                if abs(b['x'] - e['x']) < 30 and abs(b['y'] - e['y']) < 40:
                    e['health'] -= 1
                    bullets.remove(b)
                    if e['health'] <= 0:
                        enemies.remove(e)
                        score += 1
                        if random.random() < 0.3:
                            items.append(Item(e['x'], e['y']))
                    break
            if e['y'] > boundary_y:
                enemies.remove(e)

        for boss in bosses[:]:
            boss['y'] += boss['speed']
            screen.blit(bossImg, (boss['x'], boss['y']))
            boss['shoot_timer'] += 1
            if boss['shoot_timer'] >= 120:
                boss['shoot_timer'] = 0
                for i in range(3):
                    angle = math.atan2(player.y - boss['y'], player.x - boss['x']) + random.uniform(-0.4, 0.4)
                    dx = math.cos(angle) * boss_bullet_speed
                    dy = math.sin(angle) * boss_bullet_speed
                    boss_bullets.append({'x': boss['x'] + 40, 'y': boss['y'] + 50, 'dx': dx, 'dy': dy})
            for b in bullets[:]:
                if abs(b['x'] - boss['x']) < 40 and abs(b['y'] - boss['y']) < 50:
                    boss['health'] -= 1
                    bullets.remove(b)
                    if boss['health'] <= 0:
                        bosses.remove(boss)
                        score += 10

        for b in boss_bullets[:]:
            b['x'] += b['dx']
            b['y'] += b['dy']
            pygame.draw.circle(screen, (255, 50, 50), (int(b['x']), int(b['y'])), 5)
            if b['y'] > 900 or b['x'] < 0 or b['x'] > 1200:
                boss_bullets.remove(b)

        for item in items[:]:
            item.update()
            item.draw(screen)
        check_collision_and_apply(player, items)

        player.draw(screen)
        player.draw_status_bars(screen)
        draw_text(f"Level {level}", 10, 30)
        draw_text(f"Score: {score}", 10, 60)


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
