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
                f"{ranking}º de {total} municípios",
                delta=None
            )
    
    st.markdown("---")
    
    # ==================== GRÁFICOS E ANÁLISES ====================
    
    # Gráfico de gauge / indicador visual
    st.subheader("📈 Indicador de Renda")
    fig_gauge = RendaCharts.criar_indicador_municipio(estatisticas_municipio)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Gráfico mensal (mês e valor)
    st.subheader("📅 Tendência Mensal (Estimativa)")
    df_mensal = processor.criar_dados_mensais_para_demo(df_principal, estatisticas_municipio)
    fig_mensal = RendaCharts.criar_grafico_mensal(df_mensal)
    st.plotly_chart(fig_mensal, use_container_width=True)
    
    # Explicação das faixas de renda
    with st.expander("📖 Entenda as faixas de renda"):
        st.markdown("""
        | Classificação | Renda Familiar Mensal | Descrição |
        |--------------|----------------------|-----------|
        | 🟢 **Alta renda** | Acima de R$ 25.000 | Famílias com alto poder aquisitivo |
        | 🔵 **Classe média alta** | R$ 13.300 a R$ 25.000 | Padrão de vida elevado, acesso a bens e serviços premium |
        | 🟡 **Classe média** | R$ 6.000 a R$ 13.300 | Padrão de vida confortável, acesso a educação e lazer |
        | 🟠 **Classe média baixa** | R$ 3.000 a R$ 6.000 | Consumo moderado, alguma capacidade de poupança |
        | 🔴 **Baixa renda** | Abaixo de R$ 3.000 | Necessidades básicas, baixa capacidade de poupança |
        """)
    
    # ==================== RANKING E COMPARAÇÕES ====================
    
    if mostrar_ranking:
        st.subheader("🏆 Ranking de Renda por Município")
        
        maiores, menores = processor.gerar_ranking_municipios(df_principal, n=20)
        
        col_rank1, col_rank2 = st.columns(2)
        
        with col_rank1:
            st.markdown("### 📈 Maiores Rendas")
            fig_maiores = RendaCharts.criar_grafico_barras_ranking(
                maiores, 
                "Top 20 Maiores Rendas por Município"
            )
            st.plotly_chart(fig_maiores, use_container_width=True)
        
        with col_rank2:
            st.markdown("### 📉 Menores Rendas")
            fig_menores = RendaCharts.criar_grafico_barras_ranking(
                menores,
                "Bottom 20 Menores Rendas por Município"
            )
            st.plotly_chart(fig_menores, use_container_width=True)
        
        # Tabela completa
        st.subheader("📋 Tabela Completa de Renda")
        fig_tabela = RendaCharts.criar_tabela_ranking(df_principal, "Ranking de Renda - Todos os Municípios Paulistas")
        st.plotly_chart(fig_tabela, use_container_width=True)
    
    if mostrar_comparacao and len(cidades_para_comparar) > 1:
        st.subheader("🔄 Comparação entre Municípios")
        
        df_comparacao = processor.comparar_municipios(df_principal, cidades_para_comparar)
        fig_comparativo = RendaCharts.criar_comparativo_municipios(df_comparacao)
        st.plotly_chart(fig_comparativo, use_container_width=True)
        
        # Tabela comparativa
        st.dataframe(
            df_comparacao.style.format({
                'renda_familiar_estimada': lambda x: f'R$ {x:,.0f}',
                'populacao': lambda x: f'{x:,.0f}' if pd.notna(x) else 'N/A'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    # ==================== DISTRIBUIÇÃO GERAL ====================
    st.subheader("📊 Distribuição de Renda no Estado de São Paulo")
    
    col_dist1, col_dist2 = st.columns(2)
    
    with col_dist1:
        # Gráfico de distribuição geral
        estatisticas_classificacao = processor.estatisticas_por_classificacao(df_principal)
        if estatisticas_classificacao is not None:
            fig_pizza = px.pie(
                estatisticas_classificacao,
                values='quantidade_municipios',
                names='classificacao_agrupada',
                title="Distribuição dos Municípios por Faixa de Renda",
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.3
            )
            fig_pizza.update_layout(title_x=0.5)
            st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col_dist2:
        # Gráfico de dispersão
        fig_scatter = RendaCharts.criar_mapa_distribuicao(df_principal, municipio_selecionado)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Estatísticas gerais do estado
    st.subheader("📊 Estatísticas Gerais do Estado de São Paulo")
    
    col_est1, col_est2, col_est3 = st.columns(3)
    
    with col_est1:
        st.metric(
            "Renda Média Estadual",
            f"R$ {df_principal['renda_familiar_estimada'].mean():,.0f}".replace(",", "."),
            delta=None
        )
    
    with col_est2:
        st.metric(
            "Renda Mediana Estadual",
            f"R$ {df_principal['renda_familiar_estimada'].median():,.0f}".replace(",", "."),
            delta=None
        )
    
    with col_est3:
        st.metric(
            "Município com Maior Renda",
            df_principal.loc[df_principal['renda_familiar_estimada'].idxmax(), 'municipio'],
            delta=None
        )
    
    # ==================== DOWNLOAD DOS DADOS ====================
    st.subheader("📥 Exportar Dados")
    
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        # Dados completos em CSV
        csv_data = df_principal.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Baixar dados completos (CSV)",
            data=csv_data,
            file_name=f"renda_municipios_sp_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_download2:
        # Dados do município selecionado
        if estatisticas_municipio:
            df_municipio = pd.DataFrame([estatisticas_municipio])
            csv_municipio = df_municipio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"🏙️ Baixar dados de {municipio_selecionado} (CSV)",
                data=csv_municipio,
                file_name=f"renda_{municipio_selecionado.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )

else:
    st.error("❌ Não foi possível carregar os dados. Verifique sua conexão com a internet e tente novamente.")
    st.info("💡 Dica: O IBGE SIDRA pode estar temporariamente indisponível. Tente novamente em alguns minutos.")

# ==================== RODAPÉ ====================
st.markdown("""
<div class="footer">
    <p>📊 Dashboard desenvolvido com Streamlit | Dados: IBGE SIDRA (Censo 2022 e PIB per capita)</p>
    <p>🔍 Fonte oficial: Instituto Brasileiro de Geografia e Estatística | Última atualização: {}</p>
    <p>💡 Renda familiar estimada = Renda per capita × 3 pessoas (média nacional de moradores por domicílio)</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)
