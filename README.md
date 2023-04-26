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
