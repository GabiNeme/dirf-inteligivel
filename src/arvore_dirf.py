from src.no import No

ESTRUTURA_DIRF = {
    "Dirf": ["RESPO", "DECPJ", "PSE"],
    "DECPJ": ["IDREC"],
    "IDREC": ["BPFDEC"],
    "BPFDEC": ["RTRT", "RTPO", "RTIRF", "RIIRP", "RIMOG", "RIP65", "RIO", "INFPA"],
    "INFPA": ["RTPA"],
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
