import pygame
import math
import random
from words import word_list

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
run = True


def main():
    global hangman_status
    global guessed
    global run
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        try:
            clock.tick(FPS)
        except KeyboardInterrupt:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON!")
            break

        if hangman_status == 6:
            display_message_lost("You LOST!", word)
            break
    else:
        pygame.quit()


while run:
    # button variables
    RADIUS = 20
    GAP = 15
    letters = []
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

    # fonts
    LETTER_FONT = pygame.font.SysFont('comicsans', 40)
    WORD_FONT = pygame.font.SysFont('comicsans', 60)
    TITLE_FONT = pygame.font.SysFont('comicsans', 70)
    LAST_FONT = pygame.font.SysFont('comicsans', 50)
    # load images.
    images = []
    for i in range(7):
        image = pygame.image.load("hangman" + str(i) + ".png")
        images.append(image)

    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


    def draw():
        win.fill(WHITE)

        # draw title
        text = TITLE_FONT.render("Guess the Word..", True, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

        # draw word
        display_word = ""
        for letter in word:
            if letter in guessed:
                display_word += letter + " "
            else:
                display_word += "_ "
        text = WORD_FONT.render(display_word, True, BLACK)
        win.blit(text, (400, 200))

        # draw buttons
        for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
                text = LETTER_FONT.render(ltr, True, BLACK)
                win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        win.blit(images[hangman_status], (150, 100))
        pygame.display.update()


    def display_message(message):
        pygame.time.delay(1000)
        win.fill(WHITE)
        text = WORD_FONT.render(message, True, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

        pygame.display.update()
        pygame.time.delay(3000)


    def display_message_lost(message, word):
        pygame.time.delay(1000)
        win.fill(WHITE)
        text = WORD_FONT.render(message, True, BLACK)
        text_2 = LAST_FONT.render(word, True, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        win.blit(text_2, (WIDTH / 2 - text_2.get_width() / 2, (HEIGHT / 2 - text_2.get_height() / 2) + 50))

        pygame.display.update()
        pygame.time.delay(3000)

    hangman_status = 0
    words = word_list
    word = random.choice(words).upper()
    guessed = []

    for letter in letters:
        if letter[3] is not True:
            visible = True
            draw()
    main()

pygame.quit()
