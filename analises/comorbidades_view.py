import pandas as pd 
import glob 
import os 
 
def analisar_letalidade_comorbidades(pasta_dados, 
pasta_saida="resultados"): 
    # Busca os arquivos na pasta 'dados' 
    arquivos = glob.glob(os.path.join(pasta_dados, "*.parquet")) 
     
    if not os.path.exists(pasta_saida): 
        os.makedirs(pasta_saida) 
 
    comorbidades = [ 
        "Comorb_Diabetes", "Comorb_Hematolog", "Comorb_Hepatopat",  
        "Comorb_Renal", "Comorb_Hipertensao", "Comorb_AcidoPeptica", 
"Comorb_AutoImune" 
    ] 
 
    # Dicionários para somar os valores de todos os arquivos 
    total_casos_comorb = {c: 0 for c in comorbidades} 
    total_obitos_comorb = {c: 0 for c in comorbidades} 
 
    print(f"\n{'='*65}") 
    print(f"📊 INICIANDO MAPEAMENTO DE COMORBIDADES") 
    print(f"{'='*65}") 
 
    for arquivo in arquivos: 
        print(f"📖 Lendo: {os.path.basename(arquivo)}") 
        # Lê apenas as colunas necessárias 
        df = pd.read_parquet(arquivo, columns=comorbidades + 
["Desfecho_Caso"]) 
         
        # Padroniza o desfecho para string e remove o ".0" 
        df["Desfecho_Caso"].astype(str).str.replace(".0", "", 
regex=False).str.strip() 
         
        for c in comorbidades: 
            # Padroniza a comorbidade (1 = Sim) 
            df[c] = df[c].astype(str).str.replace(".0", "", 
regex=False).str.strip() 
             
            # Contagem absoluta: quem tem a doença e quem morreu com ela 
            n_casos = (df[c] == "1").sum() 
            n_obitos = ((df[c] == "1") & (df["Desfecho_Caso"] == 
"2")).sum() 
             
            total_casos_comorb[c] += n_casos 
            total_obitos_comorb[c] += n_obitos 
 
    # Criando a tabela final 
    res = pd.DataFrame({ 
        "Comorbidade": comorbidades, 
        "Total_Casos_com_Comorbidade": [total_casos_comorb[c] for c in 
comorbidades], 
        "Obitos_Confirmados": [total_obitos_comorb[c] for c in 
comorbidades] # Nome corrigido para bater com o cálculo 
    }) 
 
    # Cálculo da Letalidade % (Evita divisão por zero se não houver casos) 
    res["Letalidade_%"] = (res["Obitos_Confirmados"] / 
    res["Total_Casos_com_Comorbidade"] * 100).round(2).fillna(0) 
     
    # Ordenar pelas mais fatais 
    res = res.sort_values(by="Letalidade_%", ascending=False) 
 
    # --- O PRINT DOS DADOS NO CONSOLE --- 
    print(f"\n{'-'*65}") 
    print(f"{'TABELA CONSOLIDADA DE COMORBIDADES':^65}") 
    print(f"{'-'*65}") 
    print(res.to_string(index=False)) 
    print(f"{'-'*65}\n") 
     
    return res 
 
if __name__ == "__main__": 
    analisar_letalidade_comorbidades("dados")