import pandas as pd
import glob
import os
import re

def exibir_resultados(df_resumo):
    """Exibe a tabela e o gráfico ASCII no terminal."""
    if df_resumo is None or df_resumo.empty:
        print("\n⚠ Nenhum dado encontrado para exibir.")
        return

    print(f"\n{'-'*75}")
    print(f"{'TABELA: ÓBITOS POR ANO E SOROTIPO':^75}")
    print(f"{'-'*75}")
    
    # Matriz Ano x Sorotipo
    try:
        pivot = df_resumo.pivot(index='Ano', columns='Sorotipo', values='Obitos').fillna(0).astype(int)
        print(pivot)
    except Exception as e:
        print(df_resumo)

    print(f"\n{'='*75}")
    print(f"{'📊 GRÁFICO: EVOLUÇÃO ANUAL DE ÓBITOS':^75}")
    print(f"{'='*75}\n")

    # Gráfico ASCII
    df_ano = df_resumo.groupby('Ano')['Obitos'].sum().reset_index()
    max_val = df_ano['Obitos'].max()
    for _, row in df_ano.iterrows():
        barra = '█' * int((row['Obitos'] / max_val) * 40) if max_val > 0 else ''
        print(f"  Ano {row['Ano']}: {barra:<40} {int(row['Obitos']):>4} óbitos")
    print(f"\n{'='*75}\n")

def executar_analise_anual(pasta_dados):
    """Lê os arquivos Parquet e consolida os óbitos."""
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    if not arquivos:
        print(f"⚠ Pasta '{pasta_dados}' vazia.")
        return None

    lista_final = []
    print(f"⏳ Analisando {len(arquivos)} arquivos...")

    for arq in arquivos:
        try:
            # Extrair ano do nome do arquivo
            ano = re.search(r'(\d{4})', os.path.basename(arq))
            ano = ano.group(1) if ano else "S/A"

            # Carregar dados
            df = pd.read_parquet(arq, columns=["SOROTIPO", "Desfecho_Caso"]).copy()
            
            # Converter para string para evitar erro Categorical
            for col in df.columns:
                df[col] = df[col].astype(str).str.replace(".0", "", regex=False).str.strip()

            # Filtrar óbitos (Desfecho 2)
            df_obitos = df[(df["Desfecho_Caso"] == "2") & (df["SOROTIPO"] != "nan")]
            
            if not df_obitos.empty:
                resumo = df_obitos.groupby("SOROTIPO").size().reset_index(name="Obitos")
                resumo["Ano"] = ano
                lista_final.append(resumo)
        except Exception as e:
            print(f"❌ Erro em {os.path.basename(arq)}: {e}")

    if not lista_final:
        return None

    df_consolidado = pd.concat(lista_final, ignore_index=True)
    df_consolidado.columns = ['Sorotipo', 'Obitos', 'Ano']
    
    # Chamar exibição
    exibir_resultados(df_consolidado)
    return df_consolidado