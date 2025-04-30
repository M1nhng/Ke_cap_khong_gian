import pygame


VOLUME_SETTINGS = {
    "master": 0.5,
    "sfx": 0.5,
    "music": 0.5
}


def set_sfx_volume(sound):
    sound.set_volume(VOLUME_SETTINGS["master"] * VOLUME_SETTINGS["sfx"])


def set_music_volume():
    pygame.mixer.music.set_volume(VOLUME_SETTINGS["master"] * VOLUME_SETTINGS["music"])
