from Engine.board import Board
from Engine.draw import Draw
import Engine.info
import Engine.GUItk_LAN
import socket
import threading
import tkinter as tk
from PIL import ImageTk, Image

def receive():
    while True:
        try:
            move = client_socket.recv(BUFSIZ).decode('utf8')
            pos1 = (ord(move[0]) - ord('a'), 7 - int(move[1]))
            pos2 = (ord(move[3]) - ord('a'), 7 - int(move[4]))
            g.board.move(pos1, pos2)
            g.draw_pieces()
            g.turn = move[5]
        except OSError:
            break


def send(event=None):
    if g.res[0]:
        pos1 = g.res[1]
        pos2 = g.res[2]
        pos1_str = '{}{}'.format(chr(pos1[0] + ord('a')), 7 - pos1[1])
        pos2_str = '{}{}'.format(chr(pos2[0] + ord('a')), 7 - pos2[1])
        client_socket.send(bytes('{} {}'.format(pos1_str, pos2_str), 'utf8'))


if __name__ == "__main__":
    BUFSIZ = 1024
    HOST = input('Enter host: ')
    PORT = int(input('Enter port: '))
    Engine.info.COLOR = input('Enter color (w or b): ')
    ADDR = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(ADDR)

    root = tk.Tk()
    icon = ImageTk.PhotoImage(Image.open('Imgs/icon.png'))
    root.tk.call('wm', 'iconphoto', root._w, icon)
    b = Board()
    g = Engine.GUItk_LAN.GUI(root, b)
    g.draw_board()
    g.draw_pieces()
    d = Draw(root)
    g.pack(expand='true')
    d.pack()
    g.canvas.bind('<Button-1>', send, add='+')

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    root.mainloop()
