"""
Módulo para carregamento de dados de renda dos municípios paulistas
Fontes: IBGE SIDRA (PIB per capita) e estimativas de renda
"""

import sidrapy
import pandas as pd
import requests
from io import StringIO
from functools import lru_cache
import warnings
warnings.filterwarnings('ignore')

class RendaDataLoader:
    """
    Classe responsável por carregar dados de renda dos municípios
    """
    
    # Código do Estado de São Paulo
    SP_CODIGO = 35
    
    def __init__(self):
        self.cache = {}
        
    @lru_cache(maxsize=128)
    def carregar_pib_per_capita_municipal(self):
        """
        Carrega PIB per capita dos municípios (Tabela 5938 do SIDRA)
        Esta é a melhor proxy oficial para renda por município
        """
        try:
            print("📊 Carregando PIB per capita dos municípios paulistas...")
            
            # Tabela 5938: Produto Interno Bruto per capita
            df = sidrapy.get_table(
                table_code='5938',
                territorial_level='6',  # Nível municipal
                ibge_territorial_code='all',
                period='last',  # Último ano disponível
                variable='all'
            )
            
            # Limpa e renomeia colunas
            df = df.iloc[1:].reset_index(drop=True)
            df = df.rename(columns={
                'D1C': 'codigo_uf',
                'D1N': 'estado',
                'D2C': 'codigo_municipio',
                'D2N': 'municipio',
                'D3C': 'ano_codigo',
                'D3N': 'ano',
                'V': 'pib_per_capita'
            })
            
            # Converte para numérico
            df['pib_per_capita'] = pd.to_numeric(df['pib_per_capita'], errors='coerce')
            df['codigo_uf'] = pd.to_numeric(df['codigo_uf'], errors='coerce')
            
            # Filtra apenas São Paulo
            df_sp = df[df['codigo_uf'] == self.SP_CODIGO].copy()
            
            # Remove valores nulos
            df_sp = df_sp.dropna(subset=['pib_per_capita', 'municipio'])
            
            return df_sp
            
        except Exception as e:
            print(f"❌ Erro ao carregar PIB per capita: {e}")
            return None
    
    @lru_cache(maxsize=128)
    def carregar_renda_domiciliar_per_capita(self):
        """
        Carrega renda domiciliar per capita (Censo 2022 - Tabela 9734)
        Dados mais precisos, porém menos atualizados
        """
        try:
            print("📊 Carregando renda domiciliar per capita do Censo...")
            
            # Tabela 9734: Renda domiciliar per capita
            df = sidrapy.get_table(
                table_code='9734',
                territorial_level='6',
                ibge_territorial_code='all',
                period='2022',
                variable='all'
            )
            
            df = df.iloc[1:].reset_index(drop=True)
            df = df.rename(columns={
                'D1C': 'codigo_uf',
                'D1N': 'estado', 
                'D2C': 'codigo_municipio',
                'D2N': 'municipio',
                'V': 'renda_per_capita'
            })
            
            df['renda_per_capita'] = pd.to_numeric(df['renda_per_capita'], errors='coerce')
            df['codigo_uf'] = pd.to_numeric(df['codigo_uf'], errors='coerce')
            
            # Filtra São Paulo
            df_sp = df[df['codigo_uf'] == self.SP_CODIGO].copy()
            df_sp = df_sp.dropna(subset=['renda_per_capita', 'municipio'])
            
            return df_sp
            
        except Exception as e:
            print(f"❌ Erro ao carregar renda domiciliar: {e}")
            return None
    
    def carregar_populacao_municipios(self):
        """
        Carrega população dos municípios para contexto
        """
        try:
            df = sidrapy.get_table(
                table_code='9514',
                territorial_level='6',
                ibge_territorial_code='all',
                period='2022',
                variable='all'
            )
            
            df = df.iloc[1:].reset_index(drop=True)
            df = df.rename(columns={
                'D1C': 'codigo_uf',
                'D1N': 'estado',
                'D2C': 'codigo_municipio',
                'D2N': 'municipio',
                'V': 'populacao'
            })
            
            df['populacao'] = pd.to_numeric(df['populacao'], errors='coerce')
            df['codigo_uf'] = pd.to_numeric(df['codigo_uf'], errors='coerce')
            
            # Filtra São Paulo e tipo "Total"
            df_sp = df[df['codigo_uf'] == self.SP_CODIGO].copy()
            df_sp = df_sp.groupby(['codigo_municipio', 'municipio'])['populacao'].sum().reset_index()
            
            return df_sp
            
        except Exception as e:
            print(f"❌ Erro ao carregar população: {e}")
            return None
    
    def consolidar_dados_renda(self):
        """
        Consolida dados de PIB per capita, renda domiciliar e população
        Retorna um DataFrame unificado com todos os municípios paulistas
        """
        # Carrega dados
        df_pib = self.carregar_pib_per_capita_municipal()
        df_renda = self.carregar_renda_domiciliar_per_capita()
        df_pop = self.carregar_populacao_municipios()
        
        if df_pib is None:
            return None
        
        # Inicia com dados de PIB per capita
        df_consolidado = df_pib[['codigo_municipio', 'municipio', 'pib_per_capita', 'ano']].copy()
        
        # Adiciona renda domiciliar se disponível
        if df_renda is not None:
            df_consolidado = df_consolidado.merge(
                df_renda[['codigo_municipio', 'renda_per_capita']],
                on='codigo_municipio',
                how='left'
            )
        
        # Adiciona população
        if df_pop is not None:
            df_consolidado = df_consolidado.merge(
                df_pop[['codigo_municipio', 'populacao']],
                on='codigo_municipio',
                how='left'
            )
        
        # Calcula renda familiar estimada (baseado em média de 3 pessoas por domicílio)
        # Usa a melhor fonte disponível para renda per capita
        if 'renda_per_capita' in df_consolidado.columns:
            df_consolidado['renda_familiar_estimada'] = df_consolidado['renda_per_capita'] * 3
        else:
            # Utiliza PIB per capita como proxy, com fator de ajuste econômico
            df_consolidado['renda_familiar_estimada'] = df_consolidado['pib_per_capita'] * 0.7 * 3
        
        # Adiciona classificação baseada na renda familiar
        def classificar_renda(renda_familiar):
            if pd.isna(renda_familiar):
                return "Dados indisponíveis"
            elif renda_familiar < 3000:
                return "Baixa renda"
            elif renda_familiar < 6000:
                return "Classe média baixa"
            elif renda_familiar < 13300:
                return "Classe média"
            elif renda_familiar < 25000:
                return "Classe média alta"
            else:
                return "Alta renda"
        
        df_consolidado['classificacao'] = df_consolidado['renda_familiar_estimada'].apply(classificar_renda)
        
        # Ordena por renda
        df_consolidado = df_consolidado.sort_values('renda_familiar_estimada', ascending=False)
        
        return df_consolidado
    
    def listar_municipios(self, df_consolidado):
        """
        Retorna lista ordenada de todos os municípios paulistas
        """
        if df_consolidado is None or df_consolidado.empty:
            return []
        
        municipios = sorted(df_consolidado['municipio'].unique())
        return municipios
    
    def filtrar_por_municipio(self, df_consolidado, municipio):
        """
        Filtra dados para um município específico
        """
        if df_consolidado is None or df_consolidado.empty:
            return None
        
        return df_consolidado[df_consolidado['municipio'] == municipio].iloc[0] if not df_consolidado[df_consolidado['municipio'] == municipio].empty else None
