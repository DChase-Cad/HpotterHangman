#pylint: disable=missing-module-docstring
#pylint:disable=invalid-name
#pylint:disable=global-statement
#pylint:disable=unused-variable
#pylint:disable=redefined-outer-name

import random
import os
import math
import pygame
from words import word_list, descriptions

pygame.init()
pygame.mixer.music.load(os.path.join('assets','hedwig.mid'))
pygame.mixer.music.play(-1)

# display setup
WIDTH, HEIGHT = 1080, 760
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Harry Potter Hangman!!")

# fonts
LETTER_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 20)
DESC_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 35)
WORD_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 50)

# game colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# hangman image loading
images = []
for i in range(13, -1, -1):
    image = pygame.image.load(os.path.join(
        'assets', f'hangman{i}.jpg')).convert()
    images.append(image)


# global game vars
HANGMAN_STATUS = 6
WORD_INDEX = 0
WORDS = ''
DESCRIPTION = ''
LETTERS = []
RADIUS = 30
GAP = 15
GUESSED = [' ']
A = 65
START_X = round((WIDTH - (RADIUS*2+GAP)*13)/2)
START_Y = 600


def init():
    '''to reset global variables when playing again'''
    global HANGMAN_STATUS, WORD_INDEX, WORDS, DESCRIPTION, GUESSED,LETTERS
    HANGMAN_STATUS = 6
    LETTERS=[]
    for i in range(26):
        x = START_X + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = START_Y + ((i // 13) * (GAP + RADIUS * 2))
        LETTERS.append([x, y, chr(A+i), True])
    WORD_INDEX = random.randint(0, len(word_list)-1)
    WORDS = word_list[WORD_INDEX].upper()
    DESCRIPTION = descriptions[WORD_INDEX]
    GUESSED = [' ']

def display_message(message, desc):
    '''prints display message to the screen'''
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 - text.get_height()/2))
    text = DESC_FONT.render(desc, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2+text.get_height()))
    pygame.display.update()
    pygame.time.delay(6000)

def display():
    '''drawing the assets'''
    win.fill(WHITE)

    # buttons with LETTERS
    for letter in LETTERS:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    # displaying the word
    display_word = ""
    for letter in WORDS:
        if letter in GUESSED:
            display_word += letter + " "
        else:
            display_word += "- "

    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (425, 250))

    win.blit(images[HANGMAN_STATUS], (50, 200))
    pygame.display.update()


def main():
    """game loop"""
    init()
    global GUESSED
    global HANGMAN_STATUS
    FPS = 60
    clock = pygame.time.Clock()
    RUN = True
    while RUN:
        clock.tick(FPS)
        display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                return RUN
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in LETTERS:
                    x, y, ltr, vis = letter
                    distance = math.sqrt((x-mouse_x)**2+(y-mouse_y)**2)
                    if distance < RADIUS and ltr not in GUESSED:
                        letter[3] = False
                        test = False
                        GUESSED.append(ltr)
                        if ltr in WORDS:
                            test = True
                        if not test:
                            HANGMAN_STATUS += 1
            # if event.type==pygame.KEYDOWN:
                #figure out if the key they pressed is a letter
                #if its a letter test if its in guessed
                #if its not in guessed, add to guessed letters
                #if letter is in the word fill in all instances
                #if its not in the word progress the hung man

        won = True
        for letter in WORDS:
            if letter not in GUESSED:
                won = False
        if won:
            display()
            pygame.time.delay(500)
            display_message(f"You WON! The word was:  {WORDS}", DESCRIPTION)
            RUN=False

        if HANGMAN_STATUS == 13:
            display()
            pygame.time.delay(500)
            display_message(f"You lost, the word was:  {WORDS}", DESCRIPTION)
            RUN=False
    return True

while True:
    if not main():
        break
pygame.quit()
