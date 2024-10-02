import pygame
import sys

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
pacman_image = pygame.image.load("001__31cj05.webp")
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
    if ghost_x < pacman_x:
        ghost_x += 1  # O fantasma se move para a direita
    elif ghost_x > pacman_x:
        ghost_x -= 1  # O fantasma se move para a esquerda

    if ghost_y < pacman_y:
        ghost_y += 1  # O fantasma se move para baixo
    elif ghost_y > pacman_y:
        ghost_y -= 1  # O fantasma se move para cima
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

    # Preenche a tela com branco
    screen.fill(WHITE)

    # Desenha o Pacman
    screen.blit(pacman_image, (pacman_x, pacman_y))

    # Desenha o Fantasma
    screen.blit(ghost_image, (ghost_x, ghost_y))

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de quadros
    pygame.time.Clock().tick(60)
