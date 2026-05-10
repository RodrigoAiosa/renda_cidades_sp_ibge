"""
Módulo para processamento específico de dados de renda
"""

import pandas as pd
import numpy as np

class RendaProcessor:
    """
    Classe para processar e analisar dados de renda municipal
    """
    
    # Faixas de renda familiar (conforme solicitado)
    FAIXAS_RENDA = {
        "Classe média": (6000, 13300),
        "Classe média alta": (13300, 25000),
        "Alta renda": (25000, float('inf'))
    }
    
    @staticmethod
    def calcular_estatisticas_municipio(df, municipio):
        """
        Calcula estatísticas detalhadas para um município específico
        """
        if df is None or df.empty:
            return None
        
        municipio_data = df[df['municipio'] == municipio]
        
        if municipio_data.empty:
            return None
        
        row = municipio_data.iloc[0]
        
        estatisticas = {
            'municipio': row['municipio'],
            'renda_familiar_estimada': row['renda_familiar_estimada'],
            'pib_per_capita': row.get('pib_per_capita', None),
            'renda_per_capita': row.get('renda_per_capita', None),
            'populacao': row.get('populacao', None),
            'classificacao': row['classificacao'],
            'ranking_estadual': df['renda_familiar_estimada'].rank(ascending=False)[municipio_data.index[0]]
        }
        
        return estatisticas
    
    @staticmethod
    def gerar_ranking_municipios(df, n=10):
        """
        Gera ranking dos municípios por renda familiar
        """
        if df is None or df.empty:
            return None, None
        
        # Top maiores rendas
        maiores_rendas = df.nlargest(n, 'renda_familiar_estimada')[
            ['municipio', 'renda_familiar_estimada', 'classificacao', 'populacao']
        ].copy()
        
        # Top menores rendas
        menores_rendas = df.nsmallest(n, 'renda_familiar_estimada')[
            ['municipio', 'renda_familiar_estimada', 'classificacao', 'populacao']
        ].copy()
        
        return maiores_rendas, menores_rendas
    
    @staticmethod
    def estatisticas_por_classificacao(df):
        """
        Agrupa estatísticas por faixa de classificação
        """
        if df is None or df.empty:
            return None
        
        # Mapeia classificações para o formato desejado
        def mapear_classificacao(classif):
            if classif in ["Classe média", "Classe média baixa"]:
                return "Classe média"
            elif classif in ["Classe média alta"]:
                return "Classe média alta"
            elif classif in ["Alta renda"]:
                return "Alta renda"
            else:
                return "Outras faixas"
        
        df['classificacao_agrupada'] = df['classificacao'].apply(mapear_classificacao)
        
        estatisticas = df.groupby('classificacao_agrupada').agg({
            'municipio': 'count',
            'renda_familiar_estimada': ['mean', 'median', 'min', 'max'],
            'populacao': 'sum'
        }).round(0)
        
        estatisticas.columns = ['quantidade_municipios', 'renda_media', 'renda_mediana', 'renda_min', 'renda_max', 'populacao_total']
        
        return estatisticas.reset_index()
    
    @staticmethod
    def comparar_municipios(df, municipios):
        """
        Compara múltiplos municípios lado a lado
        """
        if df is None or df.empty or not municipios:
            return None
        
        comparacao = df[df['municipio'].isin(municipios)][
            ['municipio', 'renda_familiar_estimada', 'classificacao', 'populacao']
        ].copy()
        
        # Adiciona ranking
        comparacao['ranking'] = comparacao['renda_familiar_estimada'].rank(ascending=False).astype(int)
        
        return comparacao.sort_values('renda_familiar_estimada', ascending=False)
    
    @staticmethod
    def criar_dados_mensais_para_demo(df, municipio):
        """
        Cria dados mensais simulados para visualização de tendência
        Baseada na renda real do município com variações sazonais
        """
        if df is None or municipio is None:
            return None
        
        renda_base = municipio.get('renda_familiar_estimada', 10000)
        
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        # Variações sazonais realistas
        variacoes = [0.98, 0.97, 0.99, 1.01, 1.02, 1.00, 
                     0.99, 1.01, 1.03, 1.04, 1.05, 1.06]
        
        valores_mensais = [renda_base * var for var in variacoes]
        
        df_mensal = pd.DataFrame({
            'mes': meses,
            'renda_estimada': valores_mensais,
            'municipio': municipio.get('municipio', '')
        })
        
        return df_mensal
