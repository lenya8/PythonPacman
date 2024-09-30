import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import copy

from IPython.display import Image
from matplotlib.animation import FuncAnimation

# Função para mostrar o mapa com o caminho atual
def mostra_mapa_animado(mapa, caminho, ax):
    ncolunas = mapa["terreno"].shape[1]
    nlinhas = mapa["terreno"].shape[0]
    letras = np.array([["" for _ in range(ncolunas)] for _ in range(nlinhas)])

    # Marcando o caminho com "X"
    for passo in caminho:
        letras[passo] = "X"

    # Marcando a entrada e a saída
    letras[mapa["entrada"]] = 'P'  # Pacman
    for ponto in mapa["pontos_coleta"]:
        letras[ponto] = 'o'

    # Exibindo o mapa com seaborn
    ax.clear()
    sns.heatmap(mapa['terreno'], annot=letras, fmt="", cbar=False, cmap="Blues",
                linewidths=0.1, linecolor='black', square=True, ax=ax)

# Configurando o mapa e os obstáculos
def cria_mapa():
    tam_x = 10
    tam_y = 10
    terreno = np.zeros((tam_y, tam_x))  # Cria o mapa vazio
    entrada = (8, 1)  # Posição de entrada

    # Definindo múltiplos pontos de coleta
    pontos_coleta = [(0, 8), (2, 4), (6, 7)]  # Lista de pontos para o Pacman coletar

    # Adicionando obstáculos
    terreno[1, 1:9] = 1 # Paredes na linha 1, colunas 1 a 8
    terreno[3, 1:9] = 1
    terreno[5, 1:9] = 1
    terreno[7, 1:9] = 1

    return {"terreno": terreno, "entrada": entrada, "pontos_coleta": pontos_coleta}

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

# Verificar se o estado atual chegou ao destino
def verifica_resultado(estado):
    ponto_atual = estado["caminho"][-1]
    if ponto_atual in estado["mapa"]["pontos_coleta"]:
        estado["mapa"]["pontos_coleta"].remove(ponto_atual)  # Remove o ponto coletado
        return True
    return False

# Cálculo do custo (distância percorrida até agora)
def calc_c(estado):
    return len(estado["caminho"])

# Cálculo da heurística (distância até a saída)
def calc_h(estado):
    pontos_coleta = estado["mapa"]["pontos_coleta"]
    if not pontos_coleta:  # Se não houver mais pontos, a heurística é 0
        return 0

    p = estado["caminho"][-1]

    # Calcular a distância de Manhattan até o ponto de coleta mais próximo
    distancias = [abs(p[0] - pc[0]) + abs(p[1] - pc[1]) for pc in pontos_coleta]
    return min(distancias)  # Heurística é a menor distância até um ponto de coleta

# Algoritmo A* para encontrar o caminho mais curto
def busca_a_estrela(estado_ini, max_niveis):
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
            f = calc_c(estado) + calc_h(estado)
            node = {'estado': estado, 'f': f}
            folhas.append(node)

            # Verificar se o resultado foi encontrado
            if verifica_resultado(estado):
                return node, quant_estados

    return None, 0  # Se não encontrou resultado

# Função principal para executar a busca A*
def main():
    # Criar o mapa e configurar o estado inicial
    mapa = cria_mapa()
    estado_ini = {"mapa": mapa, "caminho": [mapa["entrada"]]}

    # Configurando a figura e o eixo
    fig, ax = plt.subplots(figsize=(5, 5))

    # Lista de frames para a animação
    frames = []

    # Executar a busca A*
    max_niveis = 100000
    quant_estados_total = 0

    while mapa["pontos_coleta"]:
        res, quant_estados_estrela = busca_a_estrela(estado_ini, max_niveis)
        quant_estados_total += quant_estados_estrela

        if res:
            estado_ini = res["estado"]
            frames.append(copy.deepcopy(estado_ini["caminho"]))  # Salva o estado para a animação
        else:
            print("Caminho não encontrado")
            break

    print(f"Quantidade total de estados explorados: {quant_estados_total}")

    # Função para atualização da animação
    def update(frame):
        mostra_mapa_animado(mapa, frame, ax)

    # Criar a animação
    ani = FuncAnimation(fig, update, frames=frames, repeat=False, interval=300)

    # Exibir a animação
    plt.show()

    ani.save("pacman.gif", writer="imagemagick")


# Executar o programa principal
if __name__ == "__main__":
    main()

#exibe o gif gerado
Image("/content/pacman.gif")

