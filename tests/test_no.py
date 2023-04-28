import pytest

from src.no import No


@pytest.fixture
def arvore():
    estrutura = {"A": ["B", "C"], "C": ["D", "E"]}

    raiz = No(pai=None, tipo="A", dados=["DadoA"], estrutura=estrutura)
    no_atual = raiz.adiciona_filho(["B", "DadoB1"])
    no_atual = no_atual.adiciona_filho(["C", "DadoC1"])
    no_atual = no_atual.adiciona_filho(["D", "DadoD1"])
    no_atual = no_atual.adiciona_filho(["B", "DadoB2"])
    no_atual = no_atual.adiciona_filho(["C", "DadoC2"])
    no_atual = no_atual.adiciona_filho(["D", "DadoD2"])
    no_atual = no_atual.adiciona_filho(["E", "DadoE1"])
    return raiz


class TestNo:
    def test_adiciona_filho_ao_pai(self):
        estrutura = {"A": ["B"]}

        raiz = No(pai=None, tipo="A", dados=["DadoA"], estrutura=estrutura)
        no_b = raiz.adiciona_filho(["B", "DadoB"])

        assert raiz.filhos == [no_b]

    def test_estrutura_profundidade_1(self):
        estrutura = {"A": ["B", "C"]}

        raiz = No(pai=None, tipo="A", dados=["DadoA"], estrutura=estrutura)
        no_atual = raiz.adiciona_filho(["B", "DadoB"])
        no_atual = no_atual.adiciona_filho(["C", "DadoC"])

        no_b, no_c = raiz.filhos
        assert no_b.tipo == "B"
        assert no_c.tipo == "C"

    def test_estrutura_profundidade_2(self):
        estrutura = {"A": ["B"], "B": ["C"]}

        raiz = No(pai=None, tipo="A", dados=["DadoA"], estrutura=estrutura)
        no_atual = raiz.adiciona_filho(["B", "DadoB"])
        no_atual = no_atual.adiciona_filho(["C", "DadoC"])

        no_b = raiz.filhos[0]
        no_c = no_b.filhos[0]
        assert no_b.tipo == "B"
        assert no_c.tipo == "C"

    def test_mesmo_tipo_dado_repetido(self):
        estrutura = {"A": ["B"], "B": ["C", "D"]}

        raiz = No(pai=None, tipo="A", dados=["DadoA"], estrutura=estrutura)
        no_atual = raiz.adiciona_filho(["B", "DadoB1"])
        no_atual = no_atual.adiciona_filho(["C", "DadoC1"])
        no_atual = no_atual.adiciona_filho(["D", "DadoD1"])
        no_atual = no_atual.adiciona_filho(["C", "DadoC2"])
        no_atual = no_atual.adiciona_filho(["B", "DadoB2"])
        no_atual = no_atual.adiciona_filho(["C", "DadoC3"])

        no_b1, no_b2 = raiz.filhos
        no_c1, no_d1, no_c2 = no_b1.filhos
        no_c3 = no_b2.filhos[0]
        assert no_b1.dados == ["DadoB1"]
        assert no_b2.dados == ["DadoB2"]
        assert no_c1.dados == ["DadoC1"]
        assert no_c2.dados == ["DadoC2"]
        assert no_c3.dados == ["DadoC3"]
        assert no_d1.dados == ["DadoD1"]

    def test_eh_noh_filho(self):
        estrutura = {"A": ["B"], "B": ["C", "D"]}

        raiz = No(pai=None, tipo="A", dados=["DadoA"], estrutura=estrutura)
        assert raiz.eh_folha()
        no_filho = raiz.adiciona_filho(["B", "DadoB1"])
        assert not raiz.eh_folha()
        assert no_filho.eh_folha()

    def test_dados_como_dict(self):
        dados_array = ["DadoA", "DadoB", "Dado3"]
        no = No(pai=None, tipo="A", dados=dados_array, estrutura={})

        dados_dict_esperado = {
            "A_1": "DadoA",
            "A_2": "DadoB",
            "A_3": "Dado3",
        }

        assert no.dados_como_dict() == dados_dict_esperado

    def test_normalizacao_hierarquias_1_e_2(self, arvore: No):
        tipos_para_imprimir = ["A", "B"]
        resultado = []
        resultado_esperado = [
            {"A_1": "DadoA", "B_1": "DadoB1"},
            {"A_1": "DadoA", "B_1": "DadoB2"},
        ]
        arvore.normaliza_sub_arvore({}, tipos_para_imprimir, resultado)

        assert resultado == resultado_esperado

    def test_normalizacao_hierarquias_1_a_3_com_1_tipo(self, arvore: No):
        tipos_para_imprimir = ["A", "C", "D"]
        resultado = []
        resultado_esperado = [
            {"A_1": "DadoA", "C_1": "DadoC1", "D_1": "DadoD1"},
            {"A_1": "DadoA", "C_1": "DadoC2", "D_1": "DadoD2"},
        ]
        arvore.normaliza_sub_arvore({}, tipos_para_imprimir, resultado)

        assert resultado == resultado_esperado

    def test_normalizacao_hierarquias_1_a_3_com_2_tipos(self, arvore: No):
        tipos_para_imprimir = ["A", "C", "D", "E"]
        resultado = []
        resultado_esperado = [
            {"A_1": "DadoA", "C_1": "DadoC1", "D_1": "DadoD1"},
            {"A_1": "DadoA", "C_1": "DadoC2", "D_1": "DadoD2"},
            {"A_1": "DadoA", "C_1": "DadoC2", "E_1": "DadoE1"},
        ]
        arvore.normaliza_sub_arvore({}, tipos_para_imprimir, resultado)

        assert resultado == resultado_esperado

    def test_normalizacao_hierarquias_2_a_3_com_2_tipos(self, arvore: No):
        tipos_para_imprimir = ["C", "D", "E"]
        resultado = []
        resultado_esperado = [
            {"C_1": "DadoC1", "D_1": "DadoD1"},
            {"C_1": "DadoC2", "D_1": "DadoD2"},
            {"C_1": "DadoC2", "E_1": "DadoE1"},
        ]
        arvore.normaliza_sub_arvore({}, tipos_para_imprimir, resultado)

        assert resultado == resultado_esperado
