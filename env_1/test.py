import sys, pygame
from pygame.locals import QUIT

def main():
    black = 0, 0, 0
    white = 255, 255, 255
    color_bg = 238, 154, 73
    size = width, height = 670, 670
    button_clicked = False

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('五子棋')

    screen.fill(color_bg)
    font = pygame.font.Font("Fonts/msjh.ttc", 24)
    text = font.render('點這裡', True, black)
    text_clicked = font.render("Clicked", True, black)
    text_rect = text.get_rect(center=(width/2, height/2))
    text_clicked_rect = text_clicked.get_rect(center=(width/2, height/2))

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    button_clicked = True
        
        screen.fill(color_bg)

        if button_clicked:
            pygame.draw.rect(screen, (100, 100, 100), text_clicked_rect)
            screen.blit(text_clicked, text_clicked_rect)
        else:
            pygame.draw.rect(screen, (100, 100, 100), text_rect)
            screen.blit(text, text_rect)
        pygame.display.update()

if __name__ == '__main__':
    main()