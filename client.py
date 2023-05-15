import pygame
import socket
import threading
from grid import Grid

import os
os.environ ['SDL_VIDEO_WINDOW_POS'] = '950, 100'

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

#socket para conectar ao servidor
HOST = '127.0.0.1'

PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #indica o tipo de endereço usado pelo socket e o tipo de socket a ser criado

sock.connect((HOST, PORT))
def receive_data():
    global turn
    while True:
        data = sock.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'seuturno':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'X')
        print(data)

print('Conectado ao servidor')

create_thread(receive_data)

white = (240, 240, 240)
surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Jogo da Velha - Cliente')
programIcon = pygame.image.load(os.path.join('res', 'iconIF.png'))
pygame.display.set_icon(programIcon)

grid = Grid()
running = True
player = "O"
turn = False
playing = 'true'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sock.close()
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)

                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'seuturno', playing)
                    sock.send(send_data.encode())
                    turn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                #playing = True
            elif event.key == pygame.K_ESCAPE:
                running = False
                #print('===============')
                #grid.print_grid()
                #print('===============')

    surface.fill(white)
    grid.draw(surface)

    pygame.display.flip()
