"""
Módulo para criação de visualizações com Plotly
Específico para dados de renda municipal
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class RendaCharts:
    """
    Classe para construção de gráficos de renda
    """
    
    @staticmethod
    def criar_grafico_barras_ranking(df, titulo="Ranking de Renda por Município"):
        """
        Gráfico de barras para ranking de renda
        """
        if df is None or df.empty:
            return go.Figure()
        
        # Cores baseadas na classificação
        cor_map = {
            'Alta renda': '#2ecc71',
            'Classe média alta': '#3498db',
            'Classe média': '#f39c12',
            'Classe média baixa': '#e67e22',
            'Baixa renda': '#e74c3c'
        }
        
        cores = [cor_map.get(c, '#95a5a6') for c in df['classificacao'].values]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['renda_familiar_estimada'],
            y=df['municipio'],
            orientation='h',
            marker_color=cores,
            text=df['renda_familiar_estimada'].apply(lambda x: f'R$ {x:,.0f}'),
            textposition='outside',
            name='Renda Familiar Estimada'
        ))
        
        fig.update_layout(
            title=dict(text=titulo, x=0.5),
            xaxis_title="Renda Familiar Estimada (R$)",
            yaxis_title="Município",
            height=max(400, len(df) * 35),
            margin=dict(l=150, r=50, t=80, b=50),
            font=dict(size=11)
        )
        
        return fig
    
    @staticmethod
    def criar_indicador_municipio(estatisticas):
        """
        Cria cards de indicadores para um município
        """
        if estatisticas is None:
            return go.Figure()
        
        renda = estatisticas.get('renda_familiar_estimada', 0)
        
        # Define cor baseada na classificação
        classificacao = estatisticas.get('classificacao', '')
        cor_map = {
            'Alta renda': '#2ecc71',
            'Classe média alta': '#3498db', 
            'Classe média': '#f39c12',
            'Classe média baixa': '#e67e22',
            'Baixa renda': '#e74c3c'
        }
        cor = cor_map.get(classificacao, '#95a5a6')
        
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="number+gauge+delta",
            value=renda,
            title={"text": f"<span style='font-size:16px'>{estatisticas.get('municipio', '')}</span><br><span style='font-size:12px'>{classificacao}</span>"},
            delta={'reference': 13300, 'relative': True, 'valueformat': '.1%'},
            gauge={
                'axis': {'range': [0, 50000], 'tickformat': 'R$,.0f'},
                'bar': {'color': cor},
                'steps': [
                    {'range': [0, 6000], 'color': '#ffcccc'},
                    {'range': [6000, 13300], 'color': '#ffffcc'},
                    {'range': [13300, 25000], 'color': '#ccffcc'},
                    {'range': [25000, 50000], 'color': '#ccffff'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': renda
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        return fig
    
    @staticmethod
    def criar_mapa_distribuicao(df, municipio_selecionado=None):
        """
        Cria mapa de distribuição de renda (versão simplificada - scatter plot geo)
        Como não temos coordenadas reais, usamos scatter plot com ranking
        """
        if df is None or df.empty:
            return go.Figure()
        
        # Cria scatter plot com ranking
        df_plot = df.copy()
        df_plot['ranking'] = df_plot['renda_familiar_estimada'].rank(ascending=False)
        df_plot['cor'] = df_plot['classificacao'].map({
            'Alta renda': 4,
            'Classe média alta': 3,
            'Classe média': 2,
            'Classe média baixa': 1,
            'Baixa renda': 0
        })
        
        fig = px.scatter(
            df_plot.head(100),
            x='ranking',
            y='renda_familiar_estimada',
            size='populacao',
            color='classificacao',
            hover_name='municipio',
            text='municipio',
            title="Distribuição de Renda vs Ranking Estadual",
            labels={'ranking': 'Ranking Estadual (1 = maior renda)', 
                    'renda_familiar_estimada': 'Renda Familiar Estimada (R$)'}
        )
        
        # Destaca município selecionado se existir
        if municipio_selecionado:
            municipio_data = df[df['municipio'] == municipio_selecionado]
            if not municipio_data.empty:
                fig.add_trace(go.Scatter(
                    x=[municipio_data['renda_familiar_estimada'].rank(ascending=False).values[0]],
                    y=[municipio_data['renda_familiar_estimada'].values[0]],
                    mode='markers',
                    marker=dict(color='red', size=15, symbol='star'),
                    name=municipio_selecionado,
                    text=[municipio_selecionado]
                ))
        
        fig.update_layout(
            title_x=0.5,
            height=500,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def criar_grafico_mensal(df_mensal):
        """
        Cria gráfico de linha para análise mensal (mês e valor)
        """
        if df_mensal is None or df_mensal.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_mensal['mes'],
            y=df_mensal['renda_estimada'],
            mode='lines+markers',
            name=df_mensal['municipio'].iloc[0],
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10, color='#ff7f0e', symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        # Linha de referência para classe média
        fig.add_hline(y=13300, line_dash="dash", line_color="green", 
                      annotation_text="Limite Classe Média Alta")
        fig.add_hline(y=6000, line_dash="dash", line_color="orange",
                      annotation_text="Limite Classe Média")
        
        fig.update_layout(
            title=dict(text=f"📈 Tendência Mensal de Renda - {df_mensal['municipio'].iloc[0]}", x=0.5),
            xaxis_title="Mês",
            yaxis_title="Renda Familiar Estimada (R$)",
            hovermode='x unified',
            height=450,
            font=dict(size=12)
        )
        
        # Formata o eixo Y como moeda
        fig.update_yaxis(tickprefix="R$ ", tickformat=",.0f")
        
        return fig
    
    @staticmethod
    def criar_tabela_ranking(df, titulo="Ranking de Renda por Município"):
        """
        Cria tabela interativa com ranking de renda
        """
        if df is None or df.empty:
            return go.Figure()
        
        # Prepara dados para tabela
        tabela_data = df[['municipio', 'renda_familiar_estimada', 'classificacao', 'populacao']].head(50).copy()
        tabela_data['renda_familiar_estimada'] = tabela_data['renda_familiar_estimada'].apply(lambda x: f'R$ {x:,.0f}')
        tabela_data['populacao'] = tabela_data['populacao'].apply(lambda x: f'{x:,.0f}' if pd.notna(x) else 'N/A')
        tabela_data = tabela_data.rename(columns={
            'municipio': 'Município',
            'renda_familiar_estimada': 'Renda Familiar (R$)',
            'classificacao': 'Classificação',
            'populacao': 'População'
        })
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(tabela_data.columns),
                fill_color='#1f77b4',
                align='left',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[tabela_data[col] for col in tabela_data.columns],
                fill_color='#f0f2f6',
                align='left',
                font=dict(size=11),
                height=30
            )
        )])
        
        fig.update_layout(
            title=titulo,
            height=600,
            margin=dict(t=50, l=0, r=0, b=0)
        )
        
        return fig
    
    @staticmethod
    def criar_comparativo_municipios(df_comparativo):
        """
        Cria gráfico comparativo entre municípios selecionados
        """
        if df_comparativo is None or df_comparativo.empty:
            return go.Figure()
        
        cores = px.colors.qualitative.Set3
        
        fig = go.Figure()
        
        for i, (_, row) in enumerate(df_comparativo.iterrows()):
            fig.add_trace(go.Bar(
                x=[row['municipio']],
                y=[row['renda_familiar_estimada']],
                name=row['municipio'],
                marker_color=cores[i % len(cores)],
                text=f"R$ {row['renda_familiar_estimada']:,.0f}",
                textposition='outside'
            ))
        
        fig.update_layout(
            title="Comparação de Renda entre Municípios",
            xaxis_title="Município",
            yaxis_title="Renda Familiar Estimada (R$)",
            showlegend=False,
            height=450,
            font=dict(size=12)
        )
        
        fig.update_yaxis(tickprefix="R$ ", tickformat=",.0f")
        
        return fig
