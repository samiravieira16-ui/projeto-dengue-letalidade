import pandas as pd 
import glob 
import os 

def analisar_dinamica_temporal(pasta_dados, 
pasta_saida="resultados"): 
    """ 
    Calcula o tempo (em dias) do início dos sintomas até o óbito. 
    ESTRITAMENTE para Desfecho_Caso == 2 (Óbito pelo agravo). 
    """ 
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet")) 
      
    if not os.path.exists(pasta_saida): 
        os.makedirs(pasta_saida) 
  
    lista_tempos = [] 
  
    print(f"⏳ Analisando dinâmica temporal (Apenas Desfecho 2) em 
{len(arquivos)} arquivos...") 
  
     for arquivo in arquivos: 
         # Carregar colunas necessárias 
         df = pd.read_parquet(arquivo, columns=[ 
             "Data_Inicio_Sintomas",  
             "Data_Obito",  
             "SOROTIPO",  
             "Desfecho_Caso" 
         ]) 
          
         # 1. Padronização e Filtro Estrito do Desfecho 2 
         # Converte para string e limpa formatos como '2.0' ou '2 ' 
         df["Desfecho_Caso"] = 
df["Desfecho_Caso"].astype(str).str.replace(".0", "", 
regex=False).str.strip() 
          
         # FILTRO CRUCIAL: Considera apenas óbitos confirmados pelo 
agravo 
         df_obitos = df[df["Desfecho_Caso"] == "2"].copy() 
  
         # 2. Remover registros com datas faltantes (null) ou sem 
sorotipo 
         df_obitos = df_obitos.dropna(subset=["Data_Obito", 
"Data_Inicio_Sintomas", "SOROTIPO"]) 
  
        if not df_obitos.empty: 
            # 3. Converter Timestamps (ms) para Datetime real 
            df_obitos["Data_Inicio_Sintomas"] = 
pd.to_datetime(df_obitos["Data_Inicio_Sintomas"], unit='ms') 
            df_obitos["Data_Obito"] = 
pd.to_datetime(df_obitos["Data_Obito"], unit='ms') 
  
             # 4. Calcular a diferença em dias 
             df_obitos["Dias_Ate_Obito"] = (df_obitos["Data_Obito"] - 
df_obitos["Data_Inicio_Sintomas"]).dt.days 
  
             # 5. Filtro de consistência: Óbito deve ser igual ou 
posterior aos sintomas 
            df_obitos = df_obitos[df_obitos["Dias_Ate_Obito"] >= 0]   
            lista_tempos.append(df_obitos) 
          
        print(f"✔ {os.path.basename(arquivo)} processado.") 
  
    if not lista_tempos: 
        print("⚠ Nenhum óbito com desfecho '2' foi encontrado nos 
arquivos.") 
        return pd.DataFrame(), pd.DataFrame() 
  
    # Concatenar resultados de todos os anos 
    df_final = pd.concat(lista_tempos, ignore_index=True) 
  
    # --- Estatísticas Descritivas por Sorotipo --- 
    estatisticas = 
df_final.groupby("SOROTIPO")["Dias_Ate_Obito"].agg([ 
        'count', 'mean', 'median', 'std' 
    ]).round(2) 
  
    # Renomear colunas para o CSV final 
    estatisticas.columns = [ 
        'Total_Obitos_Confirmados',  
        'Media_Dias_Sintoma_ao_Obito',  
        'Mediana_Dias',  
        'Desvio_Padrao' 
    ] 
  
    # Salvar resultado 
    caminho_csv = os.path.join(pasta_saida, 
"dinamica_temporal_obitos_confirmados.csv") 
    estatisticas.to_csv(caminho_csv) 
      
    print("\n" + "="*45) 
    print("📊 ANÁLISE TEMPORAL FINALIZADA (DESFECHO 2)") 
    print(f"Total de óbitos processados: {len(df_final)}") 
    print(f"Arquivo salvo: {caminho_csv}") 
    print("="*45) 
    return estatisticas, df_final 
  
if __name__ == "__main__": 
    # Executa apontando para a pasta 'dados' na raiz do seu projeto 
    stats, _ = analisar_dinamica_temporal("dados") 
print(stats) 