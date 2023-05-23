import argparse

from src.arvore_dirf import ArvoreDIRF

parser=argparse.ArgumentParser()
parser.add_argument(
  "--diretorio_dirf",
  required=True,
)
parser.add_argument(
  "--tipos",
  nargs="*",
  required=True,
)
parser.add_argument(
  "--chaves",
  nargs="*",
  required=True,
)
parser.add_argument(
  "--saida_tabela",
  required=True,
)


def main():

    args = parser.parse_args()

    arvore = ArvoreDIRF(args.diretorio_dirf)
    arvore.monta_arvore()
    df_resultado = arvore.converte_em_tabela(
        tipos=args.tipos, chaves=args.chaves
    )
    df_resultado.to_csv(args.saida_tabela, sep=";")


if __name__ == "__main__":
    main()
