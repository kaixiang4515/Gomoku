import sys, pygame, socket, json
from pygame.locals import QUIT

black = (0, 0, 0)
white = (255, 255, 255)
color_bg = (238, 154, 73)
size = width, height = (670, 670)
ip = ''
port = 0

def main_page(screen, text_create, text_create_rect, text_join, text_join_rect):
    screen.fill(color_bg)
    pygame.draw.rect(screen, (238, 0, 0), text_create_rect)
    screen.blit(text_create, text_create_rect)
    pygame.draw.rect(screen, (238, 0, 0), text_join_rect)
    screen.blit(text_join, text_join_rect)

def input_box(screen, state):
    font = pygame.font.Font("Fonts/msjh.ttc", 32)
    if state == 1:
        text_box = font.render('port', True, black)
    else:
        text_box = font.render('ip:port', True, black)
    text_rect = text_box.get_rect(center = (width/2, height/2-50))
    input_box = pygame.Rect(100, 100, 140, 42)
    color_inactive = (100, 100, 200)
    color_active = (200, 200, 255)
    color = color_inactive
    text = ''
    active = False

    screen.fill(color_bg)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        text_surface = font.render(text, True, color)
        input_box_width = max(200, text_surface.get_width()+10)
        input_box.w = input_box_width
        input_box.center = (width/2, height/2)

        screen.fill(color_bg)
        screen.blit(text_box, text_rect)
        screen.blit(text_surface, (input_box.x+5, input_box.y))
        pygame.draw.rect(screen, color, input_box, 3)
        pygame.display.flip()

def create_room(screen):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    font = pygame.font.Font("Fonts/msjh.ttc", 34)
    text = font.render('Waiting...', True, black)
    text_rect = text.get_rect(center=(width/2, height/2-100))
    server.bind((ip, port))
    server.listen(1)
    print('Listening at {}'.format(server.getsockname()))
    screen.fill(color_bg)
    screen.blit(text, text_rect)
    pygame.display.update()
    while 1:
        conn, ip_client = server.accept()
        data = server.recv(65535)
        

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
        
        #print(state)
        text = ''
        if state == 0:
            main_page(screen, text_create, text_create_rect, text_join, text_join_rect)
        elif state == 1:
            ip = '0.0.0.0'
            port = input_box(screen, state)
            port = int(port)
            print(ip)
            print(port)
            #state = 0
            create_room(screen)

        elif state == 2:
            ip, port = input_box(screen, state).split(':')
            port = int(port)
            print(ip)
            print(port)
            state = 0

        pygame.display.update()

if __name__ == '__main__':
    main()