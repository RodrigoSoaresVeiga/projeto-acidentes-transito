# Projeto G2 - Tema 27: Análise de Acidentes de Trânsito no Brasil

Desenvolvido por Rodrigo Soares Veiga.

Disciplina: Linguagem de Programação.

Orientador: Alexandre Neves Louzada.

Este projeto desenvolve uma aplicação analítica para investigar padrões de acidentes de trânsito no Brasil entre 2015 e 2024, usando uma base simulada com 4440 registros.

## Objetivos

* Identificar estados e regiões mais críticas.
* Analisar a evolução temporal dos acidentes.
* Comparar tipos de acidentes e períodos do dia.
* Investigar relação entre chuva, visibilidade e gravidade.
* Disponibilizar um dashboard interativo em Streamlit.

## Estrutura

```text
projeto-acidentes-transito/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_acidentes_transito_brasil.csv
├── notebooks/
│   └── analise_acidentes_transito.ipynb
├── database/
└── imagens/
```

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## KPIs presentes no dashboard

* Total de acidentes
* Total de mortes
* Estado mais crítico
* Tipo de acidente predominante
* Horário mais perigoso
* Taxa média de gravidade

## Links relevantes:

Github, Github Pages, Streamlit e Notebook.

* GitHub: `[https://github.com/RodrigoSoaresVeiga/projeto-acidentes-transito/tree/main]`
* GitHub Pages: `[https://rodrigosoaresveiga.github.io/projeto-acidentes-transito/]`
* Streamlit: `[https://projeto-acidentes-transito-lxikcamfryu24rsv3yndcu.streamlit.app/]`
* Notebook: `[https://colab.research.google.com/drive/1blF-ZztMBgEEmcQ0ckcW6v_wMgkQW01i?usp=sharing]`

## Conclusão

A análise permite priorizar estados, regiões, horários e fatores ambientais que concentram maior risco. O dashboard foi desenhado para apoiar decisões de prevenção, campanhas educativas e planejamento de segurança viária.
