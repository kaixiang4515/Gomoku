import sys, socket, json, threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '0.0.0.0'
port = 0
user = []
ready_cnt = 0
Ready = threading.Event()

def main():
    port = int(input('Port : '))
    print(ip)
    print(port)
    server.bind((ip, port))
    server.listen(2)
    print('Listening at {}'.format(server.getsockname()))

    while 1:
        conn, ip_client = server.accept()
        print('from {}'.format(ip_client), end=' ')
        r_data = conn.recv(65535)
        print('from {} recv: {}'.format(ip_client, r_data.decode()))
        dic = json.loads(r_data.decode())
        s_data = None

        if dic['state'] == 'join':
            if len(user) == 0:
                dic['color'] = 'black'
            else:
                dic['color'] = 'white'
            
            dic['state'] = 'ok'
            id = len(user)+1 #tmp
            dic['id'] = id
            user.append(id)
            s_data = json.dumps(dic).encode()
            conn.sendall(s_data)
            conn.close()
        
        elif dic['state'] == 'exit':
            print('ID: {} exit.'.format(dic['id']))
            conn.close()
            break
        
        elif dic['state'] == 'ready':
            global ready_cnt
            ready_cnt += 1
            if ready_cnt == 2:
                Ready.set()
            Ready.wait()
            dic['state'] = 'black turn'
            s_data = json.dumps(dic).encode()
            conn.sendall(s_data)
            conn.close()
        
        elif dic['state'] == 'black speak':
            dic['state'] = 'white turn'
            s_data = json.dumps(dic).encode()
            conn.sendall(s_data)
            conn.close()
        elif dic['state'] == 'white speak':
            dic['state'] = 'end'
            s_data = json.dumps(dic).encode()
            conn.sendall(s_data)
            conn.close()
            break
        
    server.close()

if __name__ == '__main__':
    a = threading.Thread(target=main)
    b = threading.Thread(target=main)
    a.start()
    b.start()