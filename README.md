# DIRF Inteligível
Converte o arquivo da DIRF em tabelas para facilitar sua análise e comparação.

## Descrição
O arquivo da DIRF é um arquivo cuja a ordem das linhas é relevante, e as linhas subsequentes, sem identificação própria, se referem ao contribuinte de uma linha anterior. Isso dificulta muito qualquer análise e comparação de valores, exigindo que ela seja feita quase manualmente.

Com o intuito de facilitar a comparação entre arquivos da DIRF de diferentes sistemas, o objetivo desse repositório é, em primeiro lugar, convertar a DIRF em uma tabela exportável para Excel ou CSV e, posteriormente, permitir a comparação dessas tabelas.

# Como executar

## A primeira vez
### Crie seu ambiente virtual
```
python -m venv venv
```
### Ative esse ambiente criado no passo anterior.

Para windows:
```
.\venv\Scripts\activate
```

Em Linux e Mac:
```
source venv/bin/activate
```
### Instale os pacotes necessários
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Da segunda vez em diante
Ative o ambiente virtual.

Para windows:
```
.\venv\Scripts\activate
```

Em Linux e Mac:
```
source venv/bin/activate
```

## Como transformar a DIRF em uma tabela

O método `converte_em_tabela` da classe `ArvoreDIRF` é capaz de gerar uma tabela a partir de alguns tipos de linha da DIRF.

Para que a geração seja bem-sucedida, é necessário escolher com cuidado os tipos de linha da DIRF que se deseja, bem como informar as chaves adequadas. Para mais informações, consulte a documentação dos métodos `ArvoreDIRF.normaliza_sub_arvore` e  `ArvoreDIRF.converte_em_tabela`.

### Exemplo com chaves (identificação) em dois níveis

Por exemplo, caso se deseje informações de pensão alimentícia, INFPA e RTPA, é necessário ter também o BPFDEC, que possui os dados do declarante. As chaves devem ser o CPF do declarante (campo BPFDEC_1) e o CPF do beneficiário (campo INFPA_1), conforme mostrado abaixo:
```python
from src.arvore_dirf import ArvoreDIRF

arvore = ArvoreDIRF(diretorio_arquivo_dirf)
arvore.monta_arvore()
df_resultado = arvore.converte_em_tabela(
    tipos=["BPFDEC", "INFPA", "RTPA"], chaves=["BPFDEC_1", "INFPA_1"]
)
```

A variável `df_resultado` é um Dataframe, em que apenas os declarantes que pagam pensão alimentícia terão uma linha para cada beneficiário.

### Exemplo com dois tipos de registros no mesmo declarante

Outro exemplo poderia ser gerar uma tabela com os dados das linhas RTRT e RTIRF, no qual deseja-se que haja apenas uma linha para cada declarante, para isso, poderia-se usar o código:
```python
from src.arvore_dirf import ArvoreDIRF

arvore = ArvoreDIRF(diretorio_arquivo_dirf)
arvore.monta_arvore()
df_resultado = arvore.converte_em_tabela(
    tipos=["BPFDEC", "RTRT", "RTIRF"], chaves=["BPFDEC_1"]
)
```
O resultado é uma linha para cada declarante que possua um registro RTRT ou RTIRF. Caso o declarante não possua algum dos dois registros, constará a variável `np.nan` nas colunas.

### Caso alguma linha desejada não esteja contemplada no código

Se tem algum tipo de registro da DIRF que não está contemplada nesse repositório, altere a variável `ESTRUTURA_DIRF` no arquivo `src/arvore_dirf.py`.

## Rodar os testes
Execute:
```
pytest
```
Para executar os testes e medir sua cobertura, execute:
```
coverage run -m pytest
```
E para avaliar a cobertura dos testes:
```
coverage report -m
coverage html
```
