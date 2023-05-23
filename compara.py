import argparse

from src.comparador import Comparador

parser=argparse.ArgumentParser()
parser.add_argument(
  "--diretorio_dirf_arte",
  required=True,
)
parser.add_argument(
  "--diretorio_dirf_aeros",
  required=True,
)

def main():

    args = parser.parse_args()

    comparador = Comparador(
        dir_dirf_arte=args.diretorio_dirf_arte,
        dir_dirf_aeros=args.diretorio_dirf_aeros,
    )

    comparador.compara_todos()


if __name__ == "__main__":
    main()
