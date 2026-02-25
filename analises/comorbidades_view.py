import pandas as pd
import glob
import os

# Lista de colunas de comorbidade
COMORBIDADES = [
    "Comorb_Diabetes", "Comorb_Hematolog", "Comorb_Hepatopat",
    "Comorb_Renal", "Comorb_Hipertensao", "Comorb_AcidoPeptica",
    "Comorb_AutoImune"
]

def exibir_grafico_ascii_comorbidades(df):
    """Exibe um gráfico de barras em ASCII baseado na letalidade."""
    if df.empty:
        return

    # Ordenar para o gráfico ficar em escada (opcional, mas visualmente melhor)
    df_plot = df.sort_values('Letalidade_%', ascending=True)
    max_val = df_plot['Letalidade_%'].max()
    max_width = 40  # Largura máxima da barra no terminal

    print(f"\n{'='*85}")
    print(f"{'📊 GRÁFICO: LETALIDADE (%) POR COMORBIDADE':^85}")
    print(f"{'='*85}\n")

    for _, row in df_plot.iterrows():
        nome = row['Comorbidade']
        letal = row['Letalidade_%']
        obitos = int(row['Obitos'])
        casos = int(row['Casos'])
        
        # Desenha a barra proporcional
        size = int((letal / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        
        print(f"  {nome:<15} {barra:<40} {letal:6.2f}% ({obitos}/{casos})")

    print(f"\n{'='*85}\n")

def analisar_letalidade_comorbidades(pasta_dados):
    """Calcula letalidade e exibe tabela e gráfico."""
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    if not arquivos:
        print(f"⚠ Erro: Pasta '{pasta_dados}' não encontrada.")
        return

    total_casos = {c: 0 for c in COMORBIDADES}
    total_obitos = {c: 0 for c in COMORBIDADES}

    print(f"⏳ Processando {len(arquivos)} arquivos...")

    for arq in arquivos:
        try:
            # Lemos apenas as colunas necessárias e convertemos para String imediatamente
            df_temp = pd.read_parquet(arq, columns=COMORBIDADES + ["Desfecho_Caso"])
            
            # Normalização para evitar erro de 'Categorical' e padronizar valores
            for col in df_temp.columns:
                df_temp[col] = df_temp[col].astype(str).str.replace('.0', '', regex=False).str.strip()

            for c in COMORBIDADES:
                if c in df_temp.columns:
                    # Filtro: 1 = Sim, Desfecho 2 = Óbito
                    teve_comorb = (df_temp[c] == "1")
                    foi_obito = (df_temp["Desfecho_Caso"] == "2")
                    
                    total_casos[c] += teve_comorb.sum()
                    total_obitos[c] += (teve_comorb & foi_obito).sum()
            
            print(f"✔ {os.path.basename(arq)} processado.")

        except Exception as e:
            print(f"❌ Erro no arquivo {os.path.basename(arq)}: {e}")

    # Consolidação dos dados
    dados_finais = []
    for c in COMORBIDADES:
        casos = total_casos[c]
        obitos = total_obitos[c]
        taxa = (obitos / casos * 100) if casos > 0 else 0
        dados_finais.append({
            'Comorbidade': c.replace('Comorb_', ''),
            'Casos': casos,
            'Obitos': obitos,
            'Letalidade_%': round(taxa, 2)
        })

    df_resumo = pd.DataFrame(dados_finais).sort_values('Letalidade_%', ascending=False)

    # Exibição da Tabela
    print(f"\n{'-'*85}")
    print(f"{'TABELA: RESUMO DE LETALIDADE POR COMORBIDADE':^85}")
    print(f"{'-'*85}")
    print(df_resumo.to_string(index=False))
    
    # Exibição do Gráfico
    exibir_grafico_ascii_comorbidades(df_resumo)

    return df_resumo

if __name__ == '__main__':
    analisar_letalidade_comorbidades('dados')