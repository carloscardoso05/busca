import random as rd
from tqdm import trange

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


def hill_climbing_estocastico(iteracoes: int | None = None) -> Posicoes:
    assert iteracoes is None or iteracoes > 0, (
        "O número de iterações deve ser None ou um inteiro positivo"
    )
    posicoes = posicoes_iniciais()
    pontuacao_atual = pontuar_posicoes(posicoes)
    while iteracoes is None or iteracoes > 0:
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
    return posicoes


if __name__ == "__main__":
    max_locais = 0
    max_globais = 0
    total = 2000
    for _ in trange(int(total), desc="Progresso"):
        res = hill_climbing_estocastico()
        if solucao_eh_correta(res):
            max_globais += 1
        else:
            max_locais += 1
    print("Total:", max_globais)
    print("Max globais:", max_globais)
    print("Max locais:", max_locais)
    print(f"Taxa: {(max_globais * 100 / total):.2f}%")
