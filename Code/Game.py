import pygame
import random
import math
from menu import show_menu
from enemy import Enemy
import open as open_menu

class Player:
    def __init__(self):
        self.image = pygame.image.load('D:/Python/Game/images/arcade_space.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.x = (1200 - 100) // 2
        self.y = 693
        self.speed = 1.5
        self.move = {'left': False, 'right': False, 'up': False, 'down': False}
        self.max_health = 5
        self.health = self.max_health

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
        screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.x, self.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.x, self.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)


class Bullet:
    def __init__(self):
        self.image = pygame.image.load('D:/Python/Game/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (34, 34))
        self.x = 0
        self.y = 800
        self.speed = 5
        self.state = "ready"

    def fire(self, x, y, player_width):
        self.state = "fire"
        self.x = x + player_width // 2 - self.image.get_width() // 2
        self.y = y - self.image.get_height()

    def move(self):
        if self.state == "fire":
            self.y -= self.speed
            if self.y <= 0:
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
        self.bullet = Bullet()
        self.enemies = []

        self.running = True
        self.level = 1
        self.level_timer = 0
        self.spawn_counter = 0
        self.spawned_this_level = 0
        self.score = 0

        self.max_level = 5
        self.spawn_delay = 240
        self.font = pygame.font.SysFont(None, 36)

    def get_player_pos(self):
        return self.player.x, self.player.y

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def spawn_enemy(self):
        new_enemy = Enemy(self.level, 1200, 850, self.get_player_pos)
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

        # Clear all entities for clean Game Over screen
        self.enemies.clear()
        self.bullet.state = "ready"
        self.player.health = 0

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
                    if event.key == pygame.K_SPACE and self.bullet.state == "ready":
                        self.bullet.fire(self.player.x, self.player.y, self.player.image.get_width())
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
            self.bullet.move()

            if self.spawn_counter >= self.spawn_delay:
                self.spawn_counter = 0
                self.spawn_enemy()
            self.spawn_counter += 1

            for enemy in self.enemies[:]:
                enemy.update()
                enemy.draw(self.screen)

                if self.bullet.state == "fire" and enemy.hit_by(self.bullet.x, self.bullet.y):
                    self.bullet.state = "ready"
                    if enemy.is_dead():
                        self.enemies.remove(enemy)
                        self.score += 1

                for bullet in enemy.bullets[:]:
                    bullet_rect = pygame.Rect(bullet['x'] - 5, bullet['y'] - 5, 10, 10)
                    player_rect = pygame.Rect(self.player.x, self.player.y, self.player.image.get_width(), self.player.image.get_height())
                    if player_rect.colliderect(bullet_rect):
                        enemy.bullets.remove(bullet)
                        self.player.health -= 1
                        if self.player.health <= 0:
                            self.show_game_over()
                            self.running = False

            self.player.draw(self.screen)
            self.bullet.draw(self.screen)

            self.draw_text(f"Level {self.level}", 10, 10)
            self.draw_text(f"Score: {self.score}", 10, 40)

            self.level_timer += 1
            if self.level_timer >= 3000:
                self.level_timer = 0
                if self.level < self.max_level:
                    self.level += 1
                    self.enemies.clear()
                    self.spawned_this_level = 0

            pygame.display.update()
            self.clock.tick(240)

        pygame.quit()

def run_game():
    game = Game()
    game.run()
