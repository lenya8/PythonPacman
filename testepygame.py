import pygame
import sys
import numpy as np
import copy

# Inicializa o pygame
pygame.init()

# Dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Movimento com Imagem e A*")

# Cores
WHITE = (255, 255, 255)

# Posição inicial do Pacman
pacman_x = screen_width // 3
pacman_y = screen_height // 3

# Carregar a imagem do Pacman
pacman_image = pygame.image.load("pacman_sprite.png")
pacman_size = (50, 50)  # Tamanho da imagem
pacman_image = pygame.transform.scale(pacman_image, pacman_size)

# Velocidade de movimento do Pacman
speed = 5

# Variáveis para o fantasma
ghost_x = screen_width // 2
ghost_y = screen_height // 2

# Carregar a imagem do Fantasma
ghost_image = pygame.image.load("004__108uf17.webp")
ghost_size = (50, 50)
ghost_image = pygame.transform.scale(ghost_image, ghost_size)

# Dimensões do grid
tam_x = 8
tam_y = 8
terreno = np.zeros((tam_y, tam_x))

# Obstáculos no terreno
terreno[2, 3] = 1
terreno[3, 3] = 1
terreno[5, 3] = 1
terreno[6, 3] = 1
terreno[7, 3] = 1
terreno[2, 5] = 1
terreno[3, 5] = 1
terreno[4, 5] = 1
terreno[5, 5] = 1
terreno[2, 4] = 1

entrada = (7, 4)
saida = (0, 0)
mapa = {"terreno": terreno, "entrada": entrada, "saida": saida}
caminho = []

# Tamanho das células no grid
cellsize = 100

# Funções de conversão de coordenadas
def pixel_para_grid(x, y, cellsize):
    return (y // cellsize, x // cellsize)

def grid_para_pixel(i, j, cellsize):
    return (j * cellsize, i * cellsize)

# Aplicando a operação de movimento (Norte, Sul, Leste, Oeste)
def aplica_operacao(estado, op):
    des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}
    pos = estado["caminho"][-1]
    passo = (pos[0] + des[op][0], pos[1] + des[op][1])
    novo_caminho = copy.deepcopy(estado["caminho"]) + [passo]
    novo_estado = {"mapa": estado["mapa"], "caminho": novo_caminho}

    return novo_estado

# Verificar quais movimentos são válidos
def get_operacoes_validas(estado):
    ops_validas = []
    des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}
    pos = estado["caminho"][-1]

    for op, deslocamento in des.items():
        nova_pos = (pos[0] + deslocamento[0], pos[1] + deslocamento[1])
        # Verificar se nova posição é válida
        if 0 <= nova_pos[0] < estado["mapa"]["terreno"].shape[0] and 0 <= nova_pos[1] < estado["mapa"]["terreno"].shape[1]:
            if estado["mapa"]["terreno"][nova_pos[0], nova_pos[1]] < 1:  # Não é obstáculo
                ops_validas.append(op)

    return ops_validas

# Cálculo do custo
def calc_c(estado):
    return len(estado["caminho"])

# Cálculo da heurística
def calc_h(estado, pacman_pos):
    p = estado["caminho"][-1]
    return abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1])

# Algoritmo A*
def busca_a_estrela(estado_ini, pacman_pos, max_niveis):
    quant_estados = 0
    node_ini = {'estado': estado_ini, 'f': 0}
    folhas = [node_ini]
    nivel = 0

    while nivel < max_niveis:
        nivel += 1

        # Escolher a folha com o menor valor de f
        melhor_folha = min(folhas, key=lambda folha: folha['f'])
        folhas.remove(melhor_folha)

        # Gerar novos estados a partir das operações válidas
        operacoes = get_operacoes_validas(melhor_folha['estado'])
        for op in operacoes:
            estado = aplica_operacao(melhor_folha['estado'], op)
            quant_estados += 1
            f = calc_c(estado) + calc_h(estado, pacman_pos)
            node = {'estado': estado, 'f': f}
            folhas.append(node)

            # Verificar se o fantasma alcançou o Pacman
            if estado["caminho"][-1] == pacman_pos:
                return node, quant_estados

    return None, 0  # Se não encontrou resultado

# Variável para controlar o tempo de movimento do fantasma
tempo_ultimo_movimento = pygame.time.get_ticks()
tempo_movimento = 1000  # Tempo em milissegundos (1 segundo)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Pega a posição do Pacman no grid
    pacman_pos_grid = pixel_para_grid(pacman_x, pacman_y, cellsize)
    
    # Pega a posição atual do Fantasma no grid
    ghost_pos_grid = pixel_para_grid(ghost_x, ghost_y, cellsize)

    # Estado inicial do fantasma
    estado_ini = {"mapa": mapa, "caminho": [ghost_pos_grid]}

    # Calcula o caminho usando o algoritmo A*
    max_niveis = 1000  # Limite de profundidade para o A*
    resultado, _ = busca_a_estrela(estado_ini, pacman_pos_grid, max_niveis)

    # Verifica o tempo desde o último movimento do fantasma
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_ultimo_movimento >= tempo_movimento:
        # Se encontrou um caminho, move o fantasma
        if resultado:
            # Caminho do fantasma até o Pacman
            caminho_ate_pacman = resultado["estado"]["caminho"]

            if len(caminho_ate_pacman) > 1:
                # Próximo passo no caminho (posição do grid)
                proximo_passo_grid = caminho_ate_pacman[1]
                # Converte o próximo passo do grid para a posição em pixels
                ghost_x, ghost_y = grid_para_pixel(proximo_passo_grid[0], proximo_passo_grid[1], cellsize)

        # Atualiza o tempo do último movimento do fantasma
        tempo_ultimo_movimento = tempo_atual

    # Preenche a tela com branco
    screen.fill(WHITE)

    # Desenha o mapa
    for i in range(tam_y):
        for j in range(tam_x):
            if mapa["terreno"][i, j] == 1:
                pygame.draw.rect(screen, (50, 50, 50), (j * cellsize, i * cellsize, cellsize, cellsize))  # parede
            else:
                pygame.draw.rect(screen, (200, 255, 200), (j * cellsize, i * cellsize, cellsize, cellsize))  # fundo

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
