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

Para que a geração seja bem-sucedida, é necessário informar todos os tipos que se deseja na tabela, sendo obrigatório informar da "raiz" à "folha", ou seja,  sempre devemos informar o tipo "Dirf" e pelo menos um tipo que não tenha informações aninhadas (ex: RTRT). Se não for informado nenhum tipo folha, nada será gerado (ex: se informar os tipos [Dirf, DECPJ, IDREC, BPFDEC], nada será gerado).

É necessário também informar as chaves, ou seja, os elementos que são capazes de identificar uma linha como única.

Para mais informações, consulte a documentação dos métodos `ArvoreDIRF.normaliza_tronco_arvore` e  `ArvoreDIRF.converte_em_tabela`.

### Exemplo com chaves (identificação) em dois níveis

Por exemplo, caso se deseje informações de pensão alimentícia, INFPA e RTPA, é necessário informar todos os tipos anteriores, ou seja, Dirf, DECPJ, IDREC e BPFDEC. As chaves devem ser o CPF do declarante (campo BPFDEC_1) e o CPF do beneficiário (campo INFPA_1), conforme mostrado abaixo:
```python
from src.arvore_dirf import ArvoreDIRF

arvore = ArvoreDIRF(diretorio_arquivo_dirf)
arvore.monta_arvore()
df_resultado = arvore.converte_em_tabela(
    tipos=["Dirf", "DECPJ", "IDREC", "BPFDEC", "INFPA", "RTPA"], chaves=["BPFDEC_1", "INFPA_1"]
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
    tipos=["Dirf", "DECPJ", "IDREC", "BPFDEC", "RTRT", "RTIRF"], chaves=["BPFDEC_1"]
)
```
O resultado é uma linha para cada declarante que possua um registro RTRT ou RTIRF. Caso o declarante não possua algum dos dois registros, constará a variável `np.nan` nas colunas.

### Caso alguma linha desejada não esteja contemplada no código

Se tem algum tipo de registro da DIRF que não está contemplada nesse repositório, altere a variável `ESTRUTURA_DIRF` no arquivo `src/arvore_dirf.py`.

## Como comparar informações da DIRF
Foi criado um comparador automático, que utiliza a estrutura da DIRF especificada no tópico anterior e compara:
- Rendimentos do declarante
- Pensão alimentícia
- RRA
- Plano de saúde

Para cada tópico são gerados 4 arquivos:
- Relatório em inglês com os 10 primeiros exemplos de cada diferença encontrada.
- Interseção: comparação 1 a 1 de todas as linhas que aparecem no Arte e no Aeros
- Só em 1: linhas que só aparecem no Arte
- Só em 2: linhas que só aparecem no Aeros

Para executar, basta digitar:
```
python main.py diretorio_dirf_arte diretorio_dirf_aeros
```
Exemplo:
```
python main.py dirf_arte.txt dirf_aeros.txt
```

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
