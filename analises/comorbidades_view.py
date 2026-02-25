import pandas as pd
import glob
import os


COMORBIDADES = [
    "Comorb_Diabetes", "Comorb_Hematolog", "Comorb_Hepatopat",
    "Comorb_Renal", "Comorb_Hipertensao", "Comorb_AcidoPeptica",
    "Comorb_AutoImune"
]


def calcular_letaldade_comorbidades(pasta_dados='dados'):
    """Calcula letalidade por comorbidade."""
    arquivos = glob.glob(os.path.join(pasta_dados, '*.parquet'))
    if not arquivos:
        print(f'Nenhum .parquet em {pasta_dados}')
        return None

    total_casos = {c: 0 for c in COMORBIDADES}
    total_obitos = {c: 0 for c in COMORBIDADES}

    for arquivo in arquivos:
        df = pd.read_parquet(arquivo, columns=COMORBIDADES + ["Desfecho_Caso"])
        df["Desfecho_Caso"] = df["Desfecho_Caso"].astype(str).str.replace(".0", "", regex=False).str.strip()

        for c in COMORBIDADES:
            df[c] = df[c].astype(str).str.replace(".0", "", regex=False).str.strip()
            n_casos = (df[c] == "1").sum()
            n_obitos = ((df[c] == "1") & (df["Desfecho_Caso"] == "2")).sum()
            total_casos[c] += n_casos
            total_obitos[c] += n_obitos

    resultado = pd.DataFrame({
        'comorbidade': [c.replace('Comorb_', '') for c in COMORBIDADES],
        'casos': [total_casos[c] for c in COMORBIDADES],
        'obitos': [total_obitos[c] for c in COMORBIDADES],
    })
    resultado['letalidade_%'] = (resultado['obitos'] / resultado['casos'] * 100).round(2)
    return resultado.sort_values('letalidade_%', ascending=False).reset_index(drop=True)


def exibir_grafico_ascii(df):
    """Exibe gráfico ASCII de letalidade por comorbidade."""
    if df is None or df.empty:
        return

    max_val = df['letalidade_%'].max()
    max_width = 50

    print(f"\n{'='*70}")
    print(f"{'📊 GRÁFICO: LETALIDADE (%) POR COMORBIDADE':^70}")
    print(f"{'='*70}\n")

    for _, row in df.iterrows():
        comorb = row['comorbidade']
        letal = row['letalidade_%']
        obitos = int(row['obitos'])
        casos = int(row['casos'])
        size = int((letal / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        print(f"  {comorb:20} {barra:<50} {letal:5.2f}% ({obitos}/{casos})")

    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    df = calcular_letaldade_comorbidades('dados')
    if df is not None:
        print(df.to_string(index=False))
        exibir_grafico_ascii(df)
