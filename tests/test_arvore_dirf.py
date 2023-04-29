import pathlib

import numpy as np
import pandas as pd

from src.arvore_dirf import ArvoreDIRF

DIRF_FIXTURE = str(pathlib.Path().resolve()) + "/tests/fixture/dirf.txt"


class TestArvoreDirf:
    def test_monta_arvore(self):
        arvore = ArvoreDIRF(DIRF_FIXTURE)
        arvore.monta_arvore()

        assert arvore.raiz.tipo == "Dirf"

        respo, decpf, pse = arvore.raiz.filhos
        assert respo.tipo == "RESPO"
        assert decpf.tipo == "DECPJ"
        assert pse.tipo == "PSE"

        idrec = decpf.filhos[0]
        bpfdec1, bpfdec2, bpfdec3 = idrec.filhos
        assert bpfdec1.tipo == "BPFDEC"
        assert bpfdec2.tipo == "BPFDEC"
        assert bpfdec3.tipo == "BPFDEC"
        assert bpfdec3.dados == ["00000000004", "ANDRE", "", "S", "N"]

        rtrt, rtpo, infpa1, infpa2, rtirf, rio = bpfdec3.filhos
        assert rtrt.tipo == "RTRT"
        assert rtpo.tipo == "RTPO"
        assert infpa1.tipo == "INFPA"
        assert infpa2.tipo == "INFPA"
        assert rtirf.tipo == "RTIRF"
        assert rio.tipo == "RIO"

        assert infpa1.dados == ["00000000005", "19701221", "LUCY", "10"]
        assert infpa2.dados == ["00000000056", "19701221", "LUCI", "10"]

        rtpa1 = infpa1.filhos[0]
        rtpa2 = infpa2.filhos[0]
        assert rtpa1.tipo == "RTPA"
        assert rtpa2.tipo == "RTPA"
        assert rtpa1.dados[0] == "79615"
        assert rtpa2.dados[0] == "669615"

        opse = pse.filhos[0]
        tpse1 = opse.filhos[0]
        tpse4 = opse.filhos[3]
        tpse7 = opse.filhos[6]
        assert opse.dados[0] == "16513178000176"
        assert tpse1.dados[0] == "00000000009"
        assert tpse4.dados[0] == "00000000014"
        assert tpse7.dados[0] == "00000000017"

        dtpse1 = tpse7.filhos[0]
        dtpse2 = tpse7.filhos[2]
        assert dtpse1.dados[0] == "00000000018"
        assert dtpse2.dados[0] == "00000000020"

    def test_normalizacao(self):
        arvore = ArvoreDIRF(DIRF_FIXTURE)
        arvore.monta_arvore()
        tipos_para_imprimir = ["BPFDEC", "INFPA", "RTPA"]

        dict_normalizado = arvore.normaliza_sub_arvore(tipos_para_imprimir)

        dict_esperado = [
            {
                "BPFDEC_1": "00000000004",
                "BPFDEC_2": "ANDRE",
                "BPFDEC_3": "",
                "BPFDEC_4": "S",
                "BPFDEC_5": "N",
                "INFPA_1": "00000000005",
                "INFPA_2": "19701221",
                "INFPA_3": "LUCY",
                "INFPA_4": "10",
                "RTPA_1": "79615",
                "RTPA_2": "98017",
                "RTPA_3": "79615",
                "RTPA_4": "107642",
                "RTPA_5": "92625",
                "RTPA_6": "86448",
                "RTPA_7": "94154",
                "RTPA_8": "99233",
                "RTPA_9": "86448",
                "RTPA_10": "86448",
                "RTPA_11": "99695",
                "RTPA_12": "118526",
                "RTPA_13": "86744",
            },
            {
                "BPFDEC_1": "00000000004",
                "BPFDEC_2": "ANDRE",
                "BPFDEC_3": "",
                "BPFDEC_4": "S",
                "BPFDEC_5": "N",
                "INFPA_1": "00000000056",
                "INFPA_2": "19701221",
                "INFPA_3": "LUCI",
                "INFPA_4": "10",
                "RTPA_1": "669615",
                "RTPA_2": "668017",
                "RTPA_3": "79615",
                "RTPA_4": "107642",
                "RTPA_5": "92625",
                "RTPA_6": "86448",
                "RTPA_7": "94154",
                "RTPA_8": "99233",
                "RTPA_9": "86448",
                "RTPA_10": "86448",
                "RTPA_11": "99695",
                "RTPA_12": "118526",
                "RTPA_13": "86744",
            },
        ]

        assert dict_normalizado == dict_esperado

    def test_converte_em_tabela(self):
        arvore = ArvoreDIRF(DIRF_FIXTURE)
        arvore.monta_arvore()
        df_resultado = arvore.converte_em_tabela(
            tipos=["BPFDEC", "RTRT", "RIO"], chaves=["BPFDEC_1"]
        )
        dados_esperados = {
            "BPFDEC_1": ["00000000002", "00000000003", "00000000004", "00000000007"],
            "BPFDEC_2": ["JOAO", "ANNE", "ANDRE", "CELIA"],
            "BPFDEC_3": ["", "", "", ""],
            "BPFDEC_4": ["N", "N", "S", "N"],
            "BPFDEC_5": ["N", "N", "N", "N"],
            "RTRT_1": ["", "202575", "996306", "2872201"],
            "RTRT_2": ["", "270100", "1227045", "2872201"],
            "RTRT_3": ["", "202575", "1347741", "2872201"],
            "RTRT_4": ["", "472676", "996306", "2872201"],
            "RTRT_5": ["", "283605", "1159443", "2872201"],
            "RTRT_6": ["", "222833", "1095937", "2915749"],
            "RTRT_7": ["", "222833", "1192564", "3441173"],
            "RTRT_8": ["", "", "1256240", "3178461"],
            "RTRT_9": ["", "", "1095937", "3178461"],
            "RTRT_10": ["", "", "1095937", "3178461"],
            "RTRT_11": ["408527", "", "1262984", "3178461"],
            "RTRT_12": ["371388", "", "1498773", "3178461"],
            "RTRT_13": ["92847", "146709", "1100242", "3178461"],
            "RIO_1": ["109179", "747670", "903542", np.nan],
            "RIO_2": [
                "Outros Rendimentos Isentos",
                "Outros Rendimentos Isentos",
                "Outros Rendimentos Isentos",
                np.nan,
            ],
        }

        df_esperado = pd.DataFrame(dados_esperados)

        assert df_resultado.equals(df_esperado)
