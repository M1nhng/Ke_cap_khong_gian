import pygame
import random
import math
from menu import show_menu
from enemy import Enemy, DiagonalEnemy, BombEnemy, ShotgunEnemy, ShadowEnemy, BossEnemy
from Level_manager import LevelManager
from audio_settings import set_sfx_volume
from items import Item, check_collision_and_apply
import open as open_menu

class HealthManager:
    def __init__(self, max_health=100):
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)
        return self.current_health <= 0

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def get_health(self):
        return self.current_health

    def get_max_health(self):
        return self.max_health

class Player:
    def __init__(self):
        self.image = pygame.image.load('D:/Python/Game/images/arcade_space.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.x = (1200 - 100) // 2
        self.y = 693
        self.speed = 1.5
        self.move = {'left': False, 'right': False, 'up': False, 'down': False}
        self.health_manager = HealthManager(max_health=100)
        self.hp = 100
        self.max_hp = 100
        self.shield = 0
        self.max_shield = 20
        self.base_speed = 3
        self.triple_shot_timer = 0
        self.speed_boost_timer = 0
        self.invulnerable_timer = 0
        self.shield_effect = pygame.transform.scale(
            pygame.image.load('D:/Python/Game/images/blueshield.png'),
            (120, 120)
        )

    def handle_movement(self):
        if self.move['left']:
            self.x -= self.speed
        if self.move['right']:
            self.x += self.speed
        if self.move['up']:
            self.y -= self.speed
        if self.move['down']:
            self.y += self.speed

        self.x = max(0, min(self.x, 1200 - self.image.get_width()))
        self.y = max(0, min(self.y, 850 - self.image.get_height()))

    def draw(self, screen):
        if self.shield > 0:
            shield_x = self.x - (self.shield_effect.get_width() - self.image.get_width()) // 2
            shield_y = self.y - (self.shield_effect.get_height() - self.image.get_height()) // 2
            screen.blit(self.shield_effect, (shield_x, shield_y))
        if self.invulnerable_timer % 4 < 2:
            screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        fill = (self.health_manager.get_health() / self.health_manager.get_max_health()) * bar_width
        outline_rect = pygame.Rect(self.x, self.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.x, self.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def update_buffs(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.triple_shot_timer > 0:
            self.triple_shot_timer -= 1
        if self.speed_boost_timer > 0:
            self.speed = self.base_speed * 2
            self.speed_boost_timer -= 1
        else:
            self.speed = self.base_speed

class Bullet:
    def __init__(self, angle=0):
        self.image = pygame.image.load('D:/Python/Game/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (34, 34))
        self.x = 0
        self.y = 800
        self.speed = 7
        self.angle = angle
        self.state = "ready"
        self.damage = 10

    def fire(self, x, y, player_width, triple_shot_active=False):
        self.state = "fire"
        self.x = x + player_width // 2 - self.image.get_width() // 2
        self.y = y - self.image.get_height()
        if triple_shot_active:
            self.damage = 15

    def move(self):
        if self.state == "fire":
            rad = math.radians(self.angle)
            self.x += self.speed * math.sin(rad)
            self.y -= self.speed * math.cos(rad)
            if self.y <= 0 or self.x < 0 or self.x > 1200:
                self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 850))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('D:/Python/Game/images/background.png')
        self.background = pygame.transform.scale(self.background, (1200, 850))

        icon = pygame.image.load('D:/Python/Game/images/Logo.png')
        pygame.display.set_icon(icon)

        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.items = []
        self.level_manager = LevelManager()

        self.running = True
        self.spawn_counter = 0
        self.spawned_this_level = 0
        self.score = 0
        self.shoot_cooldown = 0
        self.bomb_enemy_spawned = False

        self.spawn_delays = {
            1: 350,
            2: 100,
            3: 160,
            4: 140,
            5: 120
        }
        self.spawn_delay = self.spawn_delays[1]

        self.font = pygame.font.SysFont(None, 36)

        self.shoot_sound = pygame.mixer.Sound("D:/Python/Game/sounds/shoot3.wav")
        set_sfx_volume(self.shoot_sound)

        self.die_sound = pygame.mixer.Sound("D:/Python/Game/sounds/die_sound.wav")
        set_sfx_volume(self.die_sound)

    def get_player_pos(self):
        return self.player.x, self.player.y

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def spawn_enemy(self):
        current_level = self.level_manager.current_level
        if current_level == 5:
            new_enemy = BossEnemy(current_level, 1200, 850, self.get_player_pos)
            new_enemy.health = 100
            self.level_manager.handle_special_levels()
            self.enemies.append(new_enemy)
        else:
            if current_level == 1:
                if self.level_manager.get_time_left() > 0:
                    new_enemy = Enemy(current_level, 1200, 850, self.get_player_pos)
                    new_enemy.health = 10
                    self.enemies.append(new_enemy)
                    self.spawned_this_level += 1
            elif current_level == 2:
                if not self.bomb_enemy_spawned:
                    bomb_enemy = BombEnemy(current_level, 1200, 850, self.get_player_pos)
                    self.enemies.append(bomb_enemy)
                    self.bomb_enemy_spawned = True
                    self.spawned_this_level += 1

                if self.level_manager.get_time_left() > 0:
                    enemy_types = [Enemy, DiagonalEnemy]
                    weights = [0.6, 0.4]
                    enemy_type = random.choices(enemy_types, weights=weights, k=1)[0]
                    new_enemy = enemy_type(current_level, 1200, 850, self.get_player_pos)
                    if isinstance(new_enemy, Enemy):
                        new_enemy.health = 10
                    self.enemies.append(new_enemy)
                    self.spawned_this_level += 1
            else:
                if current_level == 3:
                    if self.level_manager.get_time_left() > 0:
                        enemy_types = [Enemy, DiagonalEnemy, ShotgunEnemy]
                        weights = [0.5, 0.3, 0.2]
                        enemy_type = random.choices(enemy_types, weights=weights, k=1)[0]
                        new_enemy = enemy_type(current_level, 1200, 850, self.get_player_pos)
                        if isinstance(new_enemy, Enemy):
                            new_enemy.health = 10 + (current_level - 1) * 5
                        elif isinstance(new_enemy, DiagonalEnemy):
                            new_enemy.health = 15 + (current_level - 1) * 5
                        elif isinstance(new_enemy, ShotgunEnemy):
                            new_enemy.health = 20 + (current_level - 1) * 5
                            # Đảm bảo ShotgunEnemy được hiển thị
                            if not new_enemy.image:
                                print("Error: robot.png not loaded correctly")
                        self.enemies.append(new_enemy)
                        self.spawned_this_level += 1
                elif current_level == 4:
                    if self.level_manager.get_time_left() > 0:
                        enemy_types = [Enemy, DiagonalEnemy, ShotgunEnemy, ShadowEnemy]
                        weights = [0.3, 0.3, 0.2, 0.2]
                        enemy_type = random.choices(enemy_types, weights=weights, k=1)[0]
                        new_enemy = enemy_type(current_level, 1200, 850, self.get_player_pos)
                        if isinstance(new_enemy, Enemy):
                            new_enemy.health = 10 + (current_level - 1) * 5
                        elif isinstance(new_enemy, DiagonalEnemy):
                            new_enemy.health = 15 + (current_level - 1) * 5
                        elif isinstance(new_enemy, ShotgunEnemy):
                            new_enemy.health = 20 + (current_level - 1) * 5
                        elif isinstance(new_enemy, ShadowEnemy):
                            new_enemy.health = 25 + (current_level - 1) * 5
                        self.enemies.append(new_enemy)
                        self.spawned_this_level += 1

    def update_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                high_score = int(f.read())
        except:
            high_score = 0

        if self.score > high_score:
            with open("highscore.txt", "w") as f:
                f.write(str(self.score))

    def show_game_over(self):
        self.update_high_score()
        self.enemies.clear()
        self.items.clear()
        self.bullets.clear()
        self.player.health_manager.current_health = 0
        self.player.hp = 0
        self.screen.blit(self.background, (0, 0))

        game_over_font = pygame.font.SysFont(None, 100)
        prompt_font = pygame.font.SysFont(None, 60)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))

        try:
            with open("highscore.txt", "r") as f:
                high_score = int(f.read())
        except:
            high_score = 0

        score_text = prompt_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        high_text = prompt_font.render(f"High Score: {high_score}", True, (255, 255, 0))
        prompt_text = prompt_font.render("Press Any Key To Exit", True, (255, 255, 255))

        self.screen.blit(game_over_text, (405, 180))
        self.screen.blit(score_text, (420, 330))
        self.screen.blit(high_text, (420, 410))
        pygame.display.update()

        pygame.time.delay(2000)

        self.screen.blit(prompt_text, (420, 570))
        pygame.display.update()

        pygame.event.clear()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
        open_menu.show_main_menu()

    def run(self):
        self.level_manager.start_level(1)
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        choice = show_menu()
                        if choice == "quit":
                            self.running = False
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.player.move['left'] = True
                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.player.move['right'] = True
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.player.move['up'] = True
                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.player.move['down'] = True
                    if event.key == pygame.K_SPACE and self.shoot_cooldown <= 0:
                        triple_shot_active = self.player.triple_shot_timer > 0
                        if triple_shot_active:
                            bullet1 = Bullet(angle=0)
                            bullet2 = Bullet(angle=-20)
                            bullet3 = Bullet(angle=20)
                            bullet1.fire(self.player.x, self.player.y, self.player.image.get_width(), triple_shot_active)
                            bullet2.fire(self.player.x, self.player.y, self.player.image.get_width(), triple_shot_active)
                            bullet3.fire(self.player.x, self.player.y, self.player.image.get_width(), triple_shot_active)
                            self.bullets.extend([bullet1, bullet2, bullet3])
                        else:
                            bullet = Bullet()
                            bullet.fire(self.player.x, self.player.y, self.player.image.get_width())
                            self.bullets.append(bullet)
                        set_sfx_volume(self.shoot_sound)
                        self.shoot_sound.play()
                        self.shoot_cooldown = 20
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.player.move['left'] = False
                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.player.move['right'] = False
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.player.move['up'] = False
                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.player.move['down'] = False

            self.player.handle_movement()
            self.player.update_buffs()
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

            for bullet in self.bullets[:]:
                bullet.move()
                bullet.draw(self.screen)
                if bullet.state == "ready":
                    self.bullets.remove(bullet)

            self.spawn_delay = self.spawn_delays.get(self.level_manager.current_level, 360)
            if self.spawn_counter >= self.spawn_delay:
                self.spawn_counter = 0
                self.spawn_enemy()
            self.spawn_counter += 1

            for enemy in self.enemies[:]:
                enemy.update()
                enemy.draw(self.screen)

                player_rect = self.player.get_rect()
                enemy_rect = enemy.rect
                if player_rect.colliderect(enemy_rect):
                    if self.player.shield > 0:
                        self.player.shield = max(0, self.player.shield - 5)
                    else:
                        is_dead = self.player.health_manager.take_damage(5)
                        self.player.hp = self.player.health_manager.get_health()
                        if self.player.invulnerable_timer <= 0:
                            self.player.invulnerable_timer = 60
                        if is_dead:
                            set_sfx_volume(self.die_sound)
                            self.die_sound.play()
                            pygame.time.delay(0)
                            self.show_game_over()
                            self.running = False
                    self.enemies.remove(enemy)
                    continue

                for bullet in self.bullets[:]:
                    if bullet.state == "fire" and enemy.hit_by(bullet.x, bullet.y):
                        enemy.health -= bullet.damage
                        self.bullets.remove(bullet)
                        if enemy.is_dead():
                            item = enemy.drop_item()
                            if item:
                                self.items.append(item)
                            if isinstance(enemy, BombEnemy):
                                new_bomb = BombEnemy(enemy.level, self.screen.get_width(), self.screen.get_height(), self.get_player_pos)
                                new_bomb.rect.x = random.randint(50, self.screen.get_width() - 100)
                                new_bomb.rect.y = 50
                                self.enemies.append(new_bomb)
                            self.enemies.remove(enemy)
                            self.score += 1
                            break

                if hasattr(enemy, 'bullets') and enemy.bullets:
                    for bullet in enemy.bullets[:]:
                        bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                        player_rect = self.player.get_rect()
                        if player_rect.colliderect(bullet_rect):
                            enemy.bullets.remove(bullet)
                            if self.player.shield > 0:
                                self.player.shield = max(0, self.player.shield - 5)
                            else:
                                is_dead = self.player.health_manager.take_damage(10)
                                self.player.hp = self.player.health_manager.get_health()
                                if is_dead:
                                    set_sfx_volume(self.die_sound)
                                    self.die_sound.play()
                                    pygame.time.delay(0)
                                    self.show_game_over()
                                    self.running = False

            for item in self.items[:]:
                item.update()
                self.screen.blit(item.image, item.rect)
            check_collision_and_apply(self.player, self.items, [], [])
            self.player.health_manager.current_health = self.player.hp

            self.player.draw(self.screen)

            self.draw_text(f"Level {self.level_manager.current_level}", 10, 10)
            self.draw_text(f"Score: {self.score}", 10, 40)
            time_left = int(self.level_manager.get_time_left())
            self.draw_text(f"Time Left: {time_left}s", 10, 70)

            if self.level_manager.is_level_complete():
                if self.level_manager.current_level < max(self.level_manager.level_durations.keys()):
                    self.level_manager.next_level()
                    self.enemies.clear()
                    self.items.clear()
                    self.bullets.clear()
                    self.spawned_this_level = 0
                    self.bomb_enemy_spawned = False
                else:
                    self.running = False
                    self.show_game_over()

            pygame.display.update()
            self.clock.tick(240)

        pygame.quit()

def run_game():
    game = Game()
    game.run()
