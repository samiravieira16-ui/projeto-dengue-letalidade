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

    df_plot = df.sort_values('Letalidade_%', ascending=True)
    max_val = df_plot['Letalidade_%'].max()
    max_width = 40

    print(f"\n{'='*75}")
    print(f"{'📊 GRÁFICO: LETALIDADE (%) POR COMORBIDADE':^75}")
    print(f"{'='*75}\n")

    for _, row in df_plot.iterrows():
        nome  = row['Comorbidade']
        letal = row['Letalidade_%']
        size  = int((letal / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        print(f"  {nome:<15} {barra:<40} {letal:6.2f}%")

    print(f"\n{'='*75}\n")


def analisar_letalidade_comorbidades(pasta_dados):
    """Calcula letalidade e exibe tabela e gráfico no terminal."""
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    if not arquivos:
        print(f"⚠ Erro: Pasta '{pasta_dados}' não encontrada.")
        return

    total_casos  = {c: 0 for c in COMORBIDADES}
    total_obitos = {c: 0 for c in COMORBIDADES}
    total_casos_sem  = 0
    total_obitos_sem = 0

    print(f"⏳ Processando {len(arquivos)} arquivos...")

    for arq in arquivos:
        try:
            df_temp = pd.read_parquet(arq, columns=COMORBIDADES + ["Desfecho_Caso"])
            for col in df_temp.columns:
                df_temp[col] = df_temp[col].astype(str).str.replace('.0', '', regex=False).str.strip()

            tem_alguma = pd.Series(False, index=df_temp.index)

            for c in COMORBIDADES:
                if c in df_temp.columns:
                    teve  = (df_temp[c] == "1")
                    obito = (df_temp["Desfecho_Caso"] == "2")
                    total_casos[c]  += teve.sum()
                    total_obitos[c] += (teve & obito).sum()
                    tem_alguma = tem_alguma | teve

            sem   = ~tem_alguma
            obito = (df_temp["Desfecho_Caso"] == "2")
            total_casos_sem  += sem.sum()
            total_obitos_sem += (sem & obito).sum()

            print(f"✔ {os.path.basename(arq)} processado.")

        except Exception as e:
            print(f"❌ Erro no arquivo {os.path.basename(arq)}: {e}")

    # Consolidação dos dados
    dados_finais = []
    for c in COMORBIDADES:
        casos  = total_casos[c]
        obitos = total_obitos[c]
        taxa   = (obitos / casos * 100) if casos > 0 else 0
        dados_finais.append({
            'Comorbidade': c.replace('Comorb_', ''),
            'Casos': casos,
            'Obitos': obitos,
            'Letalidade_%': round(taxa, 2)
        })

    taxa_sem = (total_obitos_sem / total_casos_sem * 100) if total_casos_sem > 0 else 0
    dados_finais.append({
        'Comorbidade': 'Nenhuma',
        'Casos': total_casos_sem,
        'Obitos': total_obitos_sem,
        'Letalidade_%': round(taxa_sem, 2)
    })

    df_resumo = pd.DataFrame(dados_finais).sort_values('Letalidade_%', ascending=False)

    # Exibição da Tabela
    print(f"\n{'-'*75}")
    print(f"{'TABELA: RESUMO DE LETALIDADE POR COMORBIDADE':^75}")
    print(f"{'-'*75}")
    print(df_resumo.to_string(index=False))
    print(f"{'-'*75}")
    print("* NOTA: A soma da coluna 'Obitos' excede o número total de")
    print("  pacientes fatais reais (10.477) porque um mesmo paciente pode possuir")
    print("  múltiplas comorbidades, sendo contabilizado em mais de uma categoria.")

    # Exibição do Gráfico
    exibir_grafico_ascii_comorbidades(df_resumo)

    return df_resumo


if __name__ == '__main__':
    analisar_letalidade_comorbidades('dados')