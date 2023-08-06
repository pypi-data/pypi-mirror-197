"""
@author: xiaofengkz
@date: 2023-2-25
pgzero的template程序（模板文件）
pgzero本身就是pygame的简化版本，但是我——xiaofengkz又把他简化了一下
使用方法:
    :from template import * #必须得这样，否则无法运行
提供方法:
    :template_draw(screen, bg=(255, 255, 255)
    :template_update()
    :template_on_key_down(keys, key)
    :template_on_key_up(keys, key)
    :template_on_key_down_ESCAPE()
    :template_on_mouse_down(mouse, pos, button)
    :template_on_mouse_up(mouse, pos, button)
    :play_music(music_name='bg_music')
    :stop_music()
    :play_sound(sound_name)
How to use them:
    Some examples:
        :def draw():
            template_draw(screen)
        :def update():
            template_update()
        ...and so on

开源包，任何人都可以使用并修改！
"""
import sys
import os
from pgzrun import *
import re

__version__ = '2.4'

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
LETTERS.append('ESCAPE')
LETTERS.append('SPACE')
LETTERS.append('RIGHT')
LETTERS.append('LEFT')
LETTERS.append('UP')
LETTERS.append('DOWN')
# BG = (255, 255, 255)
WIDTH = 1200
HEIGHT = 800

def template_draw(screen, bg=(255, 255, 255)):
    screen.fill(bg)
    for var in mod.__dict__:
        if re.match('draw_.+',var):
            function = getattr(mod,var)
            function(screen)

def template_update():
    for var in mod.__dict__:
        if re.match('update_.+',var):
            function = getattr(mod,var)
            function()
            
def template_on_key_down(keys,key):
    for letter in LETTERS:
        if key == getattr(keys,letter):
            for var in mod.__dict__:
                if var == 'on_key_down_{}'.format(letter):
                    function = getattr(mod,var)
                    function()
                    
def template_on_key_up(keys,key):
    for letter in LETTERS:
        if key == getattr(keys,letter):
            for var in mod.__dict__:
                if var == 'on_key_up_{}'.format(letter):
                    function = getattr(mod,var)
                    function()
                    
def on_key_down_ESCAPE():
    sys.exit()
    
def _none(pos):pass
    
def template_on_mouse_down(mouse,pos,button):
    if button == mouse.LEFT:
        function = getattr(mod,'on_mouse_left_down',_none)
        function(pos)
    if button == mouse.RIGHT:
        function = getattr(mod,'on_mouse_right_down',_none)
        function(pos)
    if button == mouse.MIDDLE:
        function = getattr(mod,'on_mouse_middle_down',_none)
        function(pos)
    
def template_on_mouse_up(mouse,pos,button):
    if button == mouse.LEFT:
        function = getattr(mod,'on_mouse_left_up',_none)
        function(pos)
    if button == mouse.RIGHT:
        function = getattr(mod,'on_mouse_right_up',_none)
        function(pos)
    if button == mouse.MIDDLE:
        function = getattr(mod,'on_mouse_middle_up',_none)
        function(pos)

def play_music(music_name='bg_music'):
    getattr(mod, 'music').play(music_name)
def stop_music(): getattr(mod, 'music').stop()
def play_sound(sound_name):
    getattr(getattr(mod, 'sounds'), sound_name).play()