import unittest
from main import posicoes_iniciais, ataca_horizontal, ataca_diagonal


class Testes(unittest.TestCase):
    def test_posicoes_iniciais(self):
        estado = posicoes_iniciais()
        self.assertEqual(8, len(estado))
        self.assertTrue(all([isinstance(posicao, int) for posicao in estado]))
        print(estado)

    def test_ataca_horizontal(self):
        posicoes = [1, 2, 3, 2, 5, 6, 7, 7]
        #           0  1  2  3  4  5  6  7
        #           F  T  F  T  F  F  T  T
        self.assertFalse(ataca_horizontal(posicoes, 0))
        self.assertTrue(ataca_horizontal(posicoes, 1))
        self.assertFalse(ataca_horizontal(posicoes, 2))
        self.assertTrue(ataca_horizontal(posicoes, 3))
        self.assertFalse(ataca_horizontal(posicoes, 4))
        self.assertFalse(ataca_horizontal(posicoes, 5))
        self.assertTrue(ataca_horizontal(posicoes, 6))
        self.assertTrue(ataca_horizontal(posicoes, 7))

    def test_ataca_diagonal(self):
        posicoes = [7, 3, 5, 2, 3, 4, 1, 3]
        #           0  1  2  3  4  5  6  7
        #           T  F  T  T  T  T  T  F
        self.assertTrue(ataca_diagonal(posicoes, 0))
        self.assertFalse(ataca_diagonal(posicoes, 1))
        self.assertTrue(ataca_diagonal(posicoes, 2))
        self.assertTrue(ataca_diagonal(posicoes, 3))
        self.assertTrue(ataca_diagonal(posicoes, 4))
        self.assertTrue(ataca_diagonal(posicoes, 5))
        self.assertTrue(ataca_diagonal(posicoes, 6))
        self.assertFalse(ataca_diagonal(posicoes, 7))


if __name__ == "__main__":
    unittest.main()
