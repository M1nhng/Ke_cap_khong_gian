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
    hit_sound = pygame.mixer.Sound(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\get_shoot.mp3")

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
            bullet = {
                'x': player.x + player.width // 2 - bulletImg.get_width() // 2,
                'y': player.y,
                'dx': 0,
                'dy': -5
            }
            if level >= 3 and level < 5:
                bullet['homing'] = True
            if level >= 5:
                bullet['laser'] = True
            bullets.append(bullet)

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

        # Update player bullets
        for b in bullets[:]:
            # Homing behavior
            if b.get("homing") and enemies:
                nearest_enemy = min(enemies, key=lambda e: (e['x'] - b['x'])**2 + (e['y'] - b['y'])**2)
                angle = math.atan2(nearest_enemy['y'] - b['y'], nearest_enemy['x'] - b['x'])
                b['dx'] = math.cos(angle) * 5
                b['dy'] = math.sin(angle) * 5

            b['x'] += b['dx']
            b['y'] += b['dy']
            screen.blit(bulletImg, (b['x'], b['y']))
            if b['y'] < 0 or b['y'] > 900 or b['x'] < 0 or b['x'] > 1200:
                bullets.remove(b)

        # Handle enemy collision with bullets
        for e in enemies[:]:
            e['y'] += e['speed']
            screen.blit(enemyImg, (e['x'], e['y']))
            if player.get_rect().colliderect(pygame.Rect(e['x'], e['y'], 65, 65)):
                damage = 10
                if player.invulnerable_timer == 0:
                    if player.shield > 0:
                        actual = min(player.shield, damage)
                        player.shield -= actual
                        damage -= actual
                    if damage > 0:
                        player.hp = max(0, player.hp - damage)
                    player.invulnerable_timer = 20
                    trigger_hit_effects(screen, backgroundImg, font, hit_sound, player, damage)
                enemies.remove(e)
            for b in bullets[:]:
                if abs(b['x'] - e['x']) < 30 and abs(b['y'] - e['y']) < 40:
                    e['health'] -= 1
                    if not b.get("laser"):
                        bullets.remove(b)
                    if e['health'] <= 0:
                        enemies.remove(e)
                        score += 1
                        if random.random() < 0.7:
                            items.append(Item(e['x'], e['y']))
                    break

        # Remaining game logic here (boss, items, player, UI...)

    pygame.quit()

def trigger_hit_effects(screen, backgroundImg, font, hit_sound, player, damage):
    if not pygame.display.get_init():
        return

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
    screen.blit(dmg_text, (player.x + player.width//2 - 20, player.y - 30))
    pygame.display.update()
    pygame.time.delay(400)

    player.invulnerable_timer = 12
