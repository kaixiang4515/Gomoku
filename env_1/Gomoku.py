import sys, pygame, socket, json
import time
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
    global ip, port
    print('In create_room:\n')
    print(ip)
    print(port)
    server.bind((ip, port))
    server.listen(1)
    print('Listening at {}'.format(server.getsockname()))
    screen.fill(color_bg)
    screen.blit(text, text_rect)
    pygame.display.update()

    
    while 1:
        conn, ip_client = server.accept()
        text = font.render('Connected!', True, black)
        text_rect = text.get_rect(center=(width/2, height/2-100))
        screen.fill(color_bg)
        screen.blit(text, text_rect)
        pygame.display.update()
        data = conn.recv(65535)
        conn.close()
        if data.decode() == 'exit':
            break
        print('recv: ' + data.decode())
    
    server.close()
    server = None
    

def join_room(screen):
    message = 'Hello'
    global ip, port
    dic = {
        'color' : None,
        'state' : 'join'
    }

    s_data = json.dumps(dic).encode() #sent data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.sendall(s_data)
    r_data = client.recv(65535) #received data
    print('from {} recv: {}'.format(ip, r_data.decode()))
    client.close()
    dic = json.loads(r_data.decode())

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    dic['state'] = 'ready'
    s_data = json.dumps(dic).encode()
    client.sendall(s_data)
    client.close()

    while 1:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        r_data = client.recv(65535)
        print('from {} recv: {}'.format(ip, r_data.decode()))
        dic = json.loads(r_data.decode())
        if dic['state'] == 'end':
            print('End...')
            client.close()
            break
        elif dic['state'] == 'black turn' and dic['color'] == 'black':
            dic['message'] = 'I am black'
            dic['state'] = 'black speak'
            s_data = json.dumps(dic).encode()
            client.sendall(s_data)
            client.close()
        elif dic['state'] == 'white turn' and dic['color'] == 'white':
            dic['message'] = 'I am white'
            dic['state'] = 'white speak'
            s_data = json.dumps(dic).encode()
            client.sendall(s_data)
            client.close()

    


    '''
    for i in range(3):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.sendall(message.encode())
        data = client.recv(65535)
        print('from {} recv: {}'.format(ip, data.decode()))
        message = data.decode() + '!'
        client.close()
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    message = 'exit'
    client.sendall(message.encode())
    client.close()
    '''

def draw_board(screen):
    screen.fill(color_bg)
    for i in range(27,670,44):
        #先畫豎線
        if i==27 or i==670-27:#邊緣線稍微粗一些
            pygame.draw.line(screen,black,[i,27],[i,670-27],4)
        else:
            pygame.draw.line(screen,black,[i,27],[i,670-27],2)
        #再畫橫線
        if i==27 or i==670-27:#邊緣線稍微粗一些
            pygame.draw.line(screen,black,[27,i],[670-27,i],4)
        else:
            pygame.draw.line(screen,black,[27,i],[670-27,i],2)

    #在棋盤中心畫個小圓表示正中心位置
    pygame.draw.circle(screen, black,[27+44*7,27+44*7], 8,0)
    pygame.display.update()

def play(screen):
    draw_board(screen)
    print("in play()")
    #while 1: pygame.display.update()

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
    global ip, port

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
            port = int(input_box(screen, state))
            print(ip)
            print(port)
            create_room(screen)
            play(screen)
            pygame.display.update()
            time.sleep(3)
            state = 0

        elif state == 2:
            ip, port = input_box(screen, state).split(':')
            port = int(port)
            print(ip)
            print(port)
            join_room(screen)
            play(screen)
            time.sleep(3)
            state = 0

        pygame.display.update()

if __name__ == '__main__':
    main()