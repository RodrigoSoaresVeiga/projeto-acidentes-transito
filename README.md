# Projeto G2 - Tema 27: An?lise de Acidentes de Tr?nsito no Brasil

Este projeto desenvolve uma aplica??o anal?tica para investigar padr?es de acidentes de tr?nsito no Brasil entre 2015 e 2024, usando uma base simulada com 4440 registros.

## Objetivos

- Identificar estados e regi?es mais cr?ticas.
- Analisar a evolu??o temporal dos acidentes.
- Comparar tipos de acidentes e per?odos do dia.
- Investigar rela??o entre chuva, visibilidade e gravidade.
- Disponibilizar um dashboard interativo em Streamlit.

## Estrutura

```text
projeto-acidentes-transito/
??? app.py
??? requirements.txt
??? README.md
??? index.html
??? dados/
?   ??? simulacao_acidentes_transito_brasil.csv
??? notebooks/
?   ??? analise_acidentes_transito.ipynb
??? database/
??? imagens/
```

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## KPIs presentes no dashboard

- Total de acidentes
- Total de mortes
- Estado mais cr?tico
- Tipo de acidente predominante
- Hor?rio mais perigoso
- Taxa m?dia de gravidade

## Publica??o

Ap?s criar o reposit?rio no GitHub, publique:

- GitHub: `https://github.com/SEU-USUARIO/projeto-acidentes-transito`
- GitHub Pages: habilite Pages usando o arquivo `index.html` na branch principal.
- Streamlit Cloud: conecte o reposit?rio e use `app.py` como arquivo principal.

## Conclus?o

A an?lise permite priorizar estados, regi?es, hor?rios e fatores ambientais que concentram maior risco. O dashboard foi desenhado para apoiar decis?es de preven??o, campanhas educativas e planejamento de seguran?a vi?ria.
