import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Acidentes de Trânsito no Brasil",
    page_icon="🚗",
    layout="wide"
)

DATA_PATH = Path(__file__).parent / "dados" / "simulacao_acidentes_transito_brasil.csv"


@st.cache_data
def carregar_dados():
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["data"],
        encoding="utf-8"
    )

    df.columns = df.columns.str.strip()

    df["taxa_gravidade"] = (
        (df["mortes"] * 5 + df["feridos"] * 1.5)
        / df["acidentes"].clip(lower=1)
    )

    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)

    return df


def multiselect(label, options, default=None):
    options = sorted(options)
    return st.sidebar.multiselect(
        label,
        options,
        default=default or options
    )


df = carregar_dados()

st.title("Análise de Acidentes de Trânsito no Brasil")

st.caption(
    "Dashboard analítico com dados simulados de acidentes de trânsito entre 2015 e 2024."
)

st.sidebar.header("Filtros")

anos = st.sidebar.slider(
    "Ano",
    int(df["ano"].min()),
    int(df["ano"].max()),
    (
        int(df["ano"].min()),
        int(df["ano"].max())
    )
)

meses = multiselect("Mês", df["mes"].unique())

regioes = multiselect(
    "Região",
    df["regiao"].unique()
)

ufs_disponiveis = (
    df[df["regiao"].isin(regioes)]["uf"]
    .unique()
)

ufs = multiselect(
    "Estado",
    ufs_disponiveis
)

cidades_disponiveis = (
    df[df["uf"].isin(ufs)]["cidade"]
    .unique()
)

cidades = multiselect(
    "Cidade",
    cidades_disponiveis
)

tipos = multiselect(
    "Tipo de acidente",
    df["tipo_acidente"].unique()
)

gravidades = multiselect(
    "Nível de gravidade",
    df["nivel_gravidade"].unique()
)

f = df[
    df["ano"].between(anos[0], anos[1])
    & df["mes"].isin(meses)
    & df["regiao"].isin(regioes)
    & df["uf"].isin(ufs)
    & df["cidade"].isin(cidades)
    & df["tipo_acidente"].isin(tipos)
    & df["nivel_gravidade"].isin(gravidades)
].copy()

if f.empty:
    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )
    st.stop()

total_acidentes = int(f["acidentes"].sum())

total_mortes = int(f["mortes"].sum())

estado_critico = (
    f.groupby("uf")["acidentes"]
    .sum()
    .idxmax()
)

tipo_predominante = (
    f.groupby("tipo_acidente")["acidentes"]
    .sum()
    .idxmax()
)

horario_perigoso = (
    f.groupby("periodo_dia")["mortes"]
    .sum()
    .idxmax()
)

taxa_gravidade = f["taxa_gravidade"].mean()

cols = st.columns(6)

cols[0].metric(
    "Total de acidentes",
    f"{total_acidentes:,}".replace(",", ".")
)

cols[1].metric(
    "Total de mortes",
    f"{total_mortes:,}".replace(",", ".")
)

cols[2].metric(
    "Estado mais crítico",
    estado_critico
)

cols[3].metric(
    "Tipo predominante",
    tipo_predominante
)

cols[4].metric(
    "Horário mais perigoso",
    horario_perigoso
)

cols[5].metric(
    "Taxa média de gravidade",
    f"{taxa_gravidade:.2f}"
)

st.subheader("Evolução temporal")

temporal = (
    f.groupby("ano_mes", as_index=False)[
        ["acidentes", "mortes", "feridos"]
    ]
    .sum()
)

st.plotly_chart(
    px.line(
        temporal,
        x="ano_mes",
        y="acidentes",
        markers=True,
        labels={
            "ano_mes": "Período",
            "acidentes": "Acidentes"
        }
    ),
    use_container_width=True
)

c1, c2 = st.columns(2)

with c1:
    estado = (
        f.groupby("uf", as_index=False)["acidentes"]
        .sum()
        .sort_values(
            "acidentes",
            ascending=False
        )
    )

    st.plotly_chart(
        px.bar(
            estado,
            x="uf",
            y="acidentes",
            color="acidentes",
            color_continuous_scale="Reds",
            title="Acidentes por estado"
        ),
        use_container_width=True
    )

with c2:
    tipo = (
        f.groupby(
            "tipo_acidente",
            as_index=False
        )["acidentes"]
        .sum()
        .sort_values(
            "acidentes",
            ascending=False
        )
    )

    st.plotly_chart(
        px.bar(
            tipo,
            x="tipo_acidente",
            y="acidentes",
            color="tipo_acidente",
            title="Ranking por tipo de acidente"
        ),
        use_container_width=True
    )

c3, c4 = st.columns(2)

with c3:
    ordem = [
        "Madrugada",
        "Manhã",
        "Tarde",
        "Noite"
    ]

    heat = (
        f.pivot_table(
            index="periodo_dia",
            columns="nivel_gravidade",
            values="acidentes",
            aggfunc="sum",
            fill_value=0
        )
        .reindex(ordem)
    )

    st.plotly_chart(
        px.imshow(
            heat,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="OrRd",
            title="Heatmap por horário e gravidade"
        ),
        use_container_width=True
    )

with c4:
    st.plotly_chart(
        px.scatter(
            f,
            x="chuva_mm",
            y="acidentes",
            color="visibilidade",
            size="mortes",
            hover_data=[
                "uf",
                "cidade",
                "tipo_acidente"
            ],
            title="Relação chuva x acidentes"
        ),
        use_container_width=True
    )

st.subheader("Tabela dinâmica")

tabela = f.pivot_table(
    index=[
        "regiao",
        "uf",
        "cidade"
    ],
    columns="nivel_gravidade",
    values="acidentes",
    aggfunc="sum",
    fill_value=0
)

tabela["Total"] = tabela.sum(axis=1)

st.dataframe(
    tabela.sort_values(
        "Total",
        ascending=False
    ),
    use_container_width=True
)

st.subheader("Interpretação dos resultados")

regiao_critica = (
    f.groupby("regiao")["acidentes"]
    .sum()
    .idxmax()
)

vis_critica = (
    f.groupby("visibilidade")["acidentes"]
    .sum()
    .idxmax()
)

st.write(
    f"No recorte selecionado, a região com maior concentração de acidentes é "
    f"*{regiao_critica}*, com destaque para o estado "
    f"*{estado_critico}*. O tipo mais frequente é "
    f"*{tipo_predominante}*, enquanto o período com maior impacto em mortes é "
    f"*{horario_perigoso}*. A condição de visibilidade mais recorrente "
    f"nos registros filtrados é *{vis_critica}*, indicando que fatores "
    f"ambientais devem ser observados em políticas de prevenção."
)

st.subheader("Conclusão executiva")

st.write(
    "A análise indica que a prevenção deve combinar fiscalização em horários críticos, "
    "ações educativas voltadas aos tipos de acidente mais frequentes e monitoramento climático. "
    "Estados e cidades com maior volume devem ser priorizados em campanhas, melhorias de sinalização "
    "e planejamento viário."
)
