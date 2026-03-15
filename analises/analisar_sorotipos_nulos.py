import pandas as pd
import glob
import os
import re

def analisar_sorotipos_nulos(pasta_dados):
    """
    Analisa a proporção de sorotipos nulos (não identificados) 
    especificamente para os casos que evoluíram para óbito.
    """
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    if not arquivos:
        print(f"⚠ Nenhum arquivo .parquet encontrado em: {pasta_dados}")
        return None

    lista_resultados = []

    for arq in sorted(arquivos):
        try:
            # Extrair ano do nome do arquivo
            match_ano = re.search(r'(\d{4})', os.path.basename(arq))
            ano = match_ano.group(1) if match_ano else "S/A"

            # Carregar apenas colunas necessárias
            df = pd.read_parquet(arq, columns=["SOROTIPO", "Desfecho_Caso"]).copy()

            # Normalização básica (converter para string para tratar nans de forma consistente)
            df["SOROTIPO"] = df["SOROTIPO"].astype(str).str.replace(".0", "", regex=False).str.strip().str.lower()
            df["Desfecho_Caso"] = df["Desfecho_Caso"].astype(str).str.replace(".0", "", regex=False).str.strip()

            # Filtrar apenas óbitos (Desfecho_Caso == 2)
            df_obitos = df[df["Desfecho_Caso"] == "2"].copy()
            
            total_obitos = len(df_obitos)
            if total_obitos == 0:
                continue

            # Identificar nulos (no parquet limpo, nulos vêm como 'nan' após conversão para string)
            # Mas vamos checar também se há sorotipos válidos (1, 2, 3, 4)
            sorotipos_validos = ["1", "2", "3", "4"]
            
            obitos_sem_sorotipo = len(df_obitos[~df_obitos["SOROTIPO"].isin(sorotipos_validos)])
            obitos_com_sorotipo = total_obitos - obitos_sem_sorotipo
            
            pct_nulo = (obitos_sem_sorotipo / total_obitos * 100) if total_obitos > 0 else 0

            lista_resultados.append({
                "Ano": ano,
                "Total_Obitos": total_obitos,
                "Com_Sorotipo": obitos_com_sorotipo,
                "Sem_Sorotipo": obitos_sem_sorotipo,
                "Pct_Nulo": pct_nulo
            })

        except Exception as e:
            print(f"  ❌ Erro ao analisar nulos em {os.path.basename(arq)}: {e}")

    if not lista_resultados:
        return None

    return pd.DataFrame(lista_resultados)

def exibir_tabela_nulos(df_nulos):
    """Exibe os resultados da análise de nulos no console."""
    if df_nulos is None or df_nulos.empty:
        print("⚠ Sem dados para exibir a tabela de sorotipos nulos.")
        return

    print(f"\n{'-'*85}")
    print(f"{'TABELA: ANÁLISE DE SOROTIPOS NÃO IDENTIFICADOS EM ÓBITOS':^85}")
    print(f"{'-'*85}")
    print(f"  {'Ano':<6} | {'Total Óbitos':>12} | {'Com Sorotipo':>12} | {'Sem Sorotipo':>12} | {'% Nulo':>10}")
    print(f"  {'-'*81}")
    
    for _, row in df_nulos.iterrows():
        print(f"  {row['Ano']:<6} | {int(row['Total_Obitos']):>12} | {int(row['Com_Sorotipo']):>12} | {int(row['Sem_Sorotipo']):>12} | {row['Pct_Nulo']:>9.1f}%")
    
    print(f"  {'-'*81}")
    
    total_geral = df_nulos['Total_Obitos'].sum()
    sem_soro_geral = df_nulos['Sem_Sorotipo'].sum()
    pct_geral = (sem_soro_geral / total_geral * 100) if total_geral > 0 else 0
    
    print(f"  {'TOTAL':<6} | {int(total_geral):>12} | {int(df_nulos['Com_Sorotipo'].sum()):>12} | {int(sem_soro_geral):>12} | {pct_geral:>9.1f}%")
    print(f"{'-'*85}\n")

def exibir_grafico_ascii_nulos(df_nulos):
    """Exibe um gráfico ASCII comparativo."""
    if df_nulos is None or df_nulos.empty:
        return

    print(f"\n{'='*85}")
    print(f"{'📊 GRÁFICO: PROPORÇÃO DE ÓBITOS SEM SOROTIPO IDENTIFICADO':^85}")
    print(f"{'='*85}\n")

    max_width = 40
    for _, row in df_nulos.iterrows():
        pct = row['Pct_Nulo']
        size_nulo = int((pct / 100) * max_width)
        size_identificado = max_width - size_nulo
        
        barra = '▒' * size_identificado + '█' * size_nulo
        print(f"  {row['Ano']}  [{barra}] {pct:>5.1f}% (Nulos)")

    print(f"\n  Legenda: [▒] Identificado  [█] Não Identificado (NULL)")
    print(f"{'='*85}\n")

if __name__ == "__main__":
    df = analisar_sorotipos_nulos('dados')
    exibir_tabela_nulos(df)
    exibir_grafico_ascii_nulos(df)
