import pygame
import socket
import threading
from grid import Grid

import os
os.environ ['SDL_VIDEO_WINDOW_POS'] = '200, 100'

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

#Definindo socket para conexão com o cliente
HOST = '127.0.0.1'

PORT = 12345

connection_est = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

#Aguarda Cliente conectar para dar inicio ao jogo
def wait_connection():
    global connection_est, conn, addr
    conn, addr = sock.accept()
    print('Cliente conectado')
    connection_est = True
    receive_data()

#Recebe String com joga do cliente.
def receive_data():
    global turn
    while True:

        data = conn.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])

        if data[2] == 'seuturno':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'O')
        print(data)

create_thread(wait_connection)

#Monta a janela do jogo
white = (240, 240, 240)
surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Jogo da Velha - Servidor')
programIcon = pygame.image.load(os.path.join('res', 'iconIF.png'))
pygame.display.set_icon(programIcon)

grid = Grid()
running = True
player = "X"
turn = True
playing = 'true'


#inicia a tela do jogo, define ações para os eventos e faz o envio de dados ao cliente.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            conn.close()
        if event.type == pygame.MOUSEBUTTONDOWN and connection_est:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'

                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'seuturno', playing)
                    conn.send(send_data.encode())
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = True
            elif event.key == pygame.K_ESCAPE:
                running = False
                #print('===============')
                #grid.print_grid()
                #print('===============')

    surface.fill(white)
    grid.draw(surface)

    pygame.display.flip()
