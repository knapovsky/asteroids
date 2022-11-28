# Tutorial on http://naucse.python.cz/2018/installfest/projects/asteroids/

import math
import random
import pyglet
from pyglet.window import key
from pyglet import gl

ACCELERATION = 30  # pixels/sec^2
ROTATION_GAIN = 50  # degrees/sec
RAND_SPEED = 100  # pixels/sec

# all objects in game
objects = []

# all pressed keys
pressed_keys = set()


window = pyglet.window.Window()

class SpaceObject:
    def __init__(self):
        self.x = window.width // 2
        self.y = window.height // 2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 0

        image = self.init_image()
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        self.radius = (image.width + image.height) / 2 / 2
        self.sprite = pyglet.sprite.Sprite(image)

        objects.append(self)


    def update_sprite(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = self.rotation

    def tick(self, t):
        self.x += t * self.x_speed
        self.y += t * self.y_speed
        self.x %= window.width
        self.y %= window.height
        self.update_sprite()

    def hit_by_spaceship(self, spaceship):
        print(self, "hit by", spaceship)
        pass

    def destroy(self):
        try:
            objects.remove(self)
        except ValueError:
            pass


class SpaceShip(SpaceObject):
    def init_image(self):
        return pyglet.image.load('spaceship.png')

    def tick(self, t):
        if key.UP in pressed_keys:
            rotation_rads = math.radians(self.rotation)
            self.x_speed += t * math.sin(rotation_rads) * ACCELERATION
            self.y_speed += t * math.cos(rotation_rads) * ACCELERATION
        if key.RIGHT in pressed_keys:
            self.rotation += ROTATION_GAIN * t
        if key.LEFT in pressed_keys:
            self.rotation -= ROTATION_GAIN * t
        super().tick(t)
        for obj in objects:
            if obj == self:
                continue
            if overlaps(obj, self):
                obj.hit_by_spaceship()

class Asteroid(SpaceObject):
    def __init__(self):
        super().__init__()
        if random.randint(0, 1):
            self.x = 0
        else:
            self.y = 0
        self.x_speed = random.randint(-RAND_SPEED, RAND_SPEED)
        self.y_speed = random.randint(-RAND_SPEED, RAND_SPEED)

    def init_image(self):
        size = random.choice(['big', 'med', 'small'])
        num = 4 if size == 'big' else 2
        num = random.randint(1, num)
        return pyglet.image.load('meteorGrey_{size}{num}.png'.format(size=size, num=num))

    def hit_by_spaceship(self):
        spaceship.destroy()
        self.destroy()

def draw_all_objects():
    window.clear()
    for obj in objects:
        obj.sprite.draw()
        draw_circle(obj.x, obj.y, obj.radius)

def tick_all_objects(t):
    for obj in objects:
        obj.tick(t)

def on_key_press(key, mod):
    pressed_keys.add(key)

def on_key_release(key, mod):
    pressed_keys.discard(key)

def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()

def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

window.push_handlers(
    on_draw=draw_all_objects,
    on_key_press=on_key_press,
    on_key_release=on_key_release,
)
pyglet.clock.schedule_interval(tick_all_objects, 1/30)

spaceship = SpaceShip()

for _ in range(6):
    Asteroid()

pyglet.app.run()