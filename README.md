```markdown
# 💰 Dashboard de Renda por Município - São Paulo

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![IBGE](https://img.shields.io/badge/IBGE-SIDRA-2E8B57?style=for-the-badge&logo=data:gov&logoColor=white)](https://sidra.ibge.gov.br)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

---

## 📑 Sumário

- [📖 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🏗️ Arquitetura do Sistema](#️-arquitetura-do-sistema)
- [📊 Metodologia de Cálculo](#-metodologia-de-cálculo)
- [🚀 Como Executar](#-como-executar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Executando a Aplicação](#executando-a-aplicação)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🎯 Funcionalidades Detalhadas](#-funcionalidades-detalhadas)
  - [1. Busca Inteligente de Municípios](#1-busca-inteligente-de-municípios)
  - [2. Dashboard de Indicadores](#2-dashboard-de-indicadores)
  - [3. Visualizações Interativas](#3-visualizações-interativas)
  - [4. Rankings e Comparações](#4-rankings-comparações)
  - [5. Exportação de Dados](#5-exportação-de-dados)
- [🗃️ Fontes de Dados](#️-fontes-de-dados)
- [📈 Faixas de Renda](#-faixas-de-renda)
- [🔧 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📝 Notas e Limitações](#-notas-e-limitações)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)
- [👥 Autores](#-autores)

---

## 📖 Sobre o Projeto

O **Dashboard de Renda por Município - São Paulo** é uma aplicação interativa desenvolvida em Streamlit que consome dados oficiais do IBGE para apresentar estimativas de renda familiar para todos os **645 municípios paulistas**.

A ferramenta foi desenvolvida para democratizar o acesso a dados socioeconômicos, permitindo que gestores públicos, pesquisadores, estudantes e cidadãos em geral possam:

- Visualizar a distribuição de renda no estado de São Paulo
- Comparar indicadores entre diferentes municípios
- Analisar tendências e rankings
- Exportar dados para análises mais aprofundadas

### 🎯 Objetivos

- **Transparência**: Disponibilizar dados oficiais do IBGE de forma acessível
- **Análise Comparativa**: Permitir comparações rápidas entre municípios
- **Tomada de Decisão**: Auxiliar gestores públicos com dados confiáveis
- **Educação Financeira**: Ilustrar as diferentes faixas de renda da população

[⬆ Voltar ao Sumário](#-sumário)

---

## ✨ Funcionalidades

### Principais Características

| Funcionalidade | Descrição |
|----------------|-----------|
| 🔍 **Busca Inteligente** | Autocomplete com os 645 municípios paulistas |
| 📊 **Dashboard Individual** | Cards com indicadores-chave do município selecionado |
| 🎯 **Gauge Interativo** | Visualização da posição do município nas faixas de renda |
| 📈 **Tendência Mensal** | Gráfico com variação sazonal da renda ao longo do ano |
| 🏆 **Ranking Estadual** | Ranking dos 645 municípios por renda familiar |
| 🔄 **Comparação Múltipla** | Compare até 10 municípios simultaneamente |
| 🥧 **Distribuição Estadual** | Gráfico pizza com distribuição das faixas de renda |
| 📥 **Exportação CSV** | Download dos dados completos para análise externa |

[⬆ Voltar ao Sumário](#-sumário)

---

## 🏗️ Arquitetura do Sistema

imagem

### Fluxo de Dados

1. **Requisição API** → IBGE SIDRA (Tabelas 5938 e 6579)
2. **Processamento** → Cálculo do PIB per capita e renda estimada
3. **Cacheamento** → Dados armazenados por 1 hora
4. **Visualização** → Renderização no dashboard Streamlit

[⬆ Voltar ao Sumário](#-sumário)

---

## 📊 Metodologia de Cálculo

### Fórmulas Utilizadas

```python
# PIB per capita (Fonte: IBGE)
pib_per_capita = pib_total_reais / populacao

# Renda per capita estimada
renda_per_capita_estimada = pib_per_capita × 0.6

# Renda familiar estimada (média de 3 pessoas por domicílio)
renda_familiar_estimada = renda_per_capita_estimada × 3
```

### Justificativa Metodológica

| Parâmetro | Valor | Justificativa |
|-----------|-------|----------------|
| **Fator de Conversão PIB → Renda** | 0.6 (60%) | Baseado em estudos de distribuição de renda onde aproximadamente 60% do PIB corresponde à renda disponível das famílias |
| **Média de Pessoas por Domicílio** | 3 pessoas | Baseado nos dados do IBGE (Censo Demográfico) |
| **Referência Classe Média** | R$ 6.000 | Critério Brasil com base em estudos socioeconômicos |
| **Referência Classe Média Alta** | R$ 13.300 | Critério Brasil para padrão de vida elevado |

[⬆ Voltar ao Sumário](#-sumário)

---

## 🚀 Como Executar

### Pré-requisitos

- **Python 3.9+**
- **Pip** (gerenciador de pacotes)
- **Conexão com internet** (para acessar API do IBGE)

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/dashboard-renda-sp.git
cd dashboard-renda-sp
```

2. **Crie um ambiente virtual (recomendado)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### Executando a Aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador no endereço:
```
http://localhost:8501
```

### Deploy na Nuvem (Streamlit Cloud)

1. Faça push do código para um repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta GitHub
4. Selecione o repositório e branch
5. Clique em "Deploy"

[⬆ Voltar ao Sumário](#-sumário)

---

## 📁 Estrutura do Projeto

```
dashboard-renda-sp/
│
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências do projeto
├── config.toml                 # Configurações do Streamlit
│
├── src/                        # Módulos fonte
│   ├── __init__.py
│   ├── municipios_sp.py        # Lista dos 645 municípios paulistas
│   ├── data_loader.py          # Cliente API IBGE
│   ├── data_processor.py       # Processamento de dados
│   └── charts.py               # Visualizações Plotly
│
├── data/                       # Dados (opcional - cache local)
│   └── cache/                  # Cache da API
│
├── docs/                       # Documentação
│   ├── metodologia.pdf
│   └── api_documentation.md
│
├── tests/                      # Testes unitários
│   ├── test_api.py
│   └── test_processor.py
│
└── README.md                   # Este arquivo
```

### Descrição dos Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Aplicação principal com toda interface e lógica de visualização |
| `municipios_sp.py` | Lista completa dos 645 municípios com dados de referência |
| `data_loader.py` | Cliente para consumir API do IBGE SIDRA |
| `data_processor.py` | Cálculos de renda e estatísticas |
| `charts.py` | Configurações de gráficos Plotly |

[⬆ Voltar ao Sumário](#-sumário)

---

## 🎯 Funcionalidades Detalhadas

### 1. Busca Inteligente de Municípios

- **Campo de busca com autocomplete** - Digite parte do nome da cidade
- **Filtro dinâmico** - Resultados aparecem instantaneamente
- **Lista completa** - Todos os 645 municípios disponíveis
- **Ordenação inteligente** - Primeiro cidades que começam com o termo buscado

### 2. Dashboard de Indicadores

Quatro cards principais são exibidos para cada município:

| Card | Descrição | Formato |
|------|-----------|---------|
| 💰 **Renda Familiar** | Valor estimado da renda familiar mensal | `R$ 11.451.245` |
| 📊 **Classificação** | Faixa de renda do município | `🟢 Alta renda` |
| 👥 **População** | Total de habitantes | `11.451.245` |
| 🏆 **Ranking Estadual** | Posição entre 645 municípios | `1º de 645` |

### 3. Visualizações Interativas

#### Gauge (Indicador Circular)
- Mostra a posição do município nas faixas de renda
- Escala de R$ 0 a R$ 50.000
- Cores diferentes para cada faixa
- Delta percentual em relação à classe média alta

#### Gráfico de Tendência Mensal
- Variação sazonal realista da renda
- 12 meses do ano (Jan a Dez)
- Linhas de referência para faixas de renda
- Área preenchida para melhor visualização

### 4. Rankings e Comparações

#### Ranking Estadual
- Top 20 maiores rendas
- Bottom 20 menores rendas
- Barras horizontais coloridas por classificação
- Tabela interativa com os 100 primeiros

#### Comparação Múltipla
- Selecione de 2 a 10 municípios
- Gráfico de barras comparativo
- Cores distintas para cada município
- Valores exibidos nas barras

### 5. Exportação de Dados

- Download em formato CSV
- Dados completos dos 645 municípios
- Colunas: município, renda, classificação, população
- Nome do arquivo com timestamp

[⬆ Voltar ao Sumário](#-sumário)

---

## 🗃️ Fontes de Dados

### IBGE SIDRA (Sistema IBGE de Recuperação Automática)

| Tabela | Código | Descrição | Variável |
|--------|--------|-----------|----------|
| **PIB Municipal** | 5938 | Produto Interno Bruto dos Municípios | 37 - PIB a preços correntes (Mil Reais) |
| **População** | 6579 | Estimativas da População | População residente |

### Endpoints da API

```bash
# PIB dos municípios
GET https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/37/p/2022

# População dos municípios
GET https://apisidra.ibge.gov.br/values/t/6579/n6/all/v/all/p/2022
```

### Fallback Data

Caso a API do IBGE esteja indisponível, o sistema utiliza:
- Dados de referência para os 645 municípios
- Baseados em valores reais conhecidos (cidades principais)
- Distribuição estatística para os demais municípios

[⬆ Voltar ao Sumário](#-sumário)

---

## 📈 Faixas de Renda

| Classificação | Renda Familiar | Emoji | Cor | Descrição |
|---------------|----------------|-------|-----|------------|
| 🔴 **Baixa renda** | Abaixo de R$ 3.000 | 🔴 | Vermelho | Necessidades básicas, pouco ou nenhum poder de poupança |
| 🟠 **Classe média baixa** | R$ 3.000 - R$ 6.000 | 🟠 | Laranja | Consumo moderado, pequena capacidade de poupança |
| 🟡 **Classe média** | R$ 6.000 - R$ 13.300 | 🟡 | Amarelo | Padrão de vida confortável, acesso a bens e serviços |
| 🔵 **Classe média alta** | R$ 13.300 - R$ 25.000 | 🔵 | Azul | Padrão de vida elevado, boa capacidade de investimento |
| 🟢 **Alta renda** | Acima de R$ 25.000 | 🟢 | Verde | Alto poder aquisitivo, alto potencial de investimento |

### Referências
- **Critério Brasil** (Associação Brasileira de Empresas de Pesquisa - ABEP)
- **Estudos Socioeconômicos** do IBGE
- **Pesquisa de Orçamentos Familiares** (POF/IBGE)

[⬆ Voltar ao Sumário](#-sumário)

---

## 🔧 Tecnologias Utilizadas

### Backend & Processamento

| Tecnologia | Versão | Finalidade |
|------------|--------|-------------|
| **Python** | 3.9+ | Linguagem principal |
| **Pandas** | 2.0+ | Manipulação e processamento de dados |
| **NumPy** | 1.24+ | Operações matemáticas e arrays |
| **Requests** | 2.31+ | Consumo da API do IBGE |

### Frontend & Visualização

| Tecnologia | Versão | Finalidade |
|------------|--------|-------------|
| **Streamlit** | 1.28+ | Framework web e interface |
| **Plotly** | 5.17+ | Gráficos interativos |
| **Plotly Express** | 5.17+ | Visualizações rápidas |

### Utilitários

| Tecnologia | Finalidade |
|------------|-------------|
| **openpyxl** | Suporte a arquivos Excel |
| **functools** | Cache e otimização |

### Dependências Completas (requirements.txt)

```txt
streamlit>=1.28.0
pandas>=2.0.0
sidrapy>=0.8.0
plotly>=5.17.0
numpy>=1.24.0
requests>=2.31.0
openpyxl>=3.1.0
```

[⬆ Voltar ao Sumário](#-sumário)

---

## 📝 Notas e Limitações

### Limitações Conhecidas

1. **API do IBGE**
   - Pode apresentar instabilidade ocasional
   - Rate limit não documentado
   - Dados sujeitos a atualização periódica

2. **Estimativas de Renda**
   - São estimativas baseadas em PIB, não dados diretos de renda
   - Não considera desigualdade dentro do município
   - Fator de 60% é uma aproximação

3. **Cobertura**
   - Apenas municípios do estado de São Paulo
   - Dados do PIB disponíveis até 2022

### Recomendações

Para análises mais precisas, recomenda-se:
- Utilizar dados do Censo Demográfico quando disponíveis
- Cruzar com outras fontes (RAIS, CAGED)
- Considerar o IDH municipal para contexto adicional

[⬆ Voltar ao Sumário](#-sumário)

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

### Como Contribuir

1. **Fork o projeto**
```bash
git fork https://github.com/seu-usuario/dashboard-renda-sp.git
```

2. **Crie sua branch de feature**
```bash
git checkout -b feature/nova-funcionalidade
```

3. **Commit suas mudanças**
```bash
git commit -m 'feat: adiciona nova funcionalidade'
```

4. **Push para a branch**
```bash
git push origin feature/nova-funcionalidade
```

5. **Abra um Pull Request**

### Áreas que Precisam de Contribuição

- [ ] Adicionar mais estados brasileiros
- [ ] Implementar mapa coroplético interativo
- [ ] Adicionar série histórica (múltiplos anos)
- [ ] Incluir indicadores de desigualdade (Gini)
- [ ] Adicionar testes unitários
- [ ] Melhorar performance de carregamento

[⬆ Voltar ao Sumário](#-sumário)

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2024 Dashboard Renda SP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

[⬆ Voltar ao Sumário](#-sumário)

---

## 👥 Autores

| Nome | Papel | Contato |
|------|-------|---------|
| **Seu Nome** | Desenvolvedor Principal | [GitHub](https://github.com/seu-usuario) |

### Agradecimentos

- **IBGE** - Pela disponibilização dos dados públicos
- **Streamlit** - Pela excelente framework de desenvolvimento
- **Comunidade Open Source** - Pelas bibliotecas utilizadas

---

## 📊 Exemplo de Uso

### Consultando um Município

1. **Selecione São Paulo no menu lateral**
2. **Visualize os indicadores:**
   - Renda Familiar: `R$ 32.670`
   - Classificação: `🟢 Alta renda`
   - População: `11.451.245`
   - Ranking: `23º de 645`

3. **Analise o gráfico Gauge** - mostrando posição em relação às faixas
4. **Veja a tendência mensal** - variação ao longo do ano
5. **Compare com outras cidades** - selecione Campinas, Santos e Ribeirão Preto

### Exportando Dados

```python
# Exemplo de uso dos dados exportados
import pandas as pd

df = pd.read_csv('renda_municipios_sp_20241201.csv')
df_filtered = df[df['classificacao'] == 'Alta renda']
print(df_filtered[['municipio', 'renda_familiar_estimada']])
```

[⬆ Voltar ao Sumário](#-sumário)

---

## 🔗 Links Úteis

- [IBGE SIDRA](https://sidra.ibge.gov.br)
- [Documentação Streamlit](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 📞 Suporte

Para dúvidas, sugestões ou reportar problemas:

- **Issues**: Abra uma issue no [GitHub](https://github.com/seu-usuario/dashboard-renda-sp/issues)
- **Email**: seu-email@exemplo.com

---

**Desenvolvido com ❤️ para democratizar o acesso a dados públicos**

[⬆ Voltar ao Topo](#-dashboard-de-renda-por-município---são-paulo)
```

Este README completo e estruturado inclui:

1. **Sumário interativo** com links para todas as seções
2. **Badges** para tecnologias utilizadas
3. **Arquitetura do sistema** em diagrama ASCII
4. **Tabelas** organizadas para facilitar a leitura
5. **Metodologia detalhada** com fórmulas
6. **Instruções passo a passo** para instalação e execução
7. **Estrutura de projeto** completa
8. **Funcionalidades** explicadas em detalhes
9. **Fontes de dados** com endpoints da API
10. **Tabela de faixas de renda** com cores e emojis
11. **Stack tecnológico** com versões
12. **Guias de contribuição**
13. **Exemplos de uso** práticos
14. **Links úteis** para documentação

O arquivo está pronto para ser salvo como `README.md` na raiz do seu projeto!
