from src.dicionarios import funde_dicts_mesmas_chaves


def test_funde_dicts_mesmas_chaves():
    dicionarios = [
        {"ChaveA": 1, "ChaveB": "2", "C": "DadoC", "D": 45},
        {"ChaveA": 1, "ChaveB": "2", "C": "DadoC", "E": "Nome"},
        {"ChaveA": 2, "ChaveB": "2", "C": "DadoC", "D": 50},
        {"ChaveA": 3, "ChaveB": "4", "C": "DadoC", "D": 50},
        {"ChaveA": 3, "ChaveB": "4", "C": "DadoC", "F": 100},
    ]

    resultado_esperado = {
        (1, "2"): {"ChaveA": 1, "ChaveB": "2", "C": "DadoC", "D": 45, "E": "Nome"},
        (2, "2"): {"ChaveA": 2, "ChaveB": "2", "C": "DadoC", "D": 50},
        (3, "4"): {"ChaveA": 3, "ChaveB": "4", "C": "DadoC", "D": 50, "F": 100},
    }

    assert (
        funde_dicts_mesmas_chaves(dicionarios, ["ChaveA", "ChaveB"])
        == resultado_esperado
    )
