from typing import Tuple

import datacompy
import pandas as pd

from src.arvore_dirf import ArvoreDIRF


class Comparador:
    def __init__(self, dir_dirf_arte: str, dir_dirf_aeros: str) -> None:
        self.dirf_arte = ArvoreDIRF(dir_dirf_arte)
        self.dirf_aeros = ArvoreDIRF(dir_dirf_aeros)

        self.dirf_arte.monta_arvore()
        self.dirf_aeros.monta_arvore()

    def _remove_colunas(self, df: pd.DataFrame, regex_exp: str):
        if regex_exp:
            return df[df.columns.drop(list(df.filter(regex=regex_exp)))]
        return df

    def _compara_tabelas(
        self,
        tipos: list[str],
        chaves: list[str],
        nome: str,
        remove_colunas_regex: str = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df_dirf_arte = self.dirf_arte.converte_em_tabela(tipos, chaves)
        df_dirf_aeros = self.dirf_aeros.converte_em_tabela(tipos, chaves)

        df_dirf_arte = self._remove_colunas(df_dirf_arte, remove_colunas_regex)
        df_dirf_aeros = self._remove_colunas(df_dirf_aeros, remove_colunas_regex)

        if df_dirf_arte.empty:
            df_dirf_aeros.to_csv("{}_so_em_2.csv".format(nome), index=False, sep=";")
            return
        if df_dirf_aeros.empty:
            df_dirf_arte.to_csv("{}_so_em_1.csv".format(nome), index=False, sep=";")
            return

        compara = datacompy.Compare(
            df1=df_dirf_arte,
            df2=df_dirf_aeros,
            join_columns=chaves,
            df1_name="arte",
            df2_name="aeros",
        )

        relatorio = open("{}_relatorio.txt".format(nome), "w")
        relatorio.write(compara.report())
        relatorio.close()
        compara.intersect_rows.to_csv(
            "{}_interseção.csv".format(nome), index=False, sep=";"
        )
        compara.df1_unq_rows.to_csv("{}_so_em_1.csv".format(nome), index=False, sep=";")
        compara.df2_unq_rows.to_csv("{}_so_em_2.csv".format(nome), index=False, sep=";")

    def compara_rendimentos_declarante(self):
        tipos = [
            "Dirf",
            "DECPJ",
            "IDREC",
            "BPFDEC",
            "RTRT",
            "RTPO",
            "RTIRF",
            "RIIRP",
            "RIMOG",
            "RIP65",
            "RIO",
        ]
        chaves = ["BPFDEC_1"]
        remove_colunas = "^(Dirf|DECPJ)"
        self._compara_tabelas(tipos, chaves, "rendimentos_declarante", remove_colunas)

    def compara_pensao_alimenticia(self):
        tipos = ["Dirf", "DECPJ", "IDREC", "BPFDEC", "INFPA", "RTPA"]
        chaves = ["BPFDEC_1", "INFPA_1"]
        remove_colunas = "^(Dirf|DECPJ)"
        self._compara_tabelas(tipos, chaves, "pensao_alimenticia", remove_colunas)

    def compara_rra(self):
        tipos = ["Dirf", "RRA", "IDREC", "BPFRRA", "RTRT", "RTPO", "QTMESES"]
        chaves = ["BPFRRA_1"]
        remove_colunas = "^(Dirf|RRA)"
        self._compara_tabelas(tipos, chaves, "rra", remove_colunas)

    def compara_plano_saude(self):
        tipos = ["Dirf", "PSE", "OPSE", "TPSE", "DTPSE"]
        chaves = ["OPSE_1", "TPSE_1", "DTPSE_1"]
        remove_colunas = "^Dirf"
        self._compara_tabelas(tipos, chaves, "plano_saude", remove_colunas)

    def compara_todos(self):
        self.compara_rendimentos_declarante()
        self.compara_pensao_alimenticia()
        self.compara_rra()
        self.compara_plano_saude()
