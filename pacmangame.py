import pygame
import sys
import numpy as np
import copy

pygame.init()

tamanho_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((tamanho_tela, altura_tela))

pacman_x = 0
pacman_y = 0

imagem_pacman = pygame.image.load("imagens/pacman_direita.png")
pacman_tamanho = (50, 50)
imagem_pacman = pygame.transform.scale(imagem_pacman, pacman_tamanho)

# Velocidade de movimento do Pacman
velicidade_pacman = 5

# Variáveis para o fantasma
fantasma_x = tamanho_tela // 2
fantasma_y = altura_tela // 2
fantasma_velocidade = 2  # Velocidade menor para o fantasma

# Carregar a imagem do Fantasma
imagem_fantasma = pygame.image.load("imagens/fantasma.webp")
fantasma_tamanho = (50, 50)
imagem_fantasma = pygame.transform.scale(imagem_fantasma, fantasma_tamanho)

def sprite_pacman(sprite):
    global imagem_pacman
    imagem_pacman = pygame.image.load(sprite)
    pacman_tamanho = (50, 50)
    imagem_pacman = pygame.transform.scale(imagem_pacman, pacman_tamanho)
    return True

# Dimensões do grid
terreno_eixo_x = 8
terreno_eixo_y = 8

# Definindo obstáculos para criar um labirinto simples
obstaculo = np.zeros((terreno_eixo_y, terreno_eixo_x))
obstaculo[1, 1] = obstaculo[2, 1] = obstaculo[3, 1] = obstaculo[3, 2] = 1
obstaculo[1, 4] = obstaculo[1, 5] = 1
obstaculo[4, 3] = obstaculo[4, 4] = obstaculo[4, 5] = obstaculo[3, 3] = obstaculo[3, 5] = obstaculo[4, 6] = 1
obstaculo[5, 0] = obstaculo[5, 1] = obstaculo[0, 7] = obstaculo[2, 7] = 1

saida = (4, 7)

jogo_encerrado = False  

mapa = {"terreno": obstaculo, "saida": saida}

tamanho_celula = 100

# Converte a posição de pixels para a grade
def pixel_para_grid(x, y, tamanho_celula):
    return (y // tamanho_celula, x // tamanho_celula)

# Converte da grade para pixels
def grid_para_pixel(i, j, tamanho_celula):
    return (j * tamanho_celula, i * tamanho_celula)

def verificar_colisao(x, y):
    # Verificar colisão para os quatro cantos do sprite do Pacman
    pacman_top_esquerda = pixel_para_grid(x, y, tamanho_celula)
    pacman_top_direita = pixel_para_grid(x + pacman_tamanho[0] - 1, y, tamanho_celula)
    pacman_base_esquerda = pixel_para_grid(x, y + pacman_tamanho[1] - 1, tamanho_celula)
    pacman_base_direita = pixel_para_grid(x + pacman_tamanho[0] - 1, y + pacman_tamanho[1] - 1, tamanho_celula)

    # Verifica se os índices estão dentro dos limites do mapa
    for pos in [pacman_top_esquerda, pacman_top_direita, pacman_base_esquerda, pacman_base_direita]:
        if pos[0] < 0 or pos[0] >= mapa["terreno"].shape[0] or pos[1] < 0 or pos[1] >= mapa["terreno"].shape[1]:
            return True  # Considera que houve uma colisão

    # Se qualquer um dos cantos colidir com um obstáculo, retorna True
    if (mapa["terreno"][pacman_top_esquerda[0], pacman_top_esquerda[1]] == 1 or
        mapa["terreno"][pacman_top_direita[0], pacman_top_direita[1]] == 1 or
        mapa["terreno"][pacman_base_esquerda[0], pacman_base_esquerda[1]] == 1 or
        mapa["terreno"][pacman_base_direita[0], pacman_base_direita[1]] == 1):
        return True
    return False

# Função para aplicar a movimentação do fantasma com o algoritmo A*
def aplica_operacao(estado, op):
    des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}
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
        if 0 <= nova_pos[0] < estado["mapa"]["terreno"].shape[0] and 0 <= nova_pos[1] < estado["mapa"]["terreno"].shape[1]:
            if estado["mapa"]["terreno"][nova_pos[0], nova_pos[1]] < 1:  # Não é obstáculo
                ops_validas.append(op)
    return ops_validas

def calc_custo(estado):
    return len(estado["caminho"])

def calc_heuristica(estado, pacman_pos):
    p = estado["caminho"][-1]
    return abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1])

# Função de busca A*
def busca_a_estrela(estado_ini, pacman_pos, max_niveis):
    quant_estados = 0
    node_ini = {'estado': estado_ini, 'f': 0}
    folhas = [node_ini]
    nivel = 0
    while nivel < max_niveis:
        nivel += 1
        f_menor_valor = min(folhas, key=lambda folha: folha['f'])
        folhas.remove(f_menor_valor)
        operacoes = get_operacoes_validas(f_menor_valor['estado'])
        for op in operacoes:
            estado = aplica_operacao(f_menor_valor['estado'], op)
            quant_estados += 1
            f = calc_custo(estado) + calc_heuristica(estado, pacman_pos)
            node = {'estado': estado, 'f': f}
            folhas.append(node)
            if estado["caminho"][-1] == pacman_pos:
                return node, quant_estados
    return None, 0

# Variável para controlar o tempo de movimento do fantasma
tempo_ultimo_movimento = pygame.time.get_ticks()
tempo_movimento = 800  # Tempo em milissegundos

proximo_destino_x = fantasma_x
proximo_destino_y = fantasma_y

def tela_final(texto):
    tela.fill((255, 255, 255))  # Preenche a tela com branco
    fonte = pygame.font.SysFont("Arial", 60)
    superficie_texto = fonte.render(texto, True, (0, 0, 0))  # Texto preto
    retangulo = superficie_texto.get_rect(center=(tamanho_tela // 2, altura_tela // 2))
    tela.blit(superficie_texto, retangulo)
    pygame.display.flip()  # Atualiza a tela
    pygame.time.wait(2000)  # Espera 2 segundos

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Pega as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimenta o Pacman com base nas teclas, mas só se não colidir
    novo_pacman_x, novo_pacman_y = pacman_x, pacman_y

    if keys[pygame.K_LEFT]:
        if not verificar_colisao(pacman_x - velicidade_pacman, pacman_y) and pacman_x - velicidade_pacman >= 0:
            novo_pacman_x -= velicidade_pacman
            sprite_pacman("imagens/pacman_esquerda.png")
    if keys[pygame.K_RIGHT]:
        if not verificar_colisao(pacman_x + velicidade_pacman, pacman_y) and pacman_x + pacman_tamanho[0] + velicidade_pacman <= tamanho_tela:
            novo_pacman_x += velicidade_pacman
            sprite_pacman("imagens/pacman_direita.png")
    if keys[pygame.K_UP]:
        if not verificar_colisao(pacman_x, pacman_y - velicidade_pacman) and pacman_y - velicidade_pacman >= 0:
            novo_pacman_y -= velicidade_pacman
    if keys[pygame.K_DOWN]:
        if not verificar_colisao(pacman_x, pacman_y + velicidade_pacman) and pacman_y + pacman_tamanho[1] + velicidade_pacman <= altura_tela:
            novo_pacman_y += velicidade_pacman

    # Atualiza a posição do Pacman
    pacman_x, pacman_y = novo_pacman_x, novo_pacman_y

    # Converte a posição do Pacman e do fantasma para o grid
    pacman_pos_grid = pixel_para_grid(pacman_x, pacman_y, tamanho_celula)
    fantasma_pos_grid = pixel_para_grid(fantasma_x, fantasma_y, tamanho_celula)

    if pacman_pos_grid == saida:
        print("Você alcançou a saída!")
        tela_final("Você alcançou a saída!")
        pygame.quit()
        sys.exit()

    if pacman_pos_grid == fantasma_pos_grid:
        print("Você perdeu!")
        tela_final("Perdeu")
        pygame.quit() 
        sys.exit() 

    # Estado inicial do fantasma
    estado_ini = {"mapa": mapa, "caminho": [fantasma_pos_grid]}

    # Calcula o caminho usando o algoritmo A*
    max_niveis = 1000  # Limite de profundidade para o A*
    resultado, _ = busca_a_estrela(estado_ini, pacman_pos_grid, max_niveis)

    # Verifica o tempo desde o último movimento do fantasma
    tempo_atual = pygame.time.get_ticks()

    if tempo_atual - tempo_ultimo_movimento >= tempo_movimento:
        # Se encontrou um caminho, define o próximo destino
        if resultado:
            caminho_ate_pacman = resultado["estado"]["caminho"]
            if len(caminho_ate_pacman) > 1:
                proximo_passo_grid = caminho_ate_pacman[1]
                proximo_destino_x, proximo_destino_y = grid_para_pixel(proximo_passo_grid[0], proximo_passo_grid[1], tamanho_celula)

        # Atualiza o tempo do último movimento do fantasma
        tempo_ultimo_movimento = tempo_atual

    # Movimenta o fantasma gradualmente em direção ao próximo destino
    if fantasma_x < proximo_destino_x:
        fantasma_x += fantasma_velocidade
    elif fantasma_x > proximo_destino_x:
        fantasma_x -= fantasma_velocidade

    if fantasma_y < proximo_destino_y:
        fantasma_y += fantasma_velocidade
    elif fantasma_y > proximo_destino_y:
        fantasma_y -= fantasma_velocidade

    # Preenche a tela com branco
    tela.fill((255, 255, 255))

    # Desenha o mapa
    for i in range(terreno_eixo_y):
        for j in range(terreno_eixo_x):
            if mapa["terreno"][i, j] == 1:
                pygame.draw.rect(tela, (50, 50, 50), (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))  # parede
            else:
                pygame.draw.rect(tela, (200, 255, 200), (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))  # fundo
    
    #indica a saída
    saida_pixel_pos = grid_para_pixel(saida[0], saida[1], tamanho_celula)
    pygame.draw.rect(tela, (255, 0, 0), (saida_pixel_pos[0] + tamanho_celula // 2, saida_pixel_pos[1] + tamanho_celula // 2 , tamanho_celula // 2, tamanho_celula // 2))
    
    # Desenha o Pacman
    tela.blit(imagem_pacman, (pacman_x, pacman_y))

    # Desenha o Fantasma
    tela.blit(imagem_fantasma, (fantasma_x, fantasma_y))

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de quadros
    pygame.time.Clock().tick(60)