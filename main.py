import sys

from src.comparador import Comparador


def main():
    if len(sys.argv) < 3:
        print("Execute o comando com `python main.py dirf_arte dirf_aeros`.")
        return

    comparador = Comparador(
        dir_dirf_arte=sys.argv[1],
        dir_dirf_aeros=sys.argv[2],
    )

    comparador.compara_todos()


if __name__ == "__main__":
    main()
