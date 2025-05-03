import pygame
import random

# Load and scale item images (clone removed)
item_images = {
    'heal': pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\healing.png"),
    'speed_up': pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\speed.png"),
    'triple_shot': pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\threebullets.png"),
    'shield_up': pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\defence.png")
}

for key in item_images:
    item_images[key] = pygame.transform.scale(item_images[key], (40, 40))

ITEM_TYPES = list(item_images.keys())

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.type = item_type
        self.image = item_images[item_type]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 2  # example fall speed

    def is_off_screen(self):
        return self.rect.top > pygame.display.get_surface().get_height()


def check_collision_and_apply(player, items, enemies, boss_bullets):
    for item in items[:]:
        if player.rect.colliderect(item.rect):
            if item.type == 'heal':
                player.hp = min(player.max_hp, player.hp + 20)
            elif item.type == 'speed_up':
                player.speed_boost_timer = 300
            elif item.type == 'triple_shot':
                player.triple_shot_timer = 300
            elif item.type == 'shield_up':
                player.shield = min(player.max_shield, player.shield + 10)
            items.remove(item)
        elif item.is_off_screen():
            items.remove(item)
