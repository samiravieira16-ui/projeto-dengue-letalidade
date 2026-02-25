import pandas as pd
import glob
import os


def calcular_letalidade(pasta_dados='dados'):
    arquivos = glob.glob(os.path.join(pasta_dados, '*.parquet'))
    if not arquivos:
        print(f'Nenhum .parquet em {pasta_dados}')
        return None

    total_casos = pd.Series(dtype='int')
    total_obitos = pd.Series(dtype='int')

    for arquivo in arquivos:
        df = pd.read_parquet(arquivo, columns=['SOROTIPO', 'Desfecho_Caso'])
        df = df.dropna(subset=['SOROTIPO'])
        df['Desfecho_Caso'] = df['Desfecho_Caso'].astype(str).str.replace('.0', '', regex=False)
        validos = df[df['Desfecho_Caso'].isin(['1', '2'])]
        total_casos = total_casos.add(validos.groupby('SOROTIPO').size(), fill_value=0)
        total_obitos = total_obitos.add(
            validos[validos['Desfecho_Caso'] == '2'].groupby('SOROTIPO').size(), fill_value=0
        )

    resultado = pd.DataFrame({
        'sorotipo': total_casos.index,
        'casos': total_casos.values,
        'obitos': total_obitos.values,
    })
    resultado['letalidade_%'] = (resultado['obitos'] / resultado['casos'] * 100).round(2)
    return resultado.sort_values('sorotipo').reset_index(drop=True)


def exibir_grafico_ascii(df):
    """Exibe gráfico ASCII de letalidade por sorotipo."""
    if df is None or df.empty:
        return
    
    df_plot = df.sort_values('letalidade_%', ascending=True)
    max_val = df_plot['letalidade_%'].max()
    max_width = 50

    print(f"\n{'='*70}")
    print(f"{'📊 GRÁFICO: LETALIDADE (%) POR SOROTIPO':^70}")
    print(f"{'='*70}\n")

    for _, row in df_plot.iterrows():
        sorotipo = str(int(row['sorotipo']))
        letal = row['letalidade_%']
        obitos = int(row['obitos'])
        casos = int(row['casos'])
        size = int((letal / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        print(f"  Sorotipo {sorotipo:<2} {barra:<50} {letal:5.2f}% ({obitos}/{casos})")

    print(f"\n{'='*70}\n")


if __name__ == '__main__':
    df = calcular_letalidade('dados')
    

