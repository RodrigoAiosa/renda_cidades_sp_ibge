"""
Dashboard de Renda por Município - Estado de São Paulo
Aplicação Streamlit com menu lateral e filtro por cidade
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Importa módulos personalizados
from src.data_loader import RendaDataLoader
from src.data_processor import RendaProcessor
from src.charts import RendaCharts

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Renda por Município - SP",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1f77b4 0%, #2ecc71 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: white;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .info-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown("""
<div class="main-header">
    <h1>💰 Renda por Município - São Paulo</h1>
    <p>Dados oficiais do IBGE | PIB per capita e estimativas de renda familiar</p>
</div>
""", unsafe_allow_html=True)

# ==================== MENU LATERAL ====================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/examples/iris/iris.png", 
             width=80)
    st.title("🔍 Filtros")
    
    st.markdown("---")
    
    # Carregamento dos dados com cache
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def carregar_dados():
        loader = RendaDataLoader()
        df = loader.consolidar_dados_renda()
        municipios = loader.listar_municipios(df)
        return df, municipios
    
    with st.spinner("🔄 Carregando dados do IBGE..."):
        df_principal, lista_municipios = carregar_dados()
    
    st.markdown("### 📍 Seleção de Município")
    
    # Filtro de município - principal funcionalidade
    municipio_selecionado = st.selectbox(
        "Escolha uma cidade:",
        options=lista_municipios if lista_municipios else ["Carregando..."],
        index=0,
        help="Selecione um município paulista para visualizar os dados de renda"
    )
    
    st.markdown("---")
    
    # Filtros adicionais
    st.markdown("### ⚙️ Configurações")
    
    mostrar_ranking = st.checkbox("Mostrar ranking completo", value=False)
    mostrar_comparacao = st.checkbox("Comparar múltiplas cidades", value=False)
    
    if mostrar_comparacao:
        cidades_para_comparar = st.multiselect(
            "Selecione cidades para comparar:",
            options=lista_municipios if lista_municipios else [],
            default=[municipio_selecionado] if municipio_selecionado else []
        )
    
    st.markdown("---")
    st.markdown("### 📊 Sobre os dados")
    st.info(
        "**Fontes oficiais:**\n"
        "- PIB per capita: IBGE SIDRA (Tabela 5938)\n"
        "- Renda domiciliar per capita: Censo 2022\n"
        "- População: IBGE Censo 2022\n\n"
        "*Renda familiar estimada = Renda per capita × 3 pessoas*"
    )

# ==================== PROCESSAMENTO DOS DADOS ====================

if df_principal is not None and not df_principal.empty:
    
    # Obtém estatísticas do município selecionado
    processor = RendaProcessor()
    estatisticas_municipio = processor.calcular_estatisticas_municipio(df_principal, municipio_selecionado)
    
    # ==================== DASHBOARD PRINCIPAL ====================
    
    # Indicador principal do município selecionado
    st.subheader(f"🏙️ Análise de Renda - {municipio_selecionado}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if estatisticas_municipio:
            st.metric(
                "💰 Renda Familiar Estimada",
                f"R$ {estatisticas_municipio.get('renda_familiar_estimada', 0):,.0f}".replace(",", "."),
                delta=None
            )
    
    with col2:
        if estatisticas_municipio:
            classificacao = estatisticas_municipio.get('classificacao', 'N/A')
            emoji_map = {
                "Alta renda": "🟢",
                "Classe média alta": "🔵",
                "Classe média": "🟡",
                "Classe média baixa": "🟠",
                "Baixa renda": "🔴"
            }
            st.metric(
                "📊 Classificação",
                f"{emoji_map.get(classificacao, '')} {classificacao}",
                delta=None
            )
    
    with col3:
        if estatisticas_municipio and estatisticas_municipio.get('populacao'):
            st.metric(
                "👥 População",
                f"{estatisticas_municipio.get('populacao', 0):,.0f}".replace(",", "."),
                delta=None
            )
    
    with col4:
        if estatisticas_municipio:
            ranking = int(estatisticas_municipio.get('ranking_estadual', 0))
            total = len(df_principal)
            st.metric(
                "🏆 Ranking Estadual",
                f"{ranking}º
