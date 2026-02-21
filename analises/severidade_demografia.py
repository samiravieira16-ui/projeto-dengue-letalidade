import pandas as pd 
import glob 
import os 
def analisar_severidade_demografia_absoluta(pasta_dados, 
pasta_saida="resultados"): 
""" 
Analisa a distribuição absoluta (contagem) de óbitos por Sexo e Faixa 
Etária. 
Considera estritamente Desfecho_Caso == 2. 
""" 
arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet")) 
if not os.path.exists(pasta_saida): 
        os.makedirs(pasta_saida) 
 
    lista_obitos = [] 
 
    for arquivo in arquivos: 
        df = pd.read_parquet(arquivo, columns=["Idade_Em_Anos", "Sexo", 
"Desfecho_Caso"]) 
         
        # 1. Filtro estrito: Apenas óbito pelo agravo (2) 
        df["Desfecho_Caso"] = 
df["Desfecho_Caso"].astype(str).str.replace(".0", "", 
regex=False).str.strip() 
        df_obitos = df[df["Desfecho_Caso"] == "2"].copy() 
 
        # 2. Limpeza de nulos 
        df_obitos = df_obitos.dropna(subset=["Idade_Em_Anos", "Sexo"]) 
         
        if not df_obitos.empty: 
            lista_obitos.append(df_obitos) 
 
    if not lista_obitos: 
        print("⚠ Nenhum óbito (Desfecho 2) encontrado.") 
        return None 
 
    # Concatenar todos os dados 
    df_final = pd.concat(lista_obitos, ignore_index=True) 
 
    # 3. Definição das Faixas Etárias (Distribuição Absoluta) 
    bins = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 120] 
    labels = ['0-4', '5-9', '10-14', '15-19', '20-29', '30-39', '40-49', 
'50-59', '60-69', '70-79', '80+'] 
    df_final['Faixa_Etaria'] = pd.cut(df_final['Idade_Em_Anos'], 
bins=bins, labels=labels, right=False) 
 
    # 4. Cruzamento Absoluto: Sexo vs Faixa Etária 
    # Usamos observed=False para garantir que todas as faixas apareçam, 
mesmo se estiverem zeradas 
    distribuicao_absoluta = pd.crosstab(df_final['Faixa_Etaria'], 
df_final['Sexo'], margins=True, margins_name="Total_Geral") 
 
    # Salvar o resultado 
    caminho_csv = os.path.join(pasta_saida, 
"distribuicao_absoluta_obitos.csv") 
    distribuicao_absoluta.to_csv(caminho_csv) 
 
print("\n" + "="*45) 
print("📊 DISTRIBUIÇÃO ABSOLUTA CONCLUÍDA") 
print(f"Total de óbitos analisados: {len(df_final)}") 
print(f"Arquivo salvo em: {caminho_csv}") 
print("="*45) 
return distribuicao_absoluta 
if __name__ == "__main__": 
res = analisar_severidade_demografia_absoluta("dados") 
print(res) 