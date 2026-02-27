import pandas as pd
import glob
import os
import re


def exibir_tabela_obitos_ano(df_ano):
    """Exibe a tabela de óbitos por ano no console."""
    print(f"\n{'-'*75}")
    print(f"{'TABELA: TOTAL DE ÓBITOS POR ANO':^75}")
    print(f"{'-'*75}")
    print(f"  {'Ano':<10} {'Óbitos':>10}")
    print(f"  {'-'*20}")
    for _, row in df_ano.iterrows():
        print(f"  {row['Ano']:<10} {int(row['Obitos']):>10}")
    print(f"  {'-'*20}")
    print(f"  {'TOTAL':<10} {int(df_ano['Obitos'].sum()):>10}")
    print(f"{'-'*75}\n")


def exibir_grafico_ascii_obitos(df_ano):
    """Exibe gráfico ASCII de óbitos por ano."""
    if df_ano is None or df_ano.empty:
        return

    max_val = df_ano['Obitos'].max()
    max_width = 40

    print(f"\n{'='*75}")
    print(f"{'📊 GRÁFICO: EVOLUÇÃO ANUAL DE ÓBITOS':^75}")
    print(f"{'='*75}\n")

    for _, row in df_ano.iterrows():
        obitos = int(row['Obitos'])
        size = int((obitos / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        print(f"  {row['Ano']}  {barra:<40} {obitos:>5} óbitos")

    print(f"\n{'='*75}\n")


def exibir_tabela_sorotipo(df_resumo):
    """Exibe a matriz Ano x Sorotipo no console."""
    if df_resumo is None or df_resumo.empty:
        return

    print(f"\n{'-'*75}")
    print(f"{'TABELA: ÓBITOS POR ANO E SOROTIPO':^75}")
    print(f"{'-'*75}")

    try:
        pivot = df_resumo.pivot_table(
            index='Ano', columns='Sorotipo', values='Obitos',
            aggfunc='sum', fill_value=0
        ).astype(int)
        print(pivot)
    except Exception:
        print(df_resumo.to_string(index=False))

    print(f"{'-'*75}\n")


def executar_analise_anual(pasta_dados):
    """Lê os arquivos Parquet e consolida os óbitos por ano e sorotipo."""
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    if not arquivos:
        print(f"⚠ Nenhum arquivo .parquet encontrado em: {pasta_dados}")
        return None

    lista_final = []
    print(f"⏳ Analisando {len(arquivos)} arquivos...\n")

    for arq in sorted(arquivos):
        try:
            # Extrair ano do nome do arquivo
            match_ano = re.search(r'(\d{4})', os.path.basename(arq))
            ano = match_ano.group(1) if match_ano else "S/A"

            # Carregar apenas colunas necessárias
            df = pd.read_parquet(arq, columns=["SOROTIPO", "Desfecho_Caso"]).copy()

            # Converter para string para evitar erro Categorical
            df["SOROTIPO"] = df["SOROTIPO"].astype(str).str.replace(".0", "", regex=False).str.strip()
            df["Desfecho_Caso"] = df["Desfecho_Caso"].astype(str).str.replace(".0", "", regex=False).str.strip()

            # Filtrar óbitos (Desfecho_Caso == 2)
            df_obitos = df[df["Desfecho_Caso"] == "2"]

            # Separar com e sem sorotipo
            df_obitos_soro = df_obitos[df_obitos["SOROTIPO"] != "nan"]

            total_obitos = len(df_obitos)
            obitos_com_soro = len(df_obitos_soro)

            print(f"  ✔ {os.path.basename(arq):<30} → {total_obitos:>5} óbitos ({obitos_com_soro} com sorotipo)")

            # Agrupar por sorotipo para a tabela detalhada
            if not df_obitos_soro.empty:
                resumo = df_obitos_soro.groupby("SOROTIPO").size().reset_index(name="Obitos")
                resumo["Ano"] = ano
                lista_final.append(resumo)

            # Guardar também o total (com e sem sorotipo) para o resumo geral
            lista_final.append(pd.DataFrame({
                "SOROTIPO": ["_TOTAL_"],
                "Obitos": [total_obitos],
                "Ano": [ano],
            }))

        except Exception as e:
            print(f"  ❌ Erro em {os.path.basename(arq)}: {e}")

    if not lista_final:
        print("\n⚠ Nenhum dado de óbitos encontrado.")
        return None

    df_consolidado = pd.concat(lista_final, ignore_index=True)
    df_consolidado.columns = ['Sorotipo', 'Obitos', 'Ano']

    # --- Exibição 1: Óbitos totais por ano ---
    df_totais = df_consolidado[df_consolidado['Sorotipo'] == '_TOTAL_']
    df_ano = df_totais.groupby('Ano')['Obitos'].sum().reset_index().sort_values('Ano')

    exibir_tabela_obitos_ano(df_ano)
    exibir_grafico_ascii_obitos(df_ano)

    # --- Exibição 2: Matriz Ano x Sorotipo (apenas com sorotipo informado) ---
    df_sorotipo = df_consolidado[df_consolidado['Sorotipo'] != '_TOTAL_']
    if not df_sorotipo.empty:
        exibir_tabela_sorotipo(df_sorotipo)

    return df_consolidado


if __name__ == '__main__':
    executar_analise_anual('dados')