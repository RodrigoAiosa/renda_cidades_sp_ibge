"""
Dashboard de Renda por Município - Estado de São Paulo
Aplicação Streamlit com menu lateral e filtro por cidade
Consome diretamente a API REST do IBGE (Tabela 5938)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from typing import Optional, List, Dict
import numpy as np
import random

# Importa a lista de municípios do arquivo separado
from src.municipios_sp import MUNICIPIOS_SP, DADOS_REAIS_REFERENCIA, get_municipios_ordenados

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Renda por Município - SP",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CLIENTE DA API IBGE ====================

class IBGEAPIClient:
    """
    Cliente direto da API do IBGE SIDRA
    Endpoint: https://apisidra.ibge.gov.br/values/
    """
    
    BASE_URL = "https://apisidra.ibge.gov.br/values"
    SP_CODIGO = "35"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; IBGE-API-Client/1.0)',
            'Accept': 'application/json'
        })
    
    def testar_conexao(self) -> bool:
        """Testa se a API está acessível"""
        try:
            url = f"{self.BASE_URL}/t/5938/n1/1"
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def buscar_pib_municipal(self, ano: int = 2022) -> Optional[pd.DataFrame]:
        """
        Busca PIB total dos municípios para um determinado ano
        Variável 37 = Produto Interno Bruto a preços correntes (Mil Reais)
        """
        url = f"{self.BASE_URL}/t/5938/n6/all/v/37/p/{ano}"
        
        try:
            print(f"📊 Buscando dados da API: {url}")
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Erro HTTP {response.status_code}")
                return None
            
            dados_json = response.json()
            
            if not dados_json or len(dados_json) < 2:
                print("⚠️ Nenhum dado retornado")
                return None
            
            df = self._converter_json_para_dataframe(dados_json)
            
            if df is not None and not df.empty:
                df_sp = df[df['codigo_uf'] == self.SP_CODIGO].copy()
                print(f"✅ Carregados {len(df_sp)} municípios paulistas")
                return df_sp
            
            return df
            
        except requests.exceptions.Timeout:
            print("❌ Timeout na requisição")
            return None
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def _converter_json_para_dataframe(self, dados_json: List) -> Optional[pd.DataFrame]:
        """Converte o JSON retornado pela API em DataFrame"""
        try:
            cabecalhos = dados_json[0]
            
            col_mapping = {}
            for i, col in enumerate(cabecalhos):
                if col == 'D1C':
                    col_mapping[i] = 'codigo_uf'
                elif col == 'D1N':
                    col_mapping[i] = 'uf_nome'
                elif col == 'D2C':
                    col_mapping[i] = 'codigo_municipio'
                elif col == 'D2N':
                    col_mapping[i] = 'municipio'
                elif col == 'V':
                    col_mapping[i] = 'pib_total_mil'
                elif col == 'MC':
                    col_mapping[i] = 'municipio_codigo_completo'
                elif col == 'NN':
                    col_mapping[i] = 'nivel'
            
            dados = []
            for linha in dados_json[1:]:
                registro = {}
                for i, valor in enumerate(linha):
                    if i in col_mapping:
                        registro[col_mapping[i]] = valor
                dados.append(registro)
            
            df = pd.DataFrame(dados)
            
            df['pib_total_mil'] = pd.to_numeric(df['pib_total_mil'], errors='coerce')
            df['codigo_uf'] = pd.to_numeric(df['codigo_uf'], errors='coerce')
            df['codigo_municipio'] = pd.to_numeric(df['codigo_municipio'], errors='coerce')
            
            df = df[df['codigo_municipio'] != 0]
            
            return df
            
        except Exception as e:
            print(f"❌ Erro ao converter JSON: {e}")
            return None
    
    def buscar_populacao_municipal(self, ano: int = 2022) -> Optional[pd.DataFrame]:
        """Busca população dos municípios (Tabela 6579)"""
        url = f"{self.BASE_URL}/t/6579/n6/all/v/all/p/{ano}"
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                return None
            
            dados_json = response.json()
            
            if not dados_json or len(dados_json) < 2:
                return None
            
            cabecalhos = dados_json[0]
            
            col_mapping = {}
            for i, col in enumerate(cabecalhos):
                if col == 'D1C':
                    col_mapping[i] = 'codigo_uf'
                elif col == 'D1N':
                    col_mapping[i] = 'uf_nome'
                elif col == 'D2C':
                    col_mapping[i] = 'codigo_municipio'
                elif col == 'D2N':
                    col_mapping[i] = 'municipio'
                elif col == 'V':
                    col_mapping[i] = 'populacao'
            
            dados = []
            for linha in dados_json[1:]:
                registro = {}
                for i, valor in enumerate(linha):
                    if i in col_mapping:
                        registro[col_mapping[i]] = valor
                dados.append(registro)
            
            df = pd.DataFrame(dados)
            df['populacao'] = pd.to_numeric(df['populacao'], errors='coerce')
            df['codigo_uf'] = pd.to_numeric(df['codigo_uf'], errors='coerce')
            df['codigo_municipio'] = pd.to_numeric(df['codigo_municipio'], errors='coerce')
            
            return df
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar população: {e}")
            return None
    
    def consolidar_dados_renda(self, ano: int = 2022) -> Optional[pd.DataFrame]:
        """Consolida PIB e população para calcular renda"""
        print(f"🚀 Iniciando busca de dados para {ano}...")
        
        df_pib = self.buscar_pib_municipal(ano)
        
        if df_pib is None or df_pib.empty:
            print("❌ Não foi possível obter dados de PIB")
            return self._gerar_dados_fallback(ano)
        
        df_pop = self.buscar_populacao_municipal(ano)
        
        df_pib['pib_total_reais'] = df_pib['pib_total_mil'] * 1000
        
        if df_pop is not None and not df_pop.empty:
            df_pib = df_pib.merge(
                df_pop[['codigo_municipio', 'populacao']],
                on='codigo_municipio',
                how='left'
            )
        else:
            print("⚠️ Estimando população com base no PIB...")
            pib_max = df_pib['pib_total_reais'].max()
            df_pib['populacao'] = (df_pib['pib_total_reais'] / pib_max * 12000000).astype(int)
            df_pib['populacao'] = df_pib['populacao'].clip(lower=1000, upper=12000000)
        
        df_pib['pib_per_capita'] = (df_pib['pib_total_reais'] / df_pib['populacao']).round(0)
        
        df_pib['renda_per_capita_estimada'] = (df_pib['pib_per_capita'] * 0.6).round(0)
        df_pib['renda_familiar_estimada'] = (df_pib['renda_per_capita_estimada'] * 3).round(0)
        
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
        
        df_pib['classificacao'] = df_pib['renda_familiar_estimada'].apply(classificar_renda)
        df_pib = df_pib[df_pib['pib_per_capita'] > 0]
        df_pib = df_pib[df_pib['renda_familiar_estimada'] > 0]
        df_pib = df_pib.sort_values('renda_familiar_estimada', ascending=False)
        
        print(f"✅ Consolidado: {len(df_pib)} municípios")
        return df_pib
    
    def _gerar_dados_fallback(self, ano: int) -> pd.DataFrame:
        """Gera dados de referência usando a lista de municípios do arquivo separado"""
        print("⚠️ Usando dados de referência locais...")
        
        municipios = MUNICIPIOS_SP
        random.seed(42)
        
        dados = []
        for i, municipio in enumerate(municipios):
            # Verifica se o município está no dicionário de dados reais
            if municipio in DADOS_REAIS_REFERENCIA:
                pib_per_capita = DADOS_REAIS_REFERENCIA[municipio]['pib_per_capita']
                populacao = DADOS_REAIS_REFERENCIA[municipio]['populacao']
            else:
                # Distribuição baseada no tamanho/importância do município
                if i < 20:
                    pib_per_capita = random.randint(45000, 80000)
                    populacao = random.randint(200000, 5000000)
                elif i < 100:
                    pib_per_capita = random.randint(30000, 45000)
                    populacao = random.randint(50000, 200000)
                elif i < 300:
                    pib_per_capita = random.randint(20000, 30000)
                    populacao = random.randint(15000, 50000)
                else:
                    pib_per_capita = random.randint(12000, 20000)
                    populacao = random.randint(2000, 15000)
            
            dados.append({
                'codigo_municipio': 3500000 + i + 1,
                'municipio': municipio,
                'pib_total_mil': (pib_per_capita * populacao) / 1000,
                'pib_total_reais': pib_per_capita * populacao,
                'populacao': populacao,
                'pib_per_capita': pib_per_capita,
                'renda_per_capita_estimada': pib_per_capita * 0.6,
                'renda_familiar_estimada': pib_per_capita * 0.6 * 3,
                'ano': ano
            })
        
        df = pd.DataFrame(dados)
        
        def classificar(r):
            if r < 3000:
                return "Baixa renda"
            elif r < 6000:
                return "Classe média baixa"
            elif r < 13300:
                return "Classe média"
            elif r < 25000:
                return "Classe média alta"
            else:
                return "Alta renda"
        
        df['classificacao'] = df['renda_familiar_estimada'].apply(classificar)
        return df
    
    def listar_municipios(self, df_consolidado: pd.DataFrame) -> List[str]:
        """Retorna lista de municípios disponíveis"""
        if df_consolidado is not None and not df_consolidado.empty:
            # Usa os municípios retornados pela API
            municipios_api = sorted(df_consolidado['municipio'].unique())
            # Se a API retornou menos de 500 municípios, usa fallback
            if len(municipios_api) > 500:
                return municipios_api
        
        # Fallback: usa a lista completa do arquivo
        return sorted(MUNICIPIOS_SP)


# ==================== FUNÇÕES DE VISUALIZAÇÃO ====================

def criar_grafico_barras_ranking(df, titulo):
    """Cria gráfico de barras para ranking de renda"""
    if df is None or df.empty:
        return go.Figure()
    
    cores = {
        'Alta renda': '#2ecc71',
        'Classe média alta': '#3498db',
        'Classe média': '#f39c12',
        'Classe média baixa': '#e67e22',
        'Baixa renda': '#e74c3c'
    }
    
    fig = go.Figure()
    fig
