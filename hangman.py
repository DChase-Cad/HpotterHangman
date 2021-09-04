#pylint: disable=missing-module-docstring
# pylint:disable=invalid-name
# pylint:disable=global-statement
# pylint:disable=unused-variable
# pylint:disable=redefined-outer-name

import random
import os
import math
import pygame
from pygame.constants import KEYDOWN
from words import word_list, descriptions

pygame.init()
pygame.mixer.music.load(os.path.join('assets', 'hedwig.mid'))


# music setup
VOL_NUM = 1
vol_image_rect = (5, 5, 300, 300)
vol_1 = pygame.mixer.music.get_volume()/50
vol_2 = vol_1*10
vol_3 = 1

pygame.mixer.music.set_volume(vol_1)
pygame.mixer.music.play()


# display setup
WIDTH, HEIGHT = 1080, 760
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Harry Potter Hangman!!")

# fonts
LETTER_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 20)
DESC_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 35)
WORD_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 50)
TITLE_FONT = pygame.font.Font(os.path.join('assets', 'HP.ttf'), 90)

# game colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)

# hangman image loading
images = []
for i in range(13, -1, -1):
    image = pygame.image.load(os.path.join(
        'assets', f'hangman{i}.jpg')).convert()
    images.append(image)

# vol images loading
volume_images = []
for i in range(0, 4):
    image = pygame.image.load(os.path.join('assets', f'vol_{i}.jpg')).convert()
    volume_images.append(image)

# global game vars
HIGH_SCORE = 0
ATTEMPTS = 13
HANGMAN_STATUS = 0
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
    print(len(descriptions), len(word_list))
    global HANGMAN_STATUS, WORD_INDEX, WORDS, DESCRIPTION, GUESSED, LETTERS, ATTEMPTS
    LETTERS = []
    for i in range(26):
        x = START_X + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = START_Y + ((i // 13) * (GAP + RADIUS * 2))
        LETTERS.append([x, y, chr(A+i), True])
    DESCRIPTION = descriptions[WORD_INDEX]
    GUESSED = [' ']


def display_message(message, desc):
    '''prints display message to the screen'''
    pygame.time.delay(500)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 - text.get_height()/2))
    text = DESC_FONT.render(desc, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2+text.get_height()))
    pygame.display.update()
    pygame.time.delay(2500)


def set_volume():
    '''sets volume of the game'''
    global VOL_NUM
    if VOL_NUM == 3:
        VOL_NUM = 0
    else:
        VOL_NUM += 1
    if VOL_NUM == 0:
        pygame.mixer.music.set_volume(0)
    if VOL_NUM == 1:
        pygame.mixer.music.set_volume(vol_1)
    if VOL_NUM == 2:
        pygame.mixer.music.set_volume(vol_2)
    if VOL_NUM == 3:
        pygame.mixer.music.set_volume(vol_3)


def title_screen():
    '''displays title screen'''
    global win
    win.fill(WHITE)
    win.fill(WHITE)
    text = TITLE_FONT.render('Harry Potter Hangman', 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 - text.get_height()/2))
    text = DESC_FONT.render(
        'See how many words you can guess before the deed is done.', 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 + 2*text.get_height()))
    text = DESC_FONT.render(
        "Press 'Enter' to begin!!!", 1, RED)
    win.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 + 4*text.get_height()))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == 13:
                return


def gameOver():
    '''game over functionality'''
    global HANGMAN_STATUS, HIGH_SCORE, ATTEMPTS
    print(HANGMAN_STATUS)
    display_message(
        f"Game Over, you achieved a high score of {HIGH_SCORE}!", "Play again? (Y/N)")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == KEYDOWN and event.key >= 97 and event.key <= 122:
                ltr = chr(event.key).upper()
                if ltr == 'N':
                    return False
                elif ltr == 'Y':
                    HANGMAN_STATUS = 0
                    ATTEMPTS = 13
                    HIGH_SCORE = 0
                    WORD_INDEX = random.randint(0, len(word_list)-1)
                    WORDS = word_list[WORD_INDEX].upper()
                    return True


def draw_volume():
    '''draws volume indicator'''
    win.blit(volume_images[VOL_NUM], (5, 5))
    pygame.display.update()


def display():
    '''drawing the assets'''
    win.fill(WHITE)

    # High Score
    text = WORD_FONT.render(f'High Score: {HIGH_SCORE}', 1, BLACK)
    win.blit(text, (800, 40))

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
    # hangman image
    win.blit(images[HANGMAN_STATUS], (50, 200))

    # attempts left
    text = LETTER_FONT.render(f'Remaining Attempts: {ATTEMPTS}', 1, RED)
    win.blit(text, (120, 470))

    draw_volume()
    pygame.display.update()


def main():
    """game loop"""
    global HANGMAN_STATUS, HIGH_SCORE, ATTEMPTS, GUESSED
    FPS = 60
    clock = pygame.time.Clock()
    RUN = True
    while RUN:
        clock.tick(FPS)
        display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 5 < mouse_x < 50 and 5 < mouse_y < 50:
                    set_volume()
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
                            ATTEMPTS -= 1
            if event.type == KEYDOWN:
                if event.key >= 97 and event.key <= 122:
                    ltr = chr(event.key).upper()
                    for letter in LETTERS:
                        if ltr not in GUESSED and letter[2] == ltr:
                            letter[3] = False
                            test = False
                            GUESSED.append(ltr)
                            if ltr in WORDS:
                                test = True
                            if not test:
                                HANGMAN_STATUS += 1
                                ATTEMPTS -= 1
                                display()

        won = True
        for letter in WORDS:
            if letter not in GUESSED:
                won = False
        if won:
            display()
            pygame.time.delay(500)
            display_message(f"You WON! The word was:  {WORDS}", DESCRIPTION)
            RUN = False
            HIGH_SCORE += 1

        if HANGMAN_STATUS == 13:
            display()
            pygame.time.delay(500)
            display_message(f"You lost, the word was:  {WORDS}", DESCRIPTION)
            return False
    word_list.pop(WORD_INDEX)
    descriptions.pop(WORD_INDEX)
    return True


title_screen()
init()
while True:
    WORD_INDEX = random.randint(0, len(word_list)-1)
    WORDS = word_list[WORD_INDEX].upper()
    init()
    if not main():
        if gameOver():
            continue
        else:
            break
pygame.quit()
