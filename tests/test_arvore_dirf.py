import pathlib

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
