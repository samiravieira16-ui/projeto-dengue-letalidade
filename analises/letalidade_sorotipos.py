
import pandas as pd
import glob
import os

def calcular_letalidade_conservadora(pasta_dados):
    """
    Calcula a letalidade excluindo casos com desfecho ignorado ou nulo.
    Considera apenas: 1 (Cura) e 2 (Óbito pelo agravo).
    """
    # Busca todos os arquivos .parquet na sua pasta de dados
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet"))
    
    if not arquivos:
        print(f"Erro: Nenhum arquivo .parquet encontrado em {pasta_dados}")
        return None

    total_casos_validos = pd.Series(dtype=int)
    total_obitos_confirmados = pd.Series(dtype=int)
    total_registros_brutos = 0

    print(f"🔍 Iniciando processamento de {len(arquivos)} arquivos em '{pasta_dados}'...")

    for arquivo in arquivos:
        # Carregar colunas necessárias (Ajuste os nomes se houver diferença de maiúsculas/minúsculas)
        df = pd.read_parquet(arquivo, columns=["SOROTIPO", "Desfecho_Caso"])
        total_registros_brutos += len(df)
        
        # 1. Limpeza: Remove linhas onde o Sorotipo é nulo
        df = df.dropna(subset=["SOROTIPO"])
        
        # 2. Padronização do Desfecho: Trata números, strings e floats (2.0 -> "2")
        df["Desfecho_Caso"] = (
            df["Desfecho_Caso"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

        # 3. Abordagem Conservadora: Filtra apenas Cura (1) ou Óbito (2)
        # Ignora automaticamente 3, 4, 9 e nulos
        df_validos = df[df["Desfecho_Caso"].isin(["1", "2"])].copy()

        # 4. Agrupamento e soma
        casos = df_validos.groupby("SOROTIPO").size()
        obitos = df_validos[df_validos["Desfecho_Caso"] == "2"].groupby("SOROTIPO").size()

        # Acumula os resultados
        total_casos_validos = total_casos_validos.add(casos, fill_value=0)
        total_obitos_confirmados = total_obitos_confirmados.add(obitos, fill_value=0)

        print(f"✅ Concluído: {os.path.basename(arquivo)}")

    # --- Consolidação Final ---
    resultado = pd.DataFrame({
        "total_casos_conhecidos": total_casos_validos,
        "obitos_confirmados": total_obitos_confirmados
    }).fillna(0)

    resultado = resultado.astype(int)

    # Cálculo da Letalidade %
    resultado["letalidade_%"] = (
        resultado["obitos_confirmados"] / resultado["total_casos_conhecidos"]
    ) * 100

    resultado = resultado.sort_index().reset_index()
    resultado.rename(columns={'index': 'sorotipo'}, inplace=True)

    print("\n" + "="*40)
    print("📊 RESULTADO FINAL")
    print(f"Total bruto de registros: {total_registros_brutos}")
    print(f"Total analisado (com desfecho 1 ou 2): {resultado['total_casos_conhecidos'].sum()}")
    print("="*40)

    return resultado

# --- Execução Principal ---
if __name__ == "__main__":
    # Caminho relativo baseado na sua imagem
    caminho_dados = "dados" 
    
    df_letalidade = calcular_letalidade_conservadora(caminho_dados)
    
    if df_letalidade is not None:
        print(df_letalidade)
        