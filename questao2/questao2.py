from random import getrandbits, randint
from time import perf_counter

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
    melhor_individuo = []
    max_fitness = 0
    for i in range(num_individuos):
        if fitness_populacao[i] > max_fitness:
            melhor_individuo = populacao[i]
            max_fitness = fitness_populacao[i] 
    return melhor_individuo, max_fitness, geracao


num_iter = 50
melhores_solucoes = []
tempos_exec = []
geracoes = []
media_num_geracoes = 0
media_tempo_exec = 0
for i in range(num_iter):
    temp_ini = perf_counter()
    individuo, individuo_fitness, num_geracoes = algoritmo_genetico()
    tempos_exec.append(perf_counter() - temp_ini)
    media_tempo_exec += tempos_exec[len(tempos_exec) - 1]
    geracoes.append(num_geracoes)
    media_num_geracoes += num_geracoes
    if individuo_fitness == 28 and len(melhores_solucoes) < 5:
        melhores_solucoes.append(individuo)
media_tempo_exec /= num_iter
media_num_geracoes /= num_iter

desvio_tempo_exec = 0
desvio_num_geracoes = 0
for i in range(num_iter):
    desvio_tempo_exec += (tempos_exec[i] - media_tempo_exec) ** 2
    desvio_num_geracoes += (geracoes[i] - media_num_geracoes) ** 2
desvio_tempo_exec = (desvio_tempo_exec / num_iter) ** 0.5
desvio_num_geracoes = (desvio_num_geracoes / num_iter) ** 0.5

print('As 5 melhores soluções:')
print(f'{melhores_solucoes[0]}, {melhores_solucoes[1]}, {melhores_solucoes[2]}, {melhores_solucoes[3]}, {melhores_solucoes[4]}\n')

print(f'A média do tempo de execução: {media_tempo_exec:.2f} segundos')
print(f'O desvio padrão do tempo de execução: {desvio_tempo_exec:.2f} segundos\n')

print(f'A média do número de iterações: {media_num_geracoes:.2f} iterações')
print(f'O desvio padrão do número de iterações: {desvio_num_geracoes:.2f} iterações')

