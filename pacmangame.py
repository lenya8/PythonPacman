import pygame
import sys
import numpy as np
import copy

pygame.init()

# Dimensões da tela
tamanho_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((tamanho_tela, altura_tela))
pygame.display.set_caption("Movimento com Imagem e A*")

# Posição inicial do Pacman
pacman_x = 0
pacman_y = 0

pacman_image = pygame.image.load("imagens/pacman_sprite.png")
pacman_tamanho = (50, 50)
pacman_image = pygame.transform.scale(pacman_image, pacman_tamanho)

# Velocidade de movimento do Pacman
velocidade = 5

# Variáveis para o fantasma
fantasma_x = tamanho_tela // 2
fantasma_y = altura_tela // 2

# Carregar a imagem do Fantasma
ghost_image = pygame.image.load("imagens/fantasma.webp")
ghost_size = (50, 50)
ghost_image = pygame.transform.scale(ghost_image, ghost_size)

# Dimensões do grid
terreno_eixo_x = 8
terreno_eixo_y = 8

# Definindo obstáculos para criar um labirinto simples
obstaculo = np.zeros((terreno_eixo_y, terreno_eixo_x))
obstaculo[1, 1] = obstaculo[1, 2] = obstaculo[1, 3] = obstaculo[1, 4] = 1
obstaculo[2, 1] = 1
obstaculo[3, 1] = 1
obstaculo[4, 1] = 1
obstaculo[2, 4] = 1
obstaculo[3, 4] = 1
obstaculo[5, 2] = obstaculo[5, 3] = obstaculo[5, 4] = 1
obstaculo[6, 1] = obstaculo[6, 2] = obstaculo[6, 3] = obstaculo[6, 5] = 1
obstaculo[4, 6] = obstaculo[4, 7] = 1

posicao_inicial = (7, 7)
saida = (5, 7)
mapa = {"terreno": obstaculo, "entrada": posicao_inicial, "saida": saida}
caminho = []

tamanho_celula = 100

# Converte a posição de pixels para posição no grid
def pixel_para_grid(x, y, tamanho_celula):
    return (y // tamanho_celula, x // tamanho_celula)

# Converte a posição do grid para pixels
def grid_para_pixel(i, j, tamanho_celula):
    return (j * tamanho_celula, i * tamanho_celula)

# Verifica se a próxima posição do Pacman é válida
def movimento_valido(x, y, mapa):
    grid_pos = pixel_para_grid(x, y, tamanho_celula)
    return mapa["terreno"][grid_pos[0], grid_pos[1]] == 0  # Retorna True se não for um obstáculo

# Aplica a operação de movimento
def aplica_operacao(estado, op):
    des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)} #(x, y)
    pos = estado["caminho"][-1]
    passo = (pos[0] + des[op][0], pos[1] + des[op][1])
    novo_caminho = copy.deepcopy(estado["caminho"]) + [passo]
    novo_estado = {"mapa": estado["mapa"], "caminho": novo_caminho}
    return novo_estado

# Verifica quais movimentos são válidos
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

def calc_custo(estado):
    return len(estado["caminho"])

def calc_heuristica(estado, pacman_pos):
    p = estado["caminho"][-1]
    return abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1])

# Busca A*
def busca_a_estrela(estado_ini, pacman_pos, max_niveis):
    quant_estados = 0
    node_ini = {'estado': estado_ini, 'f': 0}
    folhas = [node_ini]
    nivel = 0

    while nivel < max_niveis:
        nivel += 1

        # Escolher a folha com o menor valor de f
        f_menor_valor = min(folhas, key=lambda folha: folha['f'])
        folhas.remove(f_menor_valor)

        # Gerar novos estados a partir das operações válidas
        operacoes = get_operacoes_validas(f_menor_valor['estado'])
        for op in operacoes:
            estado = aplica_operacao(f_menor_valor['estado'], op)
            quant_estados += 1
            f = calc_custo(estado) + calc_heuristica(estado, pacman_pos)
            node = {'estado': estado, 'f': f}
            folhas.append(node)

            # Verificar se o fantasma alcançou o Pacman
            if estado["caminho"][-1] == pacman_pos:
                return node, quant_estados

    return None, 0  # Se não encontrou resultado

# Variável para controlar o tempo de movimento do fantasma
tempo_ultimo_movimento = pygame.time.get_ticks()
tempo_movimento = 800  # Tempo em milissegundos

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pacman_pos_grid = pixel_para_grid(pacman_x, pacman_y, tamanho_celula)
    fantasma_pacman_grid = pixel_para_grid(fantasma_x, fantasma_y, tamanho_celula)

    # Estado inicial do fantasma
    estado_ini = {"mapa": mapa, "caminho": [fantasma_pacman_grid]}

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
                fantasma_x, fantasma_y = grid_para_pixel(proximo_passo_grid[0], proximo_passo_grid[1], tamanho_celula)

        # Atualiza o tempo do último movimento do fantasma
        tempo_ultimo_movimento = tempo_atual

    # Preenche a tela com branco
    tela.fill((255, 255, 255))

    # Desenha o mapa
    for i in range(terreno_eixo_y):
        for j in range(terreno_eixo_x):
            if mapa["terreno"][i, j] == 1:
                pygame.draw.rect(tela, (50, 50, 50), (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))  # parede
            else:
                pygame.draw.rect(tela, (200, 255, 200), (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))  # fundo

    # Pega as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimenta o Pacman com base nas teclas, verificando se o movimento é válido
    if keys[pygame.K_LEFT] and movimento_valido(pacman_x - velocidade, pacman_y, mapa):
        pacman_x -= velocidade
    if keys[pygame.K_RIGHT] and movimento_valido(pacman_x + velocidade, pacman_y, mapa):
        pacman_x += velocidade
    if keys[pygame.K_UP] and movimento_valido(pacman_x, pacman_y - velocidade, mapa):
        pacman_y -= velocidade
    if keys[pygame.K_DOWN] and movimento_valido(pacman_x, pacman_y + velocidade, mapa):
        pacman_y += velocidade

    # Desenha o Pacman
    tela.blit(pacman_image, (pacman_x, pacman_y))

    # Desenha o Fantasma
    tela.blit(ghost_image, (fantasma_x, fantasma_y))

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de quadros
    pygame.time.Clock().tick(60)
