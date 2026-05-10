# 💰 Dashboard Renda por Município - SP

Dashboard interativo com dados oficiais do IBGE para os 645 municípios paulistas.

## 🚀 Como executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
streamlit run app.py
📊 Funcionalidades
🔍 Busca por qualquer município de SP

💰 Renda familiar estimada

👥 População com separador de milhar

🏆 Ranking estadual

📈 Gráficos interativos

📥 Exportação CSV

📁 Estrutura
text
app.py              # Aplicação principal
src/
├── municipios_sp.py # Lista dos 645 municípios
├── data_loader.py   # API IBGE
├── data_processor.py # Processamento
└── charts.py        # Gráficos
🔧 Tecnologias
Streamlit

Pandas

Plotly

Requests (API IBGE)

📊 Fonte dos Dados
IBGE SIDRA - Tabela 5938 (PIB Municipal)

IBGE SIDRA - Tabela 6579 (População)

📈 Faixas de Renda
Classificação	Renda Familiar
🟢 Alta renda	Acima R$ 25.000
🔵 Classe média alta	R
13.300
−
R
13.300−R 25.000
🟡 Classe média	R
6.000
−
R
6.000−R 13.300
🟠 Classe média baixa	R
3.000
−
R
3.000−R 6.000
🔴 Baixa renda	Até R$ 3.000
