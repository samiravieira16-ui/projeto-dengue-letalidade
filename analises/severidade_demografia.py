import pandas as pd
import glob
import os

def exibir_grafico_demografico_ascii(df_dist):
    """Exibe um gráfico visual simples da distribuição de óbitos por faixa etária."""
    # Removemos a linha 'Total_Geral' para não distorcer o gráfico
    df_plot = df_dist.drop('Total_Geral', axis=0, errors='ignore')
    
    # Usamos o total da linha para a barra
    max_val = df_plot['Total_Geral'].max()
    max_width = 40

    print(f"\n{'='*75}")
    print(f"{'📊 GRÁFICO: DISTRIBUIÇÃO DE ÓBITOS POR FAIXA ETÁRIA':^75}")
    print(f"{'='*75}\n")

    for faixa, row in df_plot.iterrows():
        total = int(row['Total_Geral'])
        size = int((total / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        print(f"  {faixa:>7} | {barra:<40} {total:>4} óbitos")

    print(f"\n{'='*75}\n")

def analisar_severidade_demografia_absoluta(pasta_dados):
    """Analisa a distribuição absoluta de óbitos por Sexo e Faixa Etária."""
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    
    if not arquivos:
        print(f"⚠ Nenhum arquivo .parquet encontrado em: {pasta_dados}")
        return None

    lista_obitos = []
    print(f"⏳ Analisando demografia de óbitos em {len(arquivos)} arquivos...")

    for arquivo in arquivos:
        try:
            # Leitura otimizada e prevenção de erros de tipo (Categorical/String)
            df = pd.read_parquet(arquivo, columns=["Idade_Em_Anos", "Sexo", "Desfecho_Caso"]).copy()
            
            # Padronização do Desfecho
            df["Desfecho_Caso"] = df["Desfecho_Caso"].astype(str).str.replace(".0", "", regex=False).str.strip()
            
            # Filtro estrito: Óbito (2) e remoção de nulos
            df_obitos = df[df["Desfecho_Caso"] == "2"].dropna(subset=["Idade_Em_Anos", "Sexo"]).copy()

            if not df_obitos.empty:
                # Garantir que Sexo seja string limpa (M/F)
                df_obitos["Sexo"] = df_obitos["Sexo"].astype(str).str.upper().str.strip()
                lista_obitos.append(df_obitos)
                print(f"✔ {os.path.basename(arquivo)}: {len(df_obitos)} óbitos extraídos")

        except Exception as e:
            print(f"❌ Erro ao processar {os.path.basename(arquivo)}: {e}")

    if not lista_obitos:
        print("⚠ Nenhum óbito (Desfecho 2) encontrado nos arquivos.")
        return None

    df_final = pd.concat(lista_obitos, ignore_index=True)

    # 3. Definição das Faixas Etárias
    bins = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 120]
    labels = ['0-4', '5-9', '10-14', '15-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
    df_final['Faixa_Etaria'] = pd.cut(df_final['Idade_Em_Anos'], bins=bins, labels=labels, right=False)

    # 4. Cruzamento Absoluto: Sexo vs Faixa Etária
    distribuicao_absoluta = pd.crosstab(
        df_final['Faixa_Etaria'], 
        df_final['Sexo'], 
        margins=True, 
        margins_name="Total_Geral"
    )

    # Exibição no Terminal seguindo o padrão
    print(f"\n{'-'*75}")
    print(f"{'TABELA: ÓBITOS POR SEXO E FAIXA ETÁRIA':^75}")
    print(f"{'-'*75}")
    print(distribuicao_absoluta)
    print(f"{'-'*75}")

    exibir_grafico_demografico_ascii(distribuicao_absoluta)

    print(f"✅ Análise concluída. Total: {len(df_final)} óbitos.\n")

    return distribuicao_absoluta

if __name__ == "__main__":
    analisar_severidade_demografia_absoluta("dados")