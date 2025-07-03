from random import getrandbits, randint

def eh_diagonal(candidato: list[int], colA: int, colB: int) -> bool:
    dist = colB - colA
    if candidato[colB] == candidato[colA] + dist or candidato[colB] == candidato[colA] - dist:
        return True
    return False


def fitness(individuo: list[int]) -> int:
    fitness = 0
    for i in range(len(individuo) - 1):
        for j in range(i + 1, len(individuo)):
            if individuo[i] != individuo[j] and not eh_diagonal(individuo, i, j):
                fitness += 1
    return fitness


def gerar_vetor_binario_aleatorio(tam=8):
    return [getrandbits(3) for _ in range(tam)]


def gerar_populacao_aleatoria(tam_populacao: int) -> list[list[int]]:
    return [gerar_vetor_binario_aleatorio() for _ in range(tam_populacao)]


def selecao_roleta(populacao: list[list[int]]) -> list[int]:
    fitness_porcentagem = [fitness(individuo) for individuo in populacao]
    min_fitness = min(fitness_porcentagem) // 2
    fitness_porcentagem = [int((fitness(individuo) - min_fitness) * (100 / (28 - min_fitness))) for individuo in populacao]
    res = []
    while (len(res) < len(populacao)):
        i = randint(0, len(populacao) - 1)
        if randint(0, 99) < fitness_porcentagem[i]:
            res.append(populacao[i])
    return res
    


def cruzamento_corte(individuoA: list[int], individuoB: list[int], taxa_cruzamento: int) -> tuple[list[int]]:
    if randint(0, 99) < taxa_cruzamento:
        ponto_corte = randint(1, len(individuoA) - 2)
        return (individuoA[:ponto_corte] + individuoB[ponto_corte:], individuoB[:ponto_corte] + individuoA[ponto_corte:])
    return individuoA, individuoB


def mutacao(individuo: list[int], taxa_mutacao: int) -> list[int]:
    for i in range(len(individuo)):
        for bit in range(3):
            if randint(0, 99) < taxa_mutacao:
                individuo[i] ^= 1 << bit        
    return individuo


def selecao_elitista(populacao:list[list[int]], nova_geracao: list[list[int]], num_individuos) -> list[list[int]]:
    nova_geracao.sort(key=lambda individuo: fitness(individuo), reverse=True)
    max_fitness_nova_geracao = fitness(nova_geracao[0])
    res = []
    for individuo in populacao:
        if fitness(individuo) > max_fitness_nova_geracao:
            res.append(individuo)
    num_faltantes = len(res)
    for i in range(num_individuos - num_faltantes):
        res.append(nova_geracao[i])
    return res


def algoritmo_genetico(num_individuos=20, taxa_cruzamento=80, taxa_mutacao=3, max_geracao=1000):
    populacao = gerar_populacao_aleatoria(num_individuos)
    fitness_populacao = [fitness(individuo) for individuo in populacao]
    geracao = 0
    while (geracao < max_geracao and max(fitness_populacao) < 28):
        filhos = []
        escolhidos = selecao_roleta(populacao)
        while escolhidos != []:
            a = randint(0, len(escolhidos) - 1)
            indA = escolhidos[a]
            escolhidos.remove(escolhidos[a])
            b = randint(0, len(escolhidos) - 1)
            indB = escolhidos[b]
            escolhidos.remove(escolhidos[b])
            filhoA, filhoB = cruzamento_corte(indA, indB, taxa_cruzamento)
            filhos.append(filhoA)
            filhos.append(filhoB)
        filhos = [mutacao(filho, taxa_mutacao) for filho in filhos]
        populacao = selecao_elitista(populacao, filhos, num_individuos)
        fitness_populacao = [fitness(individuo) for individuo in populacao]
        geracao += 1
    return max([fitness(individuo) for individuo in populacao])


max_global = 0
max_local = 0
for i in range(1000):
    if (algoritmo_genetico() == 28):
        max_global += 1
    else:
        max_local += 1
print(max_global, max_local)
