#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
window = pyglet.window.Window()

RYCHLOST = 10 # pix/s
UHLOVA_RYCHLOST = 10 # stupne/s

def zpracuj_text(text):
    print(text)

def tik(t):
    sprite.x += t * RYCHLOST
    sprite.y += t * RYCHLOST
    sprite.rotation += t * UHLOVA_RYCHLOST

obrazek = pyglet.image.load('src/had.png')
obrazek.anchor_x = obrazek.width // 2
obrazek.anchor_y = obrazek.height // 2
sprite = pyglet.sprite.Sprite(obrazek)

def vykresli():
    print('kreslim')
    window.clear()
    sprite.draw()


window.push_handlers(
    on_text=zpracuj_text,
    on_draw=vykresli
    )

pyglet.clock.schedule_interval(tik, 1/100)
pyglet.app.run()