import pandas as pd
import glob
import os


def exibir_grafico_temporal_ascii(df_estatisticas):
    """Exibe um gráfico de barras em ASCII com a média de dias até óbito por sorotipo."""
    df_plot = df_estatisticas.sort_values('Media_Dias_Sintoma_ao_Obito', ascending=True)
    max_val = df_plot['Media_Dias_Sintoma_ao_Obito'].max()
    max_width = 50

    print(f"\n{'='*75}")
    print(f"{'📊 GRÁFICO: MÉDIA DE DIAS ATÉ ÓBITO POR SOROTIPO':^75}")
    print(f"{'='*75}\n")

    for sorotipo, row in df_plot.iterrows():
        media = row['Media_Dias_Sintoma_ao_Obito']
        total = int(row['Total_Obitos_Confirmados'])
        size = int((media / max_val) * max_width) if max_val and max_val > 0 else 0
        barra = '█' * size
        print(f"  Sorotipo {sorotipo:<2} {barra:<50} {media:5.2f} dias")

    print(f"\n{'='*75}\n")


def exibir_tabela_temporal(df_estatisticas):
    """Exibe a tabela de estatísticas temporais no console."""
    print(f"\n{'-'*75}")
    print(f"{'TABELA: ANÁLISE TEMPORAL POR SOROTIPO':^75}")
    print(f"{'-'*75}")
    print(df_estatisticas.to_string())
    print(f"{'-'*75}\n")


def analisar_dinamica_temporal(pasta_dados):
    """Calcula e exibe estatísticas temporais (apenas no terminal).

    - Exibe tabela e gráfico ASCII no terminal.
    """
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    if not arquivos:
        print("⚠ Nenhum arquivo Parquet encontrado em:", pasta_dados)
        return pd.DataFrame()

    lista = []
    print(f"⏳ Analisando dinâmica temporal (Desfecho 2) em {len(arquivos)} arquivos...")
    for arq in arquivos:
        df = pd.read_parquet(arq, columns=["Data_Inicio_Sintomas", "Data_Obito", "SOROTIPO", "Desfecho_Caso"])
        df["Desfecho_Caso"] = df["Desfecho_Caso"].astype(str).str.replace('.0', '', regex=False).str.strip()
        df_obitos = df[df["Desfecho_Caso"] == '2'].dropna(subset=["Data_Inicio_Sintomas", "Data_Obito", "SOROTIPO"]).copy()
        if df_obitos.empty:
            print(f"✔ {os.path.basename(arq)} processado (0 óbitos relevantes)")
            continue
        df_obitos["Data_Inicio_Sintomas"] = pd.to_datetime(df_obitos["Data_Inicio_Sintomas"], unit='ms')
        df_obitos["Data_Obito"] = pd.to_datetime(df_obitos["Data_Obito"], unit='ms')
        df_obitos["Dias_Ate_Obito"] = (df_obitos["Data_Obito"] - df_obitos["Data_Inicio_Sintomas"]).dt.days
        df_obitos = df_obitos[df_obitos["Dias_Ate_Obito"] >= 0]
        lista.append(df_obitos)
        print(f"✔ {os.path.basename(arq)} processado ({len(df_obitos)} óbitos)")

    if not lista:
        print("⚠ Nenhum óbito com desfecho '2' foi encontrado nos arquivos.")
        return pd.DataFrame()

    df_final = pd.concat(lista, ignore_index=True)
    stats = df_final.groupby('SOROTIPO')["Dias_Ate_Obito"].agg(['count', 'mean', 'median', 'std']).round(2)
    stats.columns = ['Total_Obitos_Confirmados', 'Media_Dias_Sintoma_ao_Obito', 'Mediana_Dias', 'Desvio_Padrao']

    # Exibir tabela e gráfico no terminal (sem salvar arquivos)
    exibir_tabela_temporal(stats)
    exibir_grafico_temporal_ascii(stats)

    print("✅ Análise temporal concluída (visualização exibida no terminal).")
    return stats


if __name__ == '__main__':
    analisar_dinamica_temporal('dados')
