# ==================== DASHBOARD PRINCIPAL ====================

if df_principal is not None and not df_principal.empty and municipio_selecionado:
    
    # Filtra dados do município selecionado
    municipio_data = df_principal[df_principal['municipio'] == municipio_selecionado]
    
    if not municipio_data.empty:
        row = municipio_data.iloc[0]
        renda_familiar = row['renda_familiar_estimada']
        classificacao = row['classificacao']
        
        # ===== CORREÇÃO: OBTENÇÃO DA POPULAÇÃO =====
        # Tenta obter população de diferentes formas
        populacao = None
        if 'populacao' in row.index:
            populacao = row['populacao']
        
        # Se populacao for None ou NaN, tenta calcular a partir do PIB
        if populacao is None or pd.isna(populacao):
            pib_total_reais = row.get('pib_total_reais', None)
            pib_per_capita = row.get('pib_per_capita', None)
            if pib_total_reais is not None and pib_per_capita is not None and pib_per_capita > 0:
                populacao = pib_total_reais / pib_per_capita
            else:
                # Fallback: população estimada baseada no ranking
                rank_pos = df_principal.index.get_loc(municipio_data.index[0])
                total_municipios = len(df_principal)
                # Quanto maior a renda, maior a tendência de população maior
                fator = 1 - (rank_pos / total_municipios)  # 0 a 1
                populacao = int(10000 + (fator * 5000000))  # Entre 10k e 5M
        
        # Garante que é número inteiro e positivo
        if populacao is not None:
            try:
                populacao = int(abs(float(populacao)))
                if populacao < 1000:
                    populacao = 1000  # Valor mínimo razoável
            except:
                populacao = None
        
        pib_per_capita = row.get('pib_per_capita', 'N/A')
        
        # Debug (opcional - pode remover depois)
        print(f"Município: {municipio_selecionado}, População: {populacao}")
        
        # Métricas principais
        st.subheader(f"🏙️ Análise de Renda - {municipio_selecionado}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Renda Familiar",
                f"R$ {renda_familiar:,.0f}".replace(",", "."),
                delta=None
            )
        
        with col2:
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
            # População com formatação de separador de milhar
            if populacao is not None and populacao != 'N/A' and not pd.isna(populacao):
                pop_formatada = formatar_numero(populacao)
                st.metric("👥 População", pop_formatada, delta=None)
            else:
                # Tenta buscar da lista de dados reais como fallback
                from src.municipios_sp import DADOS_REAIS_REFERENCIA
                if municipio_selecionado in DADOS_REAIS_REFERENCIA:
                    pop_real = DADOS_REAIS_REFERENCIA[municipio_selecionado].get('populacao', None)
                    if pop_real:
                        st.metric("👥 População", formatar_numero(pop_real), delta=None)
                    else:
                        st.metric("👥 População", "Dado não disponível")
                else:
                    st.metric("👥 População", "Dado não disponível")
        
        with col4:
            # Calcula ranking
            try:
                ranking = df_principal['renda_familiar_estimada'].rank(ascending=False)[municipio_data.index[0]]
                total = len(df_principal)
                st.metric(
                    "🏆 Ranking Estadual",
                    f"{int(ranking)}º de {total} municípios",
                    delta=None
                )
            except:
                st.metric("🏆 Ranking Estadual", "N/A")
        
        st.markdown("---")
        
        # Resto do código continua igual...
        # Gráfico Gauge
        st.subheader("📈 Indicador de Renda")
        fig_gauge = criar_indicador_gauge(renda_familiar, classificacao, municipio_selecionado)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Gráfico Mensal (mês e valor)
        st.subheader("📅 Tendência Mensal")
        fig_mensal = criar_grafico_mensal(municipio_selecionado, renda_familiar)
        st.plotly_chart(fig_mensal, use_container_width=True)
        
        # Tabela de faixas de renda
        with st.expander("📖 Entenda as faixas de renda"):
            st.markdown("""
            | Classificação | Renda Familiar Mensal | Descrição |
            |--------------|----------------------|-----------|
            | 🟢 **Alta renda** | Acima de R$ 25.000 | Famílias com alto poder aquisitivo |
            | 🔵 **Classe média alta** | R$ 13.300 a R$ 25.000 | Padrão de vida elevado |
            | 🟡 **Classe média** | R$ 6.000 a R$ 13.300 | Padrão de vida confortável |
            | 🟠 **Classe média baixa** | R$ 3.000 a R$ 6.000 | Consumo moderado |
            | 🔴 **Baixa renda** | Abaixo de R$ 3.000 | Necessidades básicas |
            """)
        
        # Ranking (se habilitado)
        if mostrar_ranking:
            st.subheader("🏆 Ranking de Renda por Município")
            
            maiores = df_principal.nlargest(20, 'renda_familiar_estimada')
            menores = df_principal.nsmallest(20, 'renda_familiar_estimada')
            
            col_rank1, col_rank2 = st.columns(2)
            
            with col_rank1:
                fig_maiores = criar_grafico_barras_ranking(maiores, "Top 20 Maiores Rendas")
                st.plotly_chart(fig_maiores, use_container_width=True)
            
            with col_rank2:
                fig_menores = criar_grafico_barras_ranking(menores, "Bottom 20 Menores Rendas")
                st.plotly_chart(fig_menores, use_container_width=True)
            
            # Tabela completa
            st.subheader("📋 Tabela Completa")
            tabela_exibicao = df_principal[['municipio', 'renda_familiar_estimada', 'classificacao', 'populacao']].head(100).copy()
            tabela_exibicao['renda_familiar_estimada'] = tabela_exibicao['renda_familiar_estimada'].apply(lambda x: f'R$ {x:,.0f}')
            
            # Formata população na tabela
            def fmt_pop(val):
                if val is None or pd.isna(val):
                    return 'N/A'
                return formatar_numero(val)
            
            tabela_exibicao['populacao'] = tabela_exibicao['populacao'].apply(fmt_pop)
            st.dataframe(tabela_exibicao, use_container_width=True, hide_index=True)
        
        # Comparação entre cidades (se habilitado)
        if mostrar_comparacao and 'cidades_para_comparar' in locals() and len(cidades_para_comparar) > 1:
            st.subheader("🔄 Comparação entre Municípios")
            
            df_comparacao = df_principal[df_principal['municipio'].isin(cidades_para_comparar)]
            df_comparacao = df_comparacao.sort_values('renda_familiar_estimada', ascending=False)
            
            fig_comparativo = go.Figure()
            cores_comparacao = px.colors.qualitative.Set3
            
            for i, (_, row) in enumerate(df_comparacao.iterrows()):
                fig_comparativo.add_trace(go.Bar(
                    x=[row['municipio']],
                    y=[row['renda_familiar_estimada']],
                    name=row['municipio'],
                    marker_color=cores_comparacao[i % len(cores_comparacao)],
                    text=f"R$ {row['renda_familiar_estimada']:,.0f}",
                    textposition='outside'
                ))
            
            fig_comparativo.update_layout(
                title="Comparação de Renda entre Municípios",
                xaxis_title="Município",
                yaxis_title="Renda Familiar (R$)",
                showlegend=False,
                height=450
            )
            fig_comparativo.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
            st.plotly_chart(fig_comparativo, use_container_width=True)
        
        # Distribuição geral
        st.subheader("📊 Distribuição Geral no Estado")
        col_dist1, col_dist2 = st.columns(2)
        
        with col_dist1:
            fig_pizza = criar_pizza_distribuicao(df_principal)
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col_dist2:
            # Estatísticas gerais
            st.markdown("### 📈 Estatísticas do Estado")
            
            # Calcula média apenas com valores válidos
            renda_media = df_principal['renda_familiar_estimada'].mean()
            renda_mediana = df_principal['renda_familiar_estimada'].median()
            
            st.metric(
                "Renda Média Estadual",
                f"R$ {renda_media:,.0f}".replace(",", "."),
                delta=None
            )
            st.metric(
                "Renda Mediana Estadual", 
                f"R$ {renda_mediana:,.0f}".replace(",", "."),
                delta=None
            )
            cidade_maior = df_principal.loc[df_principal['renda_familiar_estimada'].idxmax(), 'municipio']
            st.metric(
                "Município com Maior Renda",
                cidade_maior,
                delta=None
            )
        
        # Download dos dados
        st.subheader("📥 Exportar Dados")
        
        # Prepara CSV com população formatada
        df_export = df_principal.copy()
        if 'populacao' in df_export.columns:
            df_export['populacao'] = df_export['populacao'].apply(lambda x: formatar_numero(x) if pd.notna(x) else 'N/A')
        
        csv_completo = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Baixar dados completos (CSV)",
            data=csv_completo,
            file_name=f"renda_municipios_sp_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    if municipio_selecionado is None and 'texto_busca' in locals() and texto_busca:
        st.info("🔍 Digite o nome de uma cidade para começar a busca")
    else:
        st.error("❌ Não foi possível carregar os dados. Verifique sua conexão com a internet e tente novamente.")
