# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 12:46:57 2019

@author: DJ_Level_3
"""

import pygame
from pygame.transform import scale
from random import randint

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)
    
_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

_cached_text = {}
def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

pygame.init()
screen = pygame.display.set_mode((640, 480))
real = 0
guess = 0
score = 0
i = 0
gameRunning = False
runEnd = False
clock = pygame.time.Clock()
done = False

font_preferences = [
        "Arial",
        "Times New Roman",
        "Papyrus",
        "Comic Sans MS"]

def endRun(score):
    global gameRunning
    global runEnd
    global i
    screen.fill([255, 255, 255])
    text = create_text(str(score), font_preferences, 72, (0, 0, 0))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    gameRunning = False
    runEnd = True
    i = 0
    
    
def genNext():
    screen.fill([255, 255, 255])
    global real
    gen = randint(1, 2)
    if gen == 2:
        ref = 0
    else:
        ref = 1
    rand1 = randint(1, 6)
    rand2 = randint(1, 6)
    words = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]
    if ref == 1:
        if rand1 == rand2:
            real = 0
        else:
            real = 1
        displayWord = words[rand1-1]
        displayCol = rand2
    elif ref == 0:
        real = 0
        displayWord = words[rand1-1]
        displayCol = rand1
    return ReturnValue(displayWord, displayCol)

def displayWordCol(word, col):
    colVal = [(255, 0, 0), (255, 128, 0), (220, 220, 0), (0, 255, 0), (0, 0, 255), (128, 0, 255)]
    i = 16
    screen.fill([255, 255, 255])
    while i >= 5:
        rect=pygame.Rect(0, 0, 640, 480)
        screen.fill([255, 255, 255], rect=rect)
        text = create_text(word, font_preferences, int(72 * i/5), colVal[col-1])
        #scale(text, (text.get_width() * i/5, text.get_height() * i/5))
        rect = pygame.Rect(320 - text.get_width() // 2, 240 - text.get_height() // 2, text.get_width(), text.get_height())
        screen.fill([255, 255, 255], rect=rect)
        screen.blit(text, (rect.left, rect.top))
        pygame.display.update(rect)
        clock.tick(60)
        i = i - 1


def checkNext(real, guess):
    global score
    if real == guess:
        score = score + 1
        e = genNext()
        displayWordCol(e.y0, e.y1)
    else:
        endRun(score)
        
def homeScreen():
    screen.fill(0)
    text = create_text("OpenTV", font_preferences, 72, (100, 100, 100))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))

def helpScreen():
    global gameRunning
    global score
    screen.fill(0)
    text = create_text("Left Click if the Colors Match", font_preferences, 30, (100, 100, 100))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.update()
    for i in range(60):
        clock.tick(60)
    screen.fill(0)
    text = create_text("Rignt Click if they Don't", font_preferences, 30, (100, 100, 100))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.update()
    for i in range(60):
        clock.tick(60)
    screen.fill(0)
    text = create_text("Ready?", font_preferences, 30, (100, 100, 100))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.update()
    for i in range(60):
        clock.tick(60)
    screen.fill(0)
    gameRunning = True
    score = 0
    e = genNext()
    displayWordCol(e.y0, e.y1)

class ReturnValue:
  def __init__(self, y0, y1):
     self.y0 = y0
     self.y1 = y1

homeScreen()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if gameRunning == True:
                        guess = 0
                        checkNext(real, guess)
                    else:
                        helpScreen()
                elif event.button == 3:
                    if gameRunning == True:
                        guess = 1
                        checkNext(real, guess)
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if gameRunning == True:
                        endRun(score)
                    elif gameRunning == False:
                        done = True
                
    
    if runEnd:
        i = i + 1
        if i == 60:
            homeScreen()
            runEnd = False
    
    pygame.display.flip()
    clock.tick(60)