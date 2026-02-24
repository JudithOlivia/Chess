import pygame 
import sys

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

White = (255, 255, 255)
Black = (0, 0, 0)
Light_brown = (240, 217, 181)
Dark_brown = (181, 136, 99)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            pygame.quit()
            sys.exit()

    for row in range(ROWS):
        for col in range(COLS):
            color = Light_brown if (row + col) % 2 == 0 else Dark_brown 
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    pygame.display.update()