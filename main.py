import random as rd

type Posicoes = list[int]


def posicoes_iniciais() -> Posicoes:
    return [rd.randint(0, 7) for _ in range(8)]


def ataca_horizontal(posicoes: Posicoes, rainha: int) -> bool:
    for outra_rainha in range(8):
        if posicoes[outra_rainha] == posicoes[rainha] and outra_rainha != rainha:
            return True
    return False


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


def ataca_algum(posicoes: Posicoes, rainha: int) -> bool:
    return ataca_diagonal(posicoes, rainha) or ataca_horizontal(posicoes, rainha)


# def pontuar_posicoes(posicoes: Posicoes) -> int:
#     pontos = 0
#     for rainha in range(8):
#         if not ataca_algum(posicoes, rainha):
#             pontos += 1
#     return pontos

def pontuar_posicoes(posicoes: Posicoes) -> int:
    n = len(posicoes)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            if posicoes[i] == posicoes[j] or abs(posicoes[i] - posicoes[j]) == abs(i - j):
                total -= 1
    return total


def solucao_eh_correta(posicoes: Posicoes) -> bool:
    return all([not ataca_algum(posicoes, rainha) for rainha in range(8)])


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


def hill_climbing() -> Posicoes:
    posicoes = posicoes_iniciais()
    while True:
        filhos = possiveis_posicoes(posicoes)
        candidatos = [filho for filho in filhos if pontuar_posicoes(filho) > pontuar_posicoes(posicoes)]
        if not candidatos:
            print("melhor:", posicoes)
            print("pontos:", pontuar_posicoes(posicoes))
            print("correta:", solucao_eh_correta(posicoes))
            for linha in range(8):
                row = ["R" if posicoes[coluna] == linha else "□" for coluna in range(8)]
                print(" ".join(row))
            return posicoes
        sucessor = rd.choice(candidatos)
        posicoes = sucessor


if __name__ == "__main__":
    print(hill_climbing())