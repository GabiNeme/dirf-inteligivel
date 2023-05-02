class No:
    def __init__(self, pai, tipo: str, dados: list[str], estrutura: dict[str]) -> None:
        self.pai = pai
        self.tipo = tipo
        self.estrutura = estrutura
        if self.tipo in self.estrutura:
            self.possiveis_filhos = self.estrutura[self.tipo]
        else:
            self.possiveis_filhos = []
        self.filhos = []
        self.dados = dados

    def adiciona_filho(self, linha: list[str]):
        """Adiciona um novo nó como filho, se for de um tipo possível de ser um nó
        filho do nó corrente. Caso não seja possível respeitar a estrutura no nó atual,
        serão feitas chamadas recursivas para o nó pai, até que se encontre sua posição
        correta."""
        tipo_filho = linha[0]

        if tipo_filho in self.possiveis_filhos:
            no = No(self, tipo_filho, linha[1:], self.estrutura)
            self.filhos.append(no)
            return no

        if self.pai:
            return self.pai.adiciona_filho(linha)

        raise KeyError(
            "O tipo {} não foi encontrado na árvore modelo.".format(tipo_filho)
        )

    def eh_folha(self) -> bool:
        """Verifica se é uma folha, ou seja, se não possui nós filhos."""

        return len(self.filhos) == 0

    def dados_como_dict(self) -> dict:
        dados_dict = {}
        for i in range(len(self.dados)):
            dados_dict["{}_{}".format(self.tipo, i + 1)] = self.dados[i]
        return dados_dict

    def normaliza_tronco_arvore(self, prefixo, tipos_pra_imprimir, resultado) -> None:
        if self.tipo not in tipos_pra_imprimir:
            return

        novo_prefixo = prefixo.copy()
        novo_prefixo.update(self.dados_como_dict())

        if self.eh_folha():
            resultado.append(novo_prefixo)
            return

        for filho in self.filhos:
            filho.normaliza_tronco_arvore(novo_prefixo, tipos_pra_imprimir, resultado)
