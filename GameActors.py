__author__ = 'Legio'
#codinf=utf-8

from GameSound import *
import math
import random

games.init(screen_width=1024, screen_height=680, fps=50)

def create_animation(image, cols, rows, sprite_width, sprite_height):
    sprite_sheet = games.load_image(image)
    imgs = []
    for i in range(0, rows, 1):
        for j in range(0, cols, 1):
            imgs.append(sprite_sheet.subsurface((sprite_width*j, sprite_height*i, sprite_width, sprite_height)))
    return imgs

def wrap_borders(obj):
    if obj.top > games.screen.height:
        obj.bottom = 0
    if obj.bottom < 0:
        obj.top = games.screen.height
    if obj.left > games.screen.width:
        obj.right = 0
    if obj.right < 0:
        obj.left = games.screen.width

def overlaping(obj):
    if obj.overlapping_sprites:
        for sprite in obj.overlapping_sprites:
            if type(sprite).__name__ == "Asteroid":
                sprite.die()
                obj.die()


class Ship(games.Sprite):
    img = games.load_image("ship.png")
    VELOCITY_MULT = 3
    burst_sound = GameSound.BURST_SOUND
    MISSILE_DELAY = 25

    def __init__(self, game):
        super().__init__(image=Ship.img,
                         x = games.screen.width/2,
                         y = games.screen.height/2)
        self.missile_wait = 0
        self.game = game
        games.screen.add(self)

    def update(self):
        wrap_borders(self)
        overlaping(self)
        if games.keyboard.is_pressed(games.K_w):
            self.y -= 1
        if games.keyboard.is_pressed(games.K_s):
            self.y += 1
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 1
        if games.keyboard.is_pressed(games.K_d):
            self.x += 1
        if games.mouse.is_pressed(2):
            Ship.burst_sound.play()
            angle = self.angle*math.pi/180
            self.dx = Ship.VELOCITY_MULT * math.sin(angle)
            self.dy = Ship.VELOCITY_MULT * -math.cos(angle)
        if not games.mouse.is_pressed(2):
            self.dx = 0
            self.dy = 0
        if games.mouse.is_pressed(0) and self.missile_wait <= 0:
            self.shoot()
        if self.missile_wait > 0:
            self.missile_wait -=1
        wrap_borders(self)
        overlaping(self)

        mouseX, mouseY = games.mouse.get_position()
        playerX, playerY = self.get_position()
        self.angle = math.atan2(mouseX-playerX, playerY-mouseY)*180/math.pi

    def shoot(self):
        Missile(self.x, self.y, self.angle)
        self.missile_wait = Ship.MISSILE_DELAY

    def die(self):
        self.game.end()
        self.destroy()


class Explosion(games.Animation):
    exps = create_animation("explosion.png", 5, 5, 64, 64)
    sound = GameSound.EXPLOSION_SOUND
    def __init__(self, x, y):
        super().__init__(images=Explosion.exps,
                         x=x,
                         y=y,
                         n_repeats=1,
                         repeat_interval=5,
                         is_collideable=False)
        games.screen.add(self)
        self.sound.play()


class Asteroid(games.Animation):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    SPAWN = 2
    POINTS = 30
    total = 0
    imgs = {SMALL : create_animation("asteroids_s.png", 5, 6, 36, 36),
            MEDIUM: create_animation("asteroids_m.png", 5, 6, 48, 48),
            LARGE: create_animation("asteroids.png", 5, 6, 64, 64)}
    SPEED = 2

    def __init__(self, game, x, y, size):
        super().__init__(images=Asteroid.imgs[size],
                         x=x,
                         y=y,
                         dx=random.choice([1, -1]) * Asteroid.SPEED * random.random()/size,
                         dy=random.choice([1, -1]) * Asteroid.SPEED * random.random()/size,
                         n_repeats=0,
                         repeat_interval=10)
        self.game = game
        self.size = size
        Asteroid.total += 1
        games.screen.add(self)

    def update(self):
        wrap_borders(self)

    def die(self):
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                Asteroid(self.game, self.x, self.y, self.size-1)
        Explosion(self.x, self.y)
        Asteroid.total -= 1
        self.game.score.value += int((Asteroid.POINTS / self.size))
        self.game.score.right = games.screen.width - 10
        if Asteroid.total <= 0:
            self.game.advance()
        self.destroy()


class Missile(games.Animation):
    imgs = create_animation("projectile.png", 4, 4, 16, 16)
    sound = GameSound.MISSILE_SOUND
    BUFFER = 50
    VELOCITY_FACTOR = 7
    LIFETIME = 50

    def __init__(self, ship_x, ship_y, ship_angle):
        Missile.sound.play()
        angle = ship_angle*math.pi/180
        buffer_x = Missile.BUFFER*math.sin(angle)
        buffer_y = Missile.BUFFER*-math.cos(angle)
        x = ship_x+buffer_x
        y = ship_y+buffer_y
        dx = Missile.VELOCITY_FACTOR*math.sin(angle)
        dy = Missile.VELOCITY_FACTOR*-math.cos(angle)
        super().__init__(images=Missile.imgs,
                         x=x,
                         y=y,
                         dx=dx,
                         dy=dy,
                         n_repeats=0,
                         repeat_interval=10)
        self.lifetime = Missile.LIFETIME
        games.screen.add(self)

    def update(self):
        self.lifetime -=1
        if self.lifetime <= 0:
            self.destroy()
        wrap_borders(self)
        overlaping(self)

    def die(self):
        self.destroy()



