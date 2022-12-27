import pygame


def main():
    # Settings
    width = 670
    height = 670
    color_background = (0, 0, 0)
    color_inactive = (100, 100, 200)
    color_active = (200, 200, 255)
    color = color_inactive
    text = ""
    active = False
    running = True

    # Init
    pygame.init()
    pygame.display.set_caption("Input Box Demo")
    screen = pygame.display.set_mode((width, height))

    # Font
    font = pygame.font.Font(None, 32)

    # Input box
    input_box = pygame.Rect(100, 100, 140, 32)

    # Run
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False

                # Change the current color of the input box
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Input box
        text_surface = font.render(text, True, color)
        input_box_width = max(200, text_surface.get_width()+10)
        input_box.w = input_box_width
        input_box.center = (width/2, height/2)

        # Updates
        screen.fill(color_background)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 3)
        pygame.display.flip()


if __name__ == "__main__":
    main()