import pygame
import sys
import numpy as np
# Inicializa o pygame
pygame.init()

# Dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Movimento com Imagem e A*")

# Cores
WHITE = (255, 255, 255)

# Posição inicial do "pacman"
pacman_x = screen_width // 3
pacman_y = screen_height // 3

# Carregar a imagem do Pacman (substitua "pacman.png" pelo caminho da sua imagem)
pacman_image = pygame.image.load("pacman_sprite.png")
pacman_size = (50, 50)  # Tamanho da imagem
pacman_image = pygame.transform.scale(pacman_image, pacman_size)

# Velocidade de movimento do Pacman
speed = 5

# Variáveis para o fantasma (começando fora da tela)
ghost_x = screen_width // 2
ghost_y = screen_height // 2

# Carregar a imagem do Fantasma (substitua "ghost.png" pelo caminho da sua imagem)
ghost_image = pygame.image.load("004__108uf17.webp")
ghost_size = (50, 50)
ghost_image = pygame.transform.scale(ghost_image, ghost_size)

#---------------------------------------------------
tam_x= 8
tam_y= 8
terreno = np.zeros((tam_y, tam_x))
#obstáculos:
terreno[2,3]=1
terreno[3,3]=1
terreno[5,3]=1
terreno[6,3]=1
terreno[7,3]=1
terreno[2,5]=1
terreno[3,5]=1
terreno[4,5]=1
terreno[5,5]=1
terreno[2,4]=1

entrada=(7,4)
saida=(0,0)
mapa={"terreno":terreno,"entrada":entrada,"saida":saida}

caminho=[]
#----------------------------------------------------

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #------------------------------------------------------------
    # Aqui você poderia calcular o caminho do fantasma usando o algoritmo A*
    # Considerando a posição do Pacman como a saída e do Fantasma como a entrada
    # Para esse exemplo, vamos apenas simular o movimento do fantasma em direção ao Pacman.





    #desenha o mapa
        # Preenche a tela com branco
    screen.fill(WHITE)

    ncolunas=mapa["terreno"].shape[1]
    nlinhas=mapa["terreno"].shape[0]
    letras = np.array([["" for _ in range(ncolunas)] for _ in range(nlinhas)])
    for passo in caminho:
        letras[passo]="X"
    letras[mapa["entrada"]]='E'
    letras[mapa["saida"]]='S'

    cellsize=100
    for i in range(nlinhas):
        for j in range(ncolunas):
            if mapa["terreno"][i,j]==1:
                pygame.draw.rect(screen, (50,50,50), (i * cellsize, j * cellsize, cellsize, cellsize)) #parede
            if mapa["terreno"][i,j]==0:
                pygame.draw.rect(screen, (200,255,200), (i * cellsize, j * cellsize, cellsize, cellsize)) #fundo


    

    #------------------------------------------------------------

    # Pega as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimenta o Pacman com base nas teclas
    if keys[pygame.K_LEFT]:
        pacman_x -= speed
    if keys[pygame.K_RIGHT]:
        pacman_x += speed
    if keys[pygame.K_UP]:
        pacman_y -= speed
    if keys[pygame.K_DOWN]:
        pacman_y += speed



    # Desenha o Pacman
    screen.blit(pacman_image, (pacman_x, pacman_y))

    # Desenha o Fantasma
    screen.blit(ghost_image, (ghost_x, ghost_y))

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de quadros
    pygame.time.Clock().tick(60)
