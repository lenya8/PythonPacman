import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def mostra_mapa(mapa,caminho):
  ncolunas=mapa["terreno"].shape[1]
  nlinhas=mapa["terreno"].shape[0]
  letras = np.array([["" for _ in range(ncolunas)] for _ in range(nlinhas)])
  for passo in caminho:
    letras[passo]="X"
  letras[mapa["entrada"]]='E'
  letras[mapa["saida"]]='S'

  plt.figure(figsize=(2, 2))
  sns.heatmap(mapa['terreno'],annot=letras, fmt="", cbar=False, cmap="Blues",
              linewidths=0.1, linecolor='black', square=True)
  plt.show()
  

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


import copy
def aplica_operacao(estado,op):
  ncolunas=estado["mapa"]["terreno"].shape[1]
  nlinhas=estado["mapa"]["terreno"].shape[0]
  pos=estado["caminho"][-1]
  des={"N":(-1,0),"S":(1,0),"L":(0,1),"O":(0,-1)}
  passo=(pos[0]+des[op][0],pos[1]+des[op][1])
  novo_caminho=copy.deepcopy(estado["caminho"])+[passo]
  novo_estado={"mapa":mapa,"caminho":novo_caminho}
  mapa["terreno"][passo]=0.3
  return novo_estado

def get_operacoes_validas(estado):
  ops_validas=[]
  ncolunas=estado["mapa"]["terreno"].shape[1]
  nlinhas=estado["mapa"]["terreno"].shape[0]
  pos=estado["caminho"][-1]
  nova_pos=None;
  ops=["N","S","L","O"]
  des=[(-1,0),(1,0),(0,1),(0,-1)]
  for i in range(len(ops)):
    nova_pos=(pos[0]+des[i][0],pos[1]+des[i][1])
    if nova_pos[0]>=0 and nova_pos[0]<nlinhas and nova_pos[1]>=0 and nova_pos[1]<ncolunas:
      if estado["mapa"]["terreno"][nova_pos[0],nova_pos[1]]<1:
        ops_validas.append(ops[i])
  return ops_validas

def verifica_resultado(estado):
  return estado["mapa"]["saida"]==estado["caminho"][-1]


def calc_c(estado):
  return len(estado["caminho"])

def calc_h(estado):
  s=estado["mapa"]["saida"]
  p=estado["caminho"][-1]
  h= abs(s[0]-p[0])+abs(s[1]-p[1])
  if len(get_operacoes_validas(estado))==0:
    h=h+float('inf'); #se não tem ops válidas h=infinito
  return h


def busca_a_estrela(estado_ini,max_niveis):
  quant_estados=0
  node_ini={'estado':estado_ini,'f':0}
  folhas=[node_ini]
  nivel=0
  while (nivel<max_niveis):
    nivel=nivel+1
    #escolhe a melhor folha (com menor f)
    melhor_folha=folhas[0]
    for folha in folhas:
      if folha["f"]<melhor_folha["f"]:
        melhor_folha=folha
    #-------------------------------
    folhas.remove(melhor_folha)
    operacoes=get_operacoes_validas(melhor_folha["estado"])
    for op in operacoes:
      estado=aplica_operacao(melhor_folha['estado'],op)
      quant_estados=quant_estados+1
      node={'estado':estado, 'f':0}
      f=calc_c(node["estado"])+calc_h(node["estado"])
      node['f']=f
      folhas.append(node)
      if verifica_resultado(estado)==True:
        return node,quant_estados
  return None, 0


estado_ini={"mapa":mapa,"caminho":[mapa["entrada"]]}
max_niveis=100000
res,quant_estados_estrela=busca_a_estrela(estado_ini,max_niveis)
estado=res["estado"]
mostra_mapa(estado["mapa"],estado["caminho"])
print("Quant estados="+str(quant_estados_estrela))


