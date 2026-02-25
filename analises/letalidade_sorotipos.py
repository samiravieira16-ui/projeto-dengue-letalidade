
import pandas as pd
import glob
import os

def _mostrar_tabela_terminal(df):
    try:
        from tabulate import tabulate
        print(tabulate(df, headers='keys', tablefmt='github', showindex=False))
    except Exception:
        print(df.to_string(index=False))


def _mostrar_grafico_ascii(df, titulo='Letalidade por Sorotipo'):
    try:
        import plotext as plt
    except Exception:
        print('\n⚠ Aviso: pacote plotext não instalado. Para gráfico ASCII instale: pip install plotext')
        return

    x = df['sorotipo'].astype(str).tolist()
    y = df['letalidade_%'].tolist()
    plt.clear_figure()
    plt.title(titulo)
    plt.xlabel('Sorotipo')
    plt.ylabel('Letalidade (%)')
    plt.bar(x, y)
    plt.plotsize(100, 20)
    plt.show()


def calcular_letalidade_conservadora(pasta_dados):
    """
    Calcula a letalidade excluindo casos com desfecho ignorado ou nulo.
    Considera apenas: 1 (Cura) e 2 (Óbito pelo agravo).
    """
    import os
    import glob
    import pandas as pd


    def _display_terminal(df, title='Letalidade por Sorotipo'):
        # Normaliza coluna `sorotipo` se necessário
        df2 = df.copy()
        if 'sorotipo' not in df2.columns:
            df2 = df2.reset_index().rename(columns={df2.index.name or 'index': 'sorotipo'})

        # Garantir string e remover entradas vazias/zero
        df2['sorotipo'] = df2['sorotipo'].astype(str).str.strip()
        df2 = df2[~df2['sorotipo'].isin(['0', ''])].copy()

        # Calcular letalidade se faltar
        if 'letalidade_%' not in df2.columns:
            if {'total_casos_conhecidos', 'obitos_confirmados'}.issubset(df2.columns):
                df2['letalidade_%'] = (
                    df2['obitos_confirmados'].astype(float) / df2['total_casos_conhecidos'].astype(float)
                ) * 100
            else:
                # tenta calcular a partir de colunas brutas
                if {'SOROTIPO', 'Desfecho_Caso'}.issubset(df.columns):
                    casos = df[df['Desfecho_Caso'].astype(str).str.replace('.0','',regex=False).isin(['1','2'])].groupby('SOROTIPO').size()
                    obitos = df[df['Desfecho_Caso'].astype(str).str.replace('.0','',regex=False) == '2'].groupby('SOROTIPO').size()
                    tmp = pd.DataFrame({'total_casos_conhecidos': casos, 'obitos_confirmados': obitos}).fillna(0).astype(int)
                    tmp['letalidade_%'] = (tmp['obitos_confirmados'] / tmp['total_casos_conhecidos']) * 100
                    tmp = tmp.reset_index().rename(columns={'index': 'sorotipo'})
                    df2 = tmp

        # Exibir tabela (usar tabulate se disponível)
        try:
            from tabulate import tabulate
            print(tabulate(df2, headers='keys', tablefmt='github', showindex=False))
        except Exception:
            print(df2.to_string(index=False))

        # Gráfico ASCII com plotext (se disponível)
        try:
            import plotext as plt
            x = df2['sorotipo'].astype(str).tolist()
            y = df2['letalidade_%'].astype(float).tolist()
            plt.clear_figure()
            plt.title(title)
            plt.xlabel('Sorotipo')
            plt.ylabel('Letalidade (%)')
            plt.bar(x, y)
            plt.plotsize(100, 20)
            plt.show()
        except Exception:
            print('\n⚠ plotext não instalado. Para ver gráfico ASCII: pip install plotext')


    def calcular_letalidade_conservadora(pasta_dados):
        """Processa arquivos .parquet em `pasta_dados` e retorna DataFrame com
        colunas: sorotipo, total_casos_conhecidos, obitos_confirmados, letalidade_%.
        """
        arquivos = glob.glob(os.path.join(pasta_dados, '*.parquet'))
        if not arquivos:
            print(f'Erro: nenhum arquivo .parquet em {pasta_dados}')
            return None

        total_casos = pd.Series(dtype='int')
        total_obitos = pd.Series(dtype='int')
        bruto = 0

        for f in arquivos:
            df = pd.read_parquet(f, columns=['SOROTIPO', 'Desfecho_Caso'])
            bruto += len(df)
            df = df.dropna(subset=['SOROTIPO'])
            df['Desfecho_Caso'] = df['Desfecho_Caso'].astype(str).str.replace('.0', '', regex=False).str.strip()
            validos = df[df['Desfecho_Caso'].isin(['1', '2'])]
            casos = validos.groupby('SOROTIPO').size()
            obitos = validos[validos['Desfecho_Caso'] == '2'].groupby('SOROTIPO').size()
            total_casos = total_casos.add(casos, fill_value=0)
            total_obitos = total_obitos.add(obitos, fill_value=0)

        resultado = pd.DataFrame({
            'total_casos_conhecidos': total_casos.fillna(0).astype(int),
            'obitos_confirmados': total_obitos.fillna(0).astype(int)
        })
        resultado['letalidade_%'] = (resultado['obitos_confirmados'] / resultado['total_casos_conhecidos']) * 100
        resultado = resultado.sort_index().reset_index().rename(columns={'index': 'sorotipo'})

        print(f"Processados {len(arquivos)} arquivos — registros brutos: {bruto}")
        return resultado


    def visualizar_letalidade_terminal(path_resultados_dir='resultados'):
        """Lê arquivos em `resultados/` (prioriza parquet) e exibe tabela + gráfico.
        Se não encontrar um arquivo pronto, tenta calcular a partir de `dados`.
        """
        p_parquet = os.path.join(path_resultados_dir, 'letalidade_sorotipos.parquet')
        p_csv = os.path.join(path_resultados_dir, 'letalidade_sorotipos.csv')

        if os.path.exists(p_parquet):
            df = pd.read_parquet(p_parquet)
        elif os.path.exists(p_csv):
            df = pd.read_csv(p_csv)
        else:
            # tenta calcular a partir da pasta `dados`
            df = calcular_letalidade_conservadora('dados')
            if df is None:
                print('Nenhum resultado disponível e não foi possível calcular a partir de dados.')
                return None

        print('\n== Tabela de Letalidade por Sorotipo ==\n')
        _display_terminal(df)
        return df


    if __name__ == '__main__':
        visualizar_letalidade_terminal()
    df_letalidade = calcular_letalidade_conservadora(caminho_dados)
