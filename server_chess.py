import socket
import threading

TURN = 'w'

def accept_connection():
    while True:
        client, client_address = SERVER.accept()
        print('{} has connected'.format(client_address))
        addresses[client] = client_address
        clients.add(client)
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    global TURN
    while True:
        move = client.recv(BUFSIZ).decode('utf8')
        TURN = 'w' if TURN == 'b' else 'b'
        for sock in clients:
            sock.send(bytes('{}{}'.format(move, TURN), 'utf8'))

clients = set()
addresses = {}

HOST = ''
PORT = 33001
#     HOST = socket.gethostname() #local
#      PORT = 5000 #temporary port
#      HOST = '192.168.3.108'
#      PORT = 1233
BUFSIZ = 1024
ADDR = (HOST, PORT)

if __name__ == '__main__':
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(3)
    print('Waiting for connection...')
    ACCEPT_THREAD = threading.Thread(target=accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
