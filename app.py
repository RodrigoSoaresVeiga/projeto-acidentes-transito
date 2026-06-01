import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Acidentes de Trânsito no Brasil",
    page_icon="🚦",
    layout="wide"
)

DATA_PATH = Path(_file_).parent / "dados" / "simulacao_acidentes_transito_brasil.csv"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #780000 0%, #c1121f 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 42px 46px;
        border-radius: 28px;
        background: linear-gradient(135deg, #780000, #c1121f);
        color: white;
        margin-bottom: 32px;
        box-shadow: 0 18px 45px rgba(120, 0, 0, 0.25);
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        right: -80px;
        top: -80px;
    }

    .hero h1 {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -1px;
    }

    .hero p {
        color: #e5e7eb;
        font-size: 17px;
        max-width: 900px;
        line-height: 1.8;
    }

    .tag {
        display: inline-block;
        padding: 8px 16px;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 999px;
        margin-bottom: 16px;
        font-size: 14px;
        font-weight: 500;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 22px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
        border: 1px solid #e5e7eb;
    }

    div[data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-size: 14px !important;
    }

    div[data-testid="stMetricValue"] {
        color: #c1121f;
        font-weight: 800;
    }

    .block-title {
        font-size: 26px;
        font-weight: 800;
        color: #780000;
        margin: 28px 0 12px 0;
    }

    .insight-box {
        background: white;
        padding: 28px;
        border-radius: 22px;
        border-left: 7px solid #c1121f;
        box-shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
        color: #4b5563;
        line-height: 1.8;
        font-size: 16px;
        margin-top: 14px;
    }

    .footer-box {
        text-align: center;
        padding: 26px;
        border-radius: 22px;
        background: #111827;
        color: #d1d5db;
        margin-top: 36px;
    }

    .footer-box strong {
        color: white;
    }

    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
    }

    h1, h2, h3 {
        color: #780000;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_PATH, parse_dates=["data"], encoding="utf-8")

    df["taxa_gravidade"] = (
        (df["mortes"] * 5 + df["feridos"] * 1.5)
        / df["acidentes"].clip(lower=1)
    )

    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)

    return df


def multiselect(label, options, default=None):
    options = sorted(options)
    return st.sidebar.multiselect(label, options, default=default or options)


df = carregar_dados()

st.markdown("""
<div class="hero">
    <div class="tag">🚦 Dashboard Analítico • Projeto G2</div>
    <h1>Análise de Acidentes de Trânsito no Brasil</h1>
    <p>
        Painel interativo com dados simulados entre 2015 e 2024, explorando padrões
        de acidentes por região, estado, cidade, clima, gravidade e período do dia.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("Painel de Filtros")
st.sidebar.caption("Ajuste os filtros para explorar diferentes recortes da base.")

anos = st.sidebar.slider(
    "Ano",
    int(df["ano"].min()),
    int(df["ano"].max()),
    (int(df["ano"].min()), int(df["ano"].max()))
)

meses = multiselect("Mês", df["mes"].unique())
regioes = multiselect("Região", df["regiao"].unique())

ufs_disponiveis = df[df["regiao"].isin(regioes)]["uf"].unique()
ufs = multiselect("Estado", ufs_disponiveis)

cidades_disponiveis = df[df["uf"].isin(ufs)]["cidade"].unique()
cidades = multiselect("Cidade", cidades_disponiveis)

tipos = multiselect("Tipo de acidente", df["tipo_acidente"].unique())
gravidades = multiselect("Nível de gravidade", df["nivel_gravidade"].unique())

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
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

total_acidentes = int(f["acidentes"].sum())
total_mortes = int(f["mortes"].sum())

estado_critico = f.groupby("uf")["acidentes"].sum().idxmax()
tipo_predominante = f.groupby("tipo_acidente")["acidentes"].sum().idxmax()
horario_perigoso = f.groupby("periodo_dia")["mortes"].sum().idxmax()
taxa_gravidade = f["taxa_gravidade"].mean()

cols = st.columns(6)

cols[0].metric("Total de acidentes", f"{total_acidentes:,}".replace(",", "."))
cols[1].metric("Total de mortes", f"{total_mortes:,}".replace(",", "."))
cols[2].metric("Estado crítico", estado_critico)
cols[3].metric("Tipo predominante", tipo_predominante)
cols[4].metric("Horário crítico", horario_perigoso)
cols[5].metric("Taxa gravidade", f"{taxa_gravidade:.2f}")

st.markdown('<div class="block-title">Evolução temporal dos acidentes</div>', unsafe_allow_html=True)

temporal = (
    f.groupby("ano_mes", as_index=False)[["acidentes", "mortes", "feridos"]]
    .sum()
)

fig_temporal = px.area(
    temporal,
    x="ano_mes",
    y="acidentes",
    markers=True,
    labels={
        "ano_mes": "Período",
        "acidentes": "Acidentes"
    },
    color_discrete_sequence=["#c1121f"]
)

fig_temporal.update_layout(
    template="plotly_white",
    height=420,
    margin=dict(l=20, r=20, t=30, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_temporal, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="block-title">Acidentes por estado</div>', unsafe_allow_html=True)

    estado = (
        f.groupby("uf", as_index=False)["acidentes"]
        .sum()
        .sort_values("acidentes", ascending=False)
    )

    fig_estado = px.bar(
        estado,
        x="uf",
        y="acidentes",
        color="acidentes",
        color_continuous_scale="Reds",
        labels={
            "uf": "Estado",
            "acidentes": "Acidentes"
        }
    )

    fig_estado.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_estado, use_container_width=True)

with c2:
    st.markdown('<div class="block-title">Ranking por tipo de acidente</div>', unsafe_allow_html=True)

    tipo = (
        f.groupby("tipo_acidente", as_index=False)["acidentes"]
        .sum()
        .sort_values("acidentes", ascending=True)
    )

    fig_tipo = px.bar(
        tipo,
        x="acidentes",
        y="tipo_acidente",
        orientation="h",
        color="acidentes",
        color_continuous_scale="OrRd",
        labels={
            "tipo_acidente": "Tipo de acidente",
            "acidentes": "Acidentes"
        }
    )

    fig_tipo.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_tipo, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="block-title">Horário x gravidade</div>', unsafe_allow_html=True)

    ordem = ["Madrugada", "Manhã", "Tarde", "Noite"]

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

    fig_heat = px.imshow(
        heat,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="OrRd",
        labels=dict(x="Gravidade", y="Período do dia", color="Acidentes")
    )

    fig_heat.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_heat, use_container_width=True)

with c4:
    st.markdown('<div class="block-title">Chuva, visibilidade e acidentes</div>', unsafe_allow_html=True)

    fig_scatter = px.scatter(
        f,
        x="chuva_mm",
        y="acidentes",
        color="visibilidade",
        size="mortes",
        hover_data=["uf", "cidade", "tipo_acidente"],
        labels={
            "chuva_mm": "Chuva (mm)",
            "acidentes": "Acidentes",
            "visibilidade": "Visibilidade"
        }
    )

    fig_scatter.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown('<div class="block-title">Tabela dinâmica por localidade</div>', unsafe_allow_html=True)

tabela = f.pivot_table(
    index=["regiao", "uf", "cidade"],
    columns="nivel_gravidade",
    values="acidentes",
    aggfunc="sum",
    fill_value=0
)

tabela["Total"] = tabela.sum(axis=1)

st.dataframe(
    tabela.sort_values("Total", ascending=False),
    use_container_width=True
)

regiao_critica = f.groupby("regiao")["acidentes"].sum().idxmax()
vis_critica = f.groupby("visibilidade")["acidentes"].sum().idxmax()

st.markdown('<div class="block-title">Interpretação dos resultados</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="insight-box">
        No recorte selecionado, a região com maior concentração de acidentes é
        <strong>{regiao_critica}</strong>, com destaque para o estado
        <strong>{estado_critico}</strong>. O tipo mais frequente é
        <strong>{tipo_predominante}</strong>, enquanto o período com maior impacto
        em mortes é <strong>{horario_perigoso}</strong>. A condição de visibilidade
        mais recorrente nos registros filtrados é <strong>{vis_critica}</strong>,
        indicando que fatores ambientais também devem ser observados em políticas
        de prevenção.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="block-title">Conclusão executiva</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="insight-box">
        A análise indica que a prevenção deve combinar fiscalização em horários
        críticos, ações educativas voltadas aos tipos de acidente mais frequentes
        e monitoramento climático. Estados e cidades com maior volume devem ser
        priorizados em campanhas, melhorias de sinalização e planejamento viário.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer-box">
        Desenvolvido por <strong>Rodrigo Soares Veiga</strong><br>
        Disciplina: <strong>Linguagens de Programação</strong><br>
        Tema: <strong>Análise de Acidentes de Trânsito no Brasil</strong>
    </div>
    """,
    unsafe_allow_html=True
)
