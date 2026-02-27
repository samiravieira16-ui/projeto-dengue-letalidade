import pandas as pd
import glob
import os

def exibir_tabela_letalidade(df_letalidade):
    """Exibe a tabela de estatísticas de letalidade no console."""
    print(f"\n{'-'*75}")
    print(f"{'TABELA: LETALIDADE (%) POR SOROTIPO':^75}")
    print(f"{'-'*75}")
    # Formatação para alinhar colunas
    print(df_letalidade.to_string(index=False))
    print(f"{'-'*75}\n")

def exibir_grafico_ascii(df):
    """Exibe gráfico ASCII de letalidade por sorotipo."""
    if df is None or df.empty:
        return
    
    # Ordenar pela letalidade para o gráfico
    df_plot = df.sort_values('Letalidade_%', ascending=True)
    max_val = df_plot['Letalidade_%'].max()
    max_width = 45

    print(f"\n{'='*75}")
    print(f"{'📊 GRÁFICO: LETALIDADE (%) POR SOROTIPO':^75}")
    print(f"{'='*75}\n")

    for _, row in df_plot.iterrows():
        # Tratamento para garantir que sorotipo seja exibido sem .0
        soro = str(row['Sorotipo']).replace('.0', '')
        letal = row['Letalidade_%']
        obitos = int(row['Obitos'])
        casos = int(row['Casos'])
        
        size = int((letal / max_val) * max_width) if max_val > 0 else 0
        barra = '█' * size
        print(f"  Sorotipo {soro:<3} {barra:<45} {letal:6.2f}%")

    print(f"\n{'='*75}\n")

def calcular_letalidade(pasta_dados='dados'):
    """Calcula a letalidade consolidada por sorotipo de todos os arquivos."""
    arquivos = glob.glob(os.path.join(pasta_dados, '*.parquet'))
    if not arquivos:
        print(f'⚠ Nenhum arquivo .parquet encontrado em: {pasta_dados}')
        return None

    total_casos = pd.Series(dtype='int')
    total_obitos = pd.Series(dtype='int')

    print(f"⏳ Analisando letalidade por sorotipo em {len(arquivos)} arquivos...")

    for arq in arquivos:
        try:
            # Carrega apenas colunas necessárias e força tipo String para evitar erro Categorical
            df = pd.read_parquet(arq, columns=['SOROTIPO', 'Desfecho_Caso']).copy()
            df['SOROTIPO'] = df['SOROTIPO'].astype(str).str.replace('.0', '', regex=False).str.strip()
            df['Desfecho_Caso'] = df['Desfecho_Caso'].astype(str).str.replace('.0', '', regex=False).str.strip()
            
            # Remove nulos ou ignorados
            df = df[df['SOROTIPO'] != 'nan']
            
            # Filtra apenas casos com desfecho válido para cálculo de letalidade (1=Cura, 2=Óbito)
            validos = df[df['Desfecho_Caso'].isin(['1', '2'])]
            
            # Soma ao total acumulado
            total_casos = total_casos.add(validos.groupby('SOROTIPO').size(), fill_value=0)
            total_obitos = total_obitos.add(
                validos[validos['Desfecho_Caso'] == '2'].groupby('SOROTIPO').size(), fill_value=0
            )
            print(f"✔ {os.path.basename(arq)} processado")
        
        except Exception as e:
            print(f"❌ Erro ao processar {os.path.basename(arq)}: {e}")

    # Montagem do DataFrame Final
    resultado = pd.DataFrame({
        'Sorotipo': total_casos.index,
        'Casos': total_casos.values.astype(int),
        'Obitos': total_obitos.values.astype(int),
    })
    
    # Previne divisão por zero
    resultado['Letalidade_%'] = (resultado['Obitos'] / resultado['Casos'] * 100).round(2)
    resultado = resultado.sort_values('Sorotipo').reset_index(drop=True)

    # Chamada das funções de exibição seguindo seu padrão
    exibir_tabela_letalidade(resultado)
    exibir_grafico_ascii(resultado)
    
    return resultado

if __name__ == '__main__':
    calcular_letalidade('dados')