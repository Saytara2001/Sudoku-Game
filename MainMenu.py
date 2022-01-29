import pygame
import GUISudokuBacktracking as bt
import GUISudokuDiffrentialEvo as de
from Button import Button

WIDTH = 550
HEIGHT = 650
background_color = (220, 220, 220)
whiteColor = (230, 230, 230)
blackColor = (50, 50, 50)
blueColor = (50, 50, 255)
redColor = (255, 50, 50)

b_backtrack = None
b_differential = None
b_exit = None


def main_menu_init(window):
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    global b_exit, b_backtrack, b_differential
    window.fill(background_color)
    pygame.display.set_caption("Sudoku AI Solver")
    window.fill(background_color)
    logo_image = pygame.image.load("images/sudoku_logo.png")
    logo_image = pygame.transform.scale(logo_image, (WIDTH / 2, WIDTH / 2))
    image_pos_x = (WIDTH / 2) - (logo_image.get_width() / 2)
    window.blit(logo_image, (image_pos_x, 50))
    pygame.display.update()
    b_backtrack.draw_button(True)
    b_differential.draw_button(True)
    b_exit.draw_button(True)


def main():
    global b_exit, b_backtrack, b_differential

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    myFont = pygame.font.SysFont("Comic Sans MS", 35)

    b_backtrack = Button(pygame, window, blueColor, (WIDTH / 2, 375), font=myFont, text="Back track Algorithm",
                         text_color=whiteColor,
                         hover_color_degree=25)
    b_differential = Button(pygame, window, blueColor, (WIDTH / 2, 450), font=myFont, text="Differential Evolution",
                            text_color=whiteColor,
                            hover_color_degree=25)
    b_exit = Button(pygame, window, redColor, (WIDTH / 2, 525), font=myFont, text="Exit",
                    text_color=whiteColor,
                    hover_color_degree=25)
    main_menu_init(window)

    while True:
        b_backtrack.update()
        b_differential.update()
        b_exit.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_backtrack.is_mouse_in():
                    print("I am in backtrack")
                    bt.main()
                    main_menu_init(window)
                if b_differential.is_mouse_in():
                    print("I am in differential")
                    de.main()
                    main_menu_init(window)
                if b_exit.is_mouse_in():
                    print("Exit game")
                    pygame.quit()
                    return


if __name__ == '__main__':
    main()
