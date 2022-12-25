# coding: utf-8
import pygame


def main():
    # Settings
    width = 800
    height = 600
    color_bg = (0, 0, 0)
    running = True

    # Init
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rect Demo")

    # Rect(left, top, width, height)
    rect_1 = pygame.Rect(0, 0, 100, 100)
    rect_2 = pygame.Rect(0, 0, 300, 100)
    rect_2.center = (width/2, height/2)

    # Run
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Screen
        screen.fill(color_bg)

        # Draw
        pygame.draw.rect(screen, (100, 100, 100), rect_1)
        pygame.draw.rect(screen, (255, 0, 255), rect_2)
        pygame.draw.rect(screen, (100, 100, 100), rect_1)

        # Updates
        pygame.display.update()


if __name__ == "__main__":
    main()
