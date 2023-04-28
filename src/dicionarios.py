def funde_dicts_mesmas_chaves(dicionarios: list[dict], chaves: list[str]) -> dict[dict]:
    """Funde em um mesmo dicionario se tiverem mesmas chaves.

    Espera receber uma lista de dicionários que serão convertidos em outra lista de
    dicionários. Caso dois ou mais dicionários compartilhem as mesmas chaves
    informadas, elas serão unidas em um único dicionário. Nesse caso, será suprimida
    a duplicação de campos de mesmo nome e os diferentes serão enfileirados. Todos os
    dicionários devem conter todas as chaves informadas.
    """

    def _extrai_tupla_de_chaves(dic):
        chave_do_dict = []
        for chave in chaves:
            chave_do_dict.append(dic[chave])
        return tuple(chave_do_dict)

    dict_agregado = {}

    for dicionario in dicionarios:
        chave = _extrai_tupla_de_chaves(dicionario)
        if chave in dict_agregado:
            dict_agregado[chave].update(dicionario)
        else:
            dict_agregado[chave] = dicionario
    return dict_agregado
