# Resultado esperado
OBJETIVO = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)

# Heurística Hamming
def hamming(estado):
    contador = 0

    # conta quantas peças estão em posições erradas
    for i in range(9):
        if estado[i] != 0:
            if estado[i] != OBJETIVO[i]:
                contador = contador + 1

    return contador

# Heurística Manhattan
def manhattan(estado):
    distancia = 0

    # passa por todos os valores do vetor
    for i in range(9):
        if estado[i] != 0:

            # encontra a posição atual da peça na matriz (3x3)
            linha_atual = i // 3
            coluna_atual = i % 3

            # a posição correta da peça é (peça - 1), pois o vetor começa em índice 0
            valor = estado[i]
            pos_correta = valor - 1

            # encontra a posição correta no qual deve ser colocado a peça na matriz (3x3)
            linha_correta = pos_correta // 3
            coluna_correta = pos_correta % 3

            # soma das distâncias para encontrar quantos movimentos devem ser feitos para colocar a peça no local correto
            distancia = distancia + abs(linha_atual - linha_correta) + abs(coluna_atual - coluna_correta)

    return distancia


# Verificação de solubilidade
def contar_inversoes(estado):
    inversoes = 0

    # remove o espaço vazio 0
    lista = []
    for x in estado:
        if x != 0:
            lista.append(x)

    # conta inversões
    for i in range(8):
        for j in range(i + 1, 8):
            if lista[i] > lista[j]:        # compara se o valor atual da lista é maior que o próximo
                inversoes = inversoes + 1

    return inversoes % 2

# Imprime todos os valores
def imprimir_tabuleiro(estado):
    for i in range(0, 9, 3):
        print("|",estado[i], estado[i+1], estado[i+2],"|")
    print()

def nodos_vizinhos(estado):
    vizinhos = []

    posicao_vazia = estado.index(0) # seleciona a peça vazia (0)

    movimentos = [1, -1, 3, -3]  # movimentos para direita, esquerda, cima e baixo

    for mov in movimentos:
        nova_posicao = posicao_vazia + mov # identifica a nova posição para o vazio

        if 0 <= nova_posicao < 9: # verifica se a nova posição é válida
            if (mov == 1 and posicao_vazia % 3 == 2) or (mov == -1 and posicao_vazia % 3 == 0): # verifica se a peça vazia está na coluna da direita ou da esquerda
                continue
            if (mov == -3 and posicao_vazia // 3 == 0) or (mov == 3 and posicao_vazia // 3 == 2): # verifica se a peça vazia está na linha de cima e ou na de baixo
                continue

            novo_estado = list(estado) # cria uma cópia do estado atual
            novo_estado[posicao_vazia], novo_estado[nova_posicao] = novo_estado[nova_posicao], novo_estado[posicao_vazia] # troca a posição do vazio com a peça vizinha
            vizinhos.append((tuple(novo_estado), 1)) # adiciona o novo estado como vizinho, junto com o custo do movimento (1)

    return vizinhos

def astar(nodo_inicial, nodo_objetivo, heuristica):

    # garante que o nó inicial seja um único elemento
    nodos_expandidos = set([nodo_inicial])
    nodos_fechados = set()

    g = {}  # custo do caminho
    nodos_pais = {}  # nodos que contem ramificações

    g[nodo_inicial] = 0

    nodos_pais[nodo_inicial] = nodo_inicial

    # contador de nós expandidos
    contador_nos_expandidos = 0

    while len(nodos_expandidos) > 0:
        # variavel que guarda o nó parental
        n = None

        # este laço serve para encontrar o caminho com menor valor
        for v in nodos_expandidos:
            if n == None or g[v] + heuristica(v) < g[n] + heuristica(n):
                n = v

        # se ainda não chegou no objetivo, expande os vizinhos
        if n == nodo_objetivo:
            pass

        else:
            # m são os nodos vizinhos
            for (m, custo_caminho) in nodos_vizinhos(n):

                # busca os nós na função que expande os nós
                if m not in nodos_expandidos and m not in nodos_fechados:
                    nodos_expandidos.add(m)
                    nodos_pais[m] = n
                    g[m] = g[n] + custo_caminho
                else:
                    if g[m] > g[n] + custo_caminho:
                        g[m] = g[n] + custo_caminho
                        nodos_pais[m] = n

                        if m in nodos_fechados:
                            nodos_fechados.remove(m)
                            nodos_expandidos.add(m)

        # caso não exista caminho
        if n == None:
            print("Caminho não existe!")
            return None, contador_nos_expandidos

        # verifica se o nó atual é o objetivo
        if n == nodo_objetivo:
            caminho_resultado = []

            while nodos_pais[n] != n:
                caminho_resultado.append(n)
                n = nodos_pais[n]

            caminho_resultado.append(nodo_inicial)

            caminho_resultado.reverse()

            return caminho_resultado, contador_nos_expandidos

        # move o nó atual para fechados
        nodos_expandidos.remove(n)
        nodos_fechados.add(n)

        # conta quantos nós foram expandidos
        contador_nos_expandidos += 1

    print("Caminho não existe!")
    return None, contador_nos_expandidos
'''
# Tabuleiro inicial
inicial = (1, 2, 3,
           4, 5, 6,
           0, 7, 8)

'''
inicial = (1, 3, 6,
           5, 0, 2,
           4, 7, 8)
'''
# tabuleiro sem solução
inicial = (1, 2, 3,
           4, 5, 6,
           8, 7, 0)
'''


print("===== Tabuleiro no estado inicial =====\n")
imprimir_tabuleiro(inicial)

if (contar_inversoes(inicial) != 0) :
    print("O tabuleiro não tem solução!")
else:

    caminho, contador_nos_expandidos = astar(inicial, OBJETIVO, manhattan)

    print("===== Movimentos usando heurística Manhattan =====\n")
    for estado in caminho:
        imprimir_tabuleiro(estado)

    print("============ RESULTADOS ============")
    print("\nUsando a heurística Manhattan:")
    print("Movimentos:", len(caminho) - 1)
    print("Nós expandidos:", contador_nos_expandidos)

    print("\nUsando a heurística Hamming:")
    caminho, contador_nos_expandidos = astar(inicial, OBJETIVO, hamming)
    print("Movimentos:", len(caminho) - 1)
    print("Nós expandidos:", contador_nos_expandidos)
