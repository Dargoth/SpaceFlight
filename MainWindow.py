__author__ = 'Legio'
#coding=utf-8

from livewires import color
from GameActors import *
from GameSound import *

class Game(object):

    def __init__(self):
        self.level = 0
        self.level_sound = GameSound.LOAD_SOUND
        self.score = games.Text(value=0,
                                size=30,
                                color=color.white,
                                top = 5,
                                right=games.screen.width-10,
                                is_collideable=False)
        games.screen.add(self.score)
        self.ship = Ship(self)

    def play(self):
        bg = games.load_image("space.jpg", transparent=False)
        games.screen.background = bg
        GameSound.play_music()
        self.advance()
        games.screen.mainloop()

    def advance(self):
        self.level += 1
        BUFFER = 150
        for i in range(self.level * 5):
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min
            x_dist = random.randrange(x_min, games.screen.width - x_min)
            y_dist = random.randrange(y_min, games.screen.height - y_min)
            x = self.ship.x + x_dist
            y = self.ship.y + y_dist
            x%= games.screen.width
            y%= games.screen.height
            size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
            Asteroid(self, x = x, y = y, size = size)
        GameMessage(self)

    def end(self):
        end_message = games.Message(value="Game Over",
                                    size=90,
                                    color=color.red,
                                    x = games.screen.width/2,
                                    y=games.screen.height/2,
                                    lifetime= 5 * games.screen.fps,
                                    after_death=games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_message)


class GameMessage(games.Message):
    def __init__(self, game):
        super().__init__(value="Level " + str(game.level),
                                              size=40,
                                              color=color.yellow,
                                              x=games.screen.width/2,
                                              y=games.screen.height/10,
                                              lifetime=3*games.screen.fps,
                                              is_collideable=False)
        games.screen.add(self)
        if game.level > 1:
            game.level_sound.play()


def main():
    Game().play()


if __name__ == '__main__':
    main()

