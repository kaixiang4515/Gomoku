import socket

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '0.0.0.0'
    port = 5555
    server.bind((ip, port))
    server.listen(1)
    print('Listening at {}'.format(server.getsockname()))
    conn, ip_client = server.accept()
    while 1:
        data = conn.recv(65535)
        if len(data) == 0:
            conn.close()
            break
        print('recv: ' + data.decode())
        print('\n')
    
    server.close()

def Client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    port = 5555
    client.connect((ip, port))
    message = 'Hello'
    for i in range(10):
        client.sendall(message.encode())

    client.close()

def main():
    x = int(input('1. Server 2. Client'))
    if x == 1:
        Server()
    elif x == 2:
        Client()

if __name__ == '__main__':
    main()