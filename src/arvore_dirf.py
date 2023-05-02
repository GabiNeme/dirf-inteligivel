import pandas as pd

from src.dicionarios import funde_dicts_mesmas_chaves
from src.no import No

ESTRUTURA_DIRF = {
    "Dirf": ["RESPO", "DECPJ", "RRA", "PSE"],
    "DECPJ": ["IDREC"],
    "IDREC": ["BPFDEC", "BPFRRA"],
    "BPFDEC": [
        "RTRT",
        "RTPO",
        "RTDP",
        "RTIRF",
        "RIIRP",
        "RIMOG",
        "RIP65",
        "RIO",
        "INFPA",
    ],
    "INFPA": ["RTPA"],
    "RRA": ["IDREC"],
    "BPFRRA": ["RTRT", "RTPO", "QTMESES"],
    "PSE": ["OPSE"],
    "OPSE": ["TPSE"],
    "TPSE": ["DTPSE"],
}


class ArvoreDIRF:
    def __init__(self, diretorio_arquivo: str) -> None:
        self.arquivo_dirf = diretorio_arquivo
        self.estrutura = ESTRUTURA_DIRF
        self.raiz = None

    def monta_arvore(self):
        """Cria uma árvore que representa os dados da DIRF.

        Usando a classe No, uma árvore que representa a DIRF é construída. Como o
        arquivo da DIRF é uma impressão pre-ordem da árvore, é possível
        reconstruí-la, utilizando como base seu layout (estrutura)."""

        dirf = open(self.arquivo_dirf, "r", encoding="utf-8-sig")
        linhas = dirf.readlines()

        no_atual = None
        for linha in linhas:
            dado = linha.strip()[:-1].split("|")
            tipo_linha = dado[0]

            if tipo_linha == "Dirf":
                self.raiz = No(None, tipo_linha, dado[1:], self.estrutura)
                no_atual = self.raiz
            elif tipo_linha == "FIMDirf":
                return
            else:
                no_atual = no_atual.adiciona_filho(dado)

    def normaliza_tronco_arvore(self, tipos: list[str]) -> list[dict]:
        """Normaliza os dados de um tronco da árvore em dicionários.

        Considerando os tipos de registro informados, os dados contidos nesse tronco
        são convertidos em dicionários, de forma que os dados dos nós de hierarquia
        mais alta são repetidos em todos os dicionários, e o número de dicionários
        corresponde ao número de folhas.

        Deve ser passada para a função uma lista dos tipos que devem ser impressos,
        desde a raiz até a folha desejada, sem 'pular uma geração', mas podendo deixar
        folhas de lado. Um ramo só será 'impresso' se constar pelo menos uma folha, e a
        raiz sempre deve ser informada. Por exemplo, em uma hierarquia A: [B, C],
        C: [D, E], podem ser passados os tipos [A, C, D] ou [A, B] ou [A, C, D, E], mas
        não [A, D] ou [C, E].

        Caso seja informada [A, C, D, E], serão impressos os dicionários com os dados
        [A, C, D] e [A, C, E].
        """
        resultado = []
        self.raiz.normaliza_tronco_arvore({}, tipos, resultado)
        return resultado

    def converte_em_tabela(self, tipos: list[str], chaves: list[str]) -> pd.DataFrame:
        """Converte a DIRF em uma tabela normalizada.

        Os tipos de linhas da DIRF informados em `tipos` devem seguir a estrutura
        explicada no método `normaliza_tronco_arvore`.

        A partir do dicionário criado pela normalização, serão convertidos em tabelas,
        transformando os diversos dicionários com mesmas chaves em uma única linha,
        como explicado pela função `funde_dicts_mesmas_chaves`.
        """

        dicionarios = self.normaliza_tronco_arvore(tipos=tipos)
        dict_fundidos = funde_dicts_mesmas_chaves(dicionarios, chaves)

        df = pd.DataFrame.from_dict(dict_fundidos, orient="index")
        df.reset_index(drop=True, inplace=True)
        return df
