# 💰 Dashboard de Renda por Município - Estado de São Paulo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seu-app.streamlit.app)

Dashboard interativo para visualização da renda média por município do estado de São Paulo, utilizando dados oficiais do IBGE.

## 🎯 Funcionalidades

- ✅ **Filtro por município** - Selecione qualquer cidade paulista para ver seus dados
- ✅ **Renda familiar estimada** - Baseada na renda per capita do Censo 2022
- ✅ **Classificação automática** - Enquadra o município nas faixas definidas:
  - Alta renda: acima de R$ 25.000
  - Classe média alta: R$ 13.300 a R$ 25.000
  - Classe média: R$ 6.000 a R$ 13.300
- ✅ **Gráfico mensal** - Visualização de tendência (mês e valor)
- ✅ **Ranking completo** - Veja os municípios com maior e menor renda
- ✅ **Comparação entre cidades** - Compare múltiplos municípios lado a lado
- ✅ **Exportação de dados** - Baixe os dados em CSV

## 📊 Fontes de Dados

| Fonte | Dado | Ano |
|-------|------|-----|
| IBGE SIDRA (Tabela 5938) | PIB per capita | Último disponível |
| IBGE Censo 2022 | Renda domiciliar per capita | 2022 |
| IBGE Censo 2022 | População municipal | 2022 |

## 🚀 Como executar localmente

### Pré-requisitos

- Python 3.9 ou superior
- Pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/dashboard-renda-sp.git
cd dashboard-renda-sp

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
