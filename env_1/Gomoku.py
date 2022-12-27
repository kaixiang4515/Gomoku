import sys, pygame
from pygame.locals import QUIT

black = (0, 0, 0)
white = (255, 255, 255)
color_bg = (238, 154, 73)
size = width, height = (670, 670)

def main_page(screen, text_create, text_create_rect, text_join, text_join_rect):
    screen.fill(color_bg)
    pygame.draw.rect(screen, (238, 0, 0), text_create_rect)
    screen.blit(text_create, text_create_rect)
    pygame.draw.rect(screen, (238, 0, 0), text_join_rect)
    screen.blit(text_join, text_join_rect)

def input(screen):
    font = pygame.font.Font("Fonts/msjh.ttc", 32)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = (100, 100, 200)
    color_active = (200, 200, 255)
    color = color_inactive
    text = ""
    active = False

def main():
    state = 0 # 0:main page, 1:create room, 2:join room

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('五子棋')

    font = pygame.font.Font("Fonts/msjh.ttc", 34)
    text_create = font.render('建立房間', True, black)
    text_create_rect = text_create.get_rect(center=(width/2, height/2-100))
    text_join = font.render('加入房間', True, black)
    text_join_rect = text_join.get_rect(center=(width/2, height/2+100))

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_create_rect.collidepoint(event.pos):
                    state = 1
                elif text_join_rect.collidepoint(event.pos):
                    state = 2
            
        if state == 0:
            main_page(screen, text_create, text_create_rect, text_join, text_join_rect)
        elif state == 1:
            screen.fill(color_bg)
        elif state == 2:
            screen.fill(color_bg)

        '''
        if button_clicked:
            pygame.draw.rect(screen, (100, 100, 100), text_clicked_rect)
            screen.blit(text_clicked, text_clicked_rect)
        else:
            pygame.draw.rect(screen, (100, 100, 100), text_rect)
            screen.blit(text, text_rect)
        '''
        pygame.display.update()

if __name__ == '__main__':
    main()