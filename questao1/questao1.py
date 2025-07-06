import random as rd
from tqdm import trange
import statistics
import time

type Posicoes = list[int] #Posições das rainhas

#Define as posições iniciais das rainhas
def posicoes_iniciais() -> Posicoes:
    return [rd.randint(0, 7) for _ in range(8)]


#Retorna True se a rainha conseguir atacar outra na horizontal
def ataca_horizontal(posicoes: Posicoes, rainha: int) -> bool:
    for outra_rainha in range(8):
        if posicoes[outra_rainha] == posicoes[rainha] and outra_rainha != rainha:
            return True
    return False

#Retorna True se conseguir atacar na diagonal
def ataca_diagonal(posicoes: Posicoes, rainha: int) -> bool:
    linha = posicoes[rainha]
    for outra_rainha in range(0, 8):
        if outra_rainha == rainha:
            continue
        linha_outra_rainha = posicoes[outra_rainha]
        distancia = rainha - outra_rainha
        if (
            linha_outra_rainha == linha + distancia
            or linha_outra_rainha == linha - distancia
        ):
            return True
    return False


#Retorna True se um ataque horizontal ou diagonal funcionarem
def ataca_algum(posicoes: Posicoes, rainha: int) -> bool:
    return ataca_diagonal(posicoes, rainha) or ataca_horizontal(posicoes, rainha)


#Se duas rainhas estiverem na mesma posição, decrementa
def pontuar_posicoes(posicoes: Posicoes) -> int:
    """
    Quanto maior a pontuação, melhor, tente maximizá-la (o máximo é 0)
    """
    n = len(posicoes)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            if posicoes[i] == posicoes[j] or abs(posicoes[i] - posicoes[j]) == abs(
                i - j
            ):
                total -= 1
    return total

#Se nenhuma rainha atacar outra, é a solução
def solucao_eh_correta(posicoes: Posicoes) -> bool:
    return all([not ataca_algum(posicoes, rainha) for rainha in range(8)])

#
def movimentar_rainha(posicoes: Posicoes, rainha: int) -> list[Posicoes]:
    todas_possives_posicoes: list[Posicoes] = []
    for linha in range(8):
        if linha == posicoes[rainha]:
            continue
        novas_posicoes = posicoes[:]
        novas_posicoes[rainha] = linha
        todas_possives_posicoes.append(novas_posicoes)
    return todas_possives_posicoes


def possiveis_posicoes(posicoes: Posicoes) -> list[Posicoes]:
    todas_posicoes: list[Posicoes] = []
    for rainha in range(8):
        todas_posicoes += movimentar_rainha(posicoes, rainha)
    return todas_posicoes


def hill_climbing_estocastico(iteracoes: int | None = None):
    assert iteracoes is None or iteracoes > 0, (
        "O número de iterações deve ser None ou um inteiro positivo"
    )
    posicoes = posicoes_iniciais()
    pontuacao_atual = pontuar_posicoes(posicoes)
    i=0
    while iteracoes is None or iteracoes > 0:
        i+=1
        if iteracoes is not None:
            iteracoes -= 1
        filhos = possiveis_posicoes(posicoes)
        pontuacoes = [pontuar_posicoes(f) for f in filhos]
        melhores = [
            filho
            for filho, pontuacao in zip(filhos, pontuacoes)
            if pontuacao > pontuacao_atual
        ]
        if not melhores:
            break
        posicoes = rd.choice(melhores)
        pontuacao_atual = pontuar_posicoes(posicoes)
        if pontuacao_atual == 0:
            break
    return posicoes, i

if __name__ == "__main__":
    lista_ite = []
    lista_tempo = []
    solucoes = []
    max_locais = 0
    max_globais = 0
    total = 50

    for _ in trange(int(total), desc="Progresso: "):
        inicio = time.perf_counter()
        res, ite = hill_climbing_estocastico()
        fim = time.perf_counter()
        lista_tempo.append(fim-inicio)
        lista_ite.append(ite)
        if solucao_eh_correta(res):
            max_globais += 1
            solucoes.append({"solucao":res, "iteracoes": ite, "tempo": fim-inicio})
        else:
            max_locais += 1

    print("Total:", max_globais)
    print("Max globais:", max_globais)
    print("Max locais:", max_locais)
    print(f"Taxa: {(max_globais * 100 / total):.2f}%")

    #Para as iterações
    print("\n======Sobre as iterações======")
    print(f"Média das iterações: {sum(lista_ite)/total:.2f}")
    desv= statistics.pstdev(lista_ite)
    print(f"Desvio padrão de iterações: {desv:.2f}")

    #Para o tempo
    print("\n======Sobre o tempo de execução======")
    print(f"Média do tempo: {sum(lista_tempo)/total:.6f}s")
    desv_tempo= statistics.pstdev(lista_tempo)
    print(f"Desvio padrão de tempo: {desv_tempo:.6f}s")

    #Melhores soluções
    aux_ord = sorted(solucoes, key=lambda x: (x["iteracoes"], x["tempo"]))
    print("\n====== Cinco melhores soluções ======")
    print(*aux_ord[0:5], sep="\n")
