__author__ = 'Legio'
#coding=utf-8
from livewires import games


class GameSound():
    MISSILE_SOUND = games.load_sound("mlaunch.wav")
    EXPLOSION_SOUND = games.load_sound("explosion3.wav")
    BURST_SOUND = games.load_sound("rush.wav")
    LOAD_SOUND = games.load_sound("load.wav")
    MAIN_THEME = games.music.load("theme.wav")

    @staticmethod
    def play_music():
        games.music.play(-1)

    @staticmethod
    def stop_music():
        games.music.stop()