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


if __name__ == '__main__':
    clients = set()
    addresses = {}
    BUFSIZ = 1024
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = input('Enter host: ')
    PORT = int(input('Enter port: '))
    # HOST = '' # local, same machine
    # PORT = 33000 # local, same machine
    ADDR = (HOST, PORT)
    SERVER.bind(ADDR)
    SERVER.listen(3)
    print('Waiting for connection...')
    ACCEPT_THREAD = threading.Thread(target=accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
