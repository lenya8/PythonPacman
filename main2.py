import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import copy

from IPython.display import Image
from matplotlib.animation import FuncAnimation

# Função para mostrar o mapa com o caminho atual
def mostra_mapa_animado(mapa, caminho_fantasminha, pacman_pos, ax):
    ncolunas = mapa["terreno"].shape[1]
    nlinhas = mapa["terreno"].shape[0]
    letras = np.array([["" for _ in range(ncolunas)] for _ in range(nlinhas)])


 # Marcando a posição Pacman
    letras[pacman_pos] = "P"

# Marcando o caminho fantasminha com "F"
    for pos in caminho_fantasminha:  # Marcando todas as posições do caminho
        letras[pos] = "F"



   # Exibindo o mapa com seaborn
    ax.clear()
    sns.heatmap(mapa['terreno'], annot=letras, fmt="", cbar=False, cmap="Blues",
                linewidths=0.1, linecolor='black', square=True, ax=ax)

# Configurando o mapa e os obstáculos
def cria_mapa():
    tam_x = 10
    tam_y = 10
    terreno = np.zeros((tam_y, tam_x))  # Cria o mapa vazio


    entrada = (8, 1)  # Posição inicial do fantasminha

    # Definindo a posição inicial do Pacman
    pacman_pos = (0, 8)

    
    # Adicionando obstáculos
    terreno[1, 1:9] = 1 # Paredes na linha 1, colunas 1 a 8
    terreno[3, 1:9] = 1
    terreno[5, 1:9] = 1
    terreno[7, 1:9] = 1

    return {"terreno": terreno, "entrada": entrada, "pacman_pos": pacman_pos}


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


# Função para mover o Pacman aleatoriamente
def move_pacman(mapa, pacman_pos):
    ops_validas = []
    des = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}

    for op, deslocamento in des.items():
        nova_pos = (pacman_pos[0] + deslocamento[0], pacman_pos[1] + deslocamento[1])
        if 0 <= nova_pos[0] < mapa["terreno"].shape[0] and 0 <= nova_pos[1] < mapa["terreno"].shape[1]:
            if mapa["terreno"][nova_pos[0], nova_pos[1]] < 1:  # Não é obstáculo
                ops_validas.append(nova_pos)

    return pacman_pos  # Se não houver movimento válido, o Pacman fica parado



# /ALGORITMO DE MOVIMENTO -------------------------------------



# Função principal para executar a busca A*
def main():
    # Criar o mapa e configurar o estado inicial
    mapa = cria_mapa()
    estado_ini = {"mapa": mapa, "caminho": [mapa["entrada"]]}
    pacman_pos = mapa["pacman_pos"]


    # Configurando a figura e o eixo
    fig, ax = plt.subplots(figsize=(5, 5))

    # Lista de frames para a animação
    frames = []

    # Executar a busca A*
    max_niveis = 100000
    quant_estados_total = 0

    for _ in range(30):  # Loop de tempo para a perseguição
        #pacman_pos = move_pacman(mapa, pacman_pos)  # Mover o Pacman aleatoriamente
        res, quant_estados_estrela = busca_a_estrela(estado_ini, pacman_pos, max_niveis)
        quant_estados_total += quant_estados_estrela

        if res:
            estado_ini = res["estado"]
            frames.append((copy.deepcopy(estado_ini["caminho"]), pacman_pos))  # Salva o estado para a animação
        else:
            print("Fantasminha não encontrou o Pacman")
            break

    print(f"Quantidade total de estados explorados: {quant_estados_total}")

    # Função para atualização da animação
    def update(frame):
        caminho_fantasminha, pacman_pos = frame
        mostra_mapa_animado(mapa, caminho_fantasminha, pacman_pos, ax)
        

    # Criar a animação
    ani = FuncAnimation(fig, update, frames=frames, repeat=False, interval=300)

    # Exibir a animação
    plt.show()

    ani.save("pacman.gif", writer="imagemagick")


# Executar o programa principal
if __name__ == "__main__":
    main()

# Exibe o gif gerado
Image("pacman.gif")