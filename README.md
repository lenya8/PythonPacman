# Jogo Pacman com IA de Fantasma Usando Algoritmo A*

Este projeto implementa uma versão simples do clássico jogo Pacman utilizando a biblioteca `pygame`. O jogador pode controlar o Pacman, movendo-o pela tela, enquanto é perseguido por um fantasma. O fantasma usa o algoritmo de busca de caminho A* para calcular o caminho mais curto até o Pacman, atualizando sua posição a cada frame.

## Funcionalidades
- **Movimento do Pacman**: O jogador pode mover o Pacman em quatro direções (esquerda, direita, cima e baixo).
- **IA do Fantasma**: O fantasma utiliza o algoritmo de busca de caminho A* para perseguir o Pacman.
- **Busca em Tempo Real**: O fantasma recalcula o caminho mais curto para alcançar o Pacman a cada frame, mantendo a perseguição dinâmica.

## Requisitos
- Python 3.x
- Biblioteca `pygame`

Para instalar a biblioteca necessária, execute:
```bash
pip install pygame
```

## Como Jogar
1. **Controle o Pacman**: Use as setas do teclado para mover o Pacman na direção desejada.
    - Seta Esquerda: Mover para a esquerda
    - Seta Direita: Mover para a direita
    - Seta Cima: Mover para cima
    - Seta Baixo: Mover para baixo
2. **Evite o Fantasma**: O fantasma automaticamente persegue o Pacman calculando o caminho mais curto usando o algoritmo A*. Tente não ser capturado!

## Explicação do Código

### Movimento do Pacman
O Pacman pode se mover para a esquerda, direita, cima e baixo de acordo com as entradas do jogador. O movimento é tratado através dos eventos de teclado capturados pelo `pygame`.

### IA do Fantasma: Algoritmo de Busca A*
O fantasma utiliza o algoritmo de A* para calcular o caminho mais curto até o Pacman. Este algoritmo encontra de forma eficiente o melhor caminho da posição atual do fantasma até a posição do Pacman, levando em conta possíveis obstáculos no mapa.

### Atualizações por Frame
O jogo é atualizado a cada frame, com o fantasma recalculando continuamente o caminho até o Pacman, garantindo que a perseguição seja dinâmica e reaja ao movimento do jogador.

## Executando o Jogo
1. Baixe o código ou clone o repositório.
2. Verifique se você tem Python 3.x e `pygame` instalados.
3. Execute o jogo com o seguinte comando:
   ```bash
   python pacmangame.py
   ```
4. Use as setas do teclado para controlar o Pacman e tente escapar do fantasma!

## Licença
Este projeto é de código aberto e está disponível sob a [Licença MIT](LICENSE). Sinta-se à vontade para usar e modificar o código conforme necessário.