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




    # ALGORITMO DE MOVIMENTO -------------------------------------


    # Aplicando a operação de movimento (Norte, Sul, Leste, Oeste)
    def aplica_operacao(estado, op):
        des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}
        pos = estado["caminho"][-1]
        passo = (pos[0] + des[op][0], pos[1] + des[op][1])
        novo_caminho = copy.deepcopy(estado["caminho"]) + [passo]
        novo_estado = {"mapa": estado["mapa"], "caminho": novo_caminho}

        return novo_estado

    # Verificar quais movimentos são válidos (não saem do mapa e não colidem com obstáculos)
    def get_operacoes_validas(estado):
        ops_validas = []
        des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}
        pos = estado["caminho"][-1]

        for op, deslocamento in des.items():
            nova_pos = (pos[0] + deslocamento[0], pos[1] + deslocamento[1])
            # Verificar se nova posição é válida (não fora do mapa e sem obstáculos)
            if 0 <= nova_pos[0] < estado["mapa"]["terreno"].shape[0] and 0 <= nova_pos[1] < estado["mapa"]["terreno"].shape[1]:
                if estado["mapa"]["terreno"][nova_pos[0], nova_pos[1]] < 1:  # Não é obstáculo
                    ops_validas.append(op)

        return ops_validas


    # Cálculo do custo (distância percorrida até agora)
    def calc_c(estado):
        return len(estado["caminho"])

    # Cálculo da heurística (distância do fantasminha até o Pacman)
    def calc_h(estado, pacman_pos):
        p = estado["caminho"][-1]
        # Calcular a distância de Manhattan até o Pacman
        return abs(p[0] - pacman_pos[0]) + abs(p[1] - pacman_pos[1])

    # Algoritmo A* para o fantasminha perseguir o Pacman
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

                # Verificar se o fantasminha alcançou o Pacman
                if estado["caminho"][-1] == pacman_pos:
                    return node, quant_estados

        return None, 0  # Se não encontrou resultado



    # /ALGORITMO DE MOVIMENTO -------------------------------------





    # Preenche a tela com branco
    screen.fill(WHITE)

    #desenha mapa
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

   