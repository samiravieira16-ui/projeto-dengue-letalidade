import pandas as pd 
import glob 
import os 

def analisar_letalidade_comorbidades(pasta_dados, pasta_saida="resultados"): 
    """Analisa letalidade por comorbidade a partir de arquivos Parquet."""
    
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
 
    print(f"\n{'='*70}") 
    print(f"📊 INICIANDO MAPEAMENTO DE COMORBIDADES") 
    print(f"{'='*70}") 
 
    for arquivo in arquivos: 
        print(f"📖 Lendo: {os.path.basename(arquivo)}") 
        # Lê apenas as colunas necessárias 
        df = pd.read_parquet(arquivo, columns=comorbidades + ["Desfecho_Caso"]) 
         
        # Padroniza o desfecho para string e remove o ".0" 
        df["Desfecho_Caso"] = df["Desfecho_Caso"].astype(str).str.replace(".0", "", regex=False).str.strip() 
         
        for c in comorbidades: 
            # Padroniza a comorbidade (1 = Sim) 
            df[c] = df[c].astype(str).str.replace(".0", "", regex=False).str.strip() 
             
            # Contagem absoluta: quem tem a doença e quem morreu com ela 
            n_casos = (df[c] == "1").sum() 
            n_obitos = ((df[c] == "1") & (df["Desfecho_Caso"] == "2")).sum() 
             
            total_casos_comorb[c] += n_casos 
            total_obitos_comorb[c] += n_obitos 
 
    # Criando a tabela final 
    res = pd.DataFrame({ 
        "Comorbidade": comorbidades, 
        "Total_Casos_com_Comorbidade": [total_casos_comorb[c] for c in comorbidades], 
        "Obitos_Confirmados": [total_obitos_comorb[c] for c in comorbidades]
    }) 
 
    # Cálculo da Letalidade % 
    res["Letalidade_%"] = (res["Obitos_Confirmados"] / res["Total_Casos_com_Comorbidade"] * 100).round(2).fillna(0) 
     
    # Ordenar pelas mais fatais 
    res = res.sort_values(by="Letalidade_%", ascending=False) 
 
    # --- EXIBIR TABELA NO CONSOLE --- 
    print(f"\n{'-'*70}") 
    print(f"{'TABELA CONSOLIDADA DE COMORBIDADES':^70}") 
    print(f"{'-'*70}") 
    print(res.to_string(index=False)) 
    print(f"{'-'*70}") 
    
    # --- EXIBIR GRÁFICO DE PIZZA EM ASCII --- 
    exibir_grafico_pizza_ascii(res)
     
    return res 


def exibir_grafico_pizza_ascii(df_resultado):
    """Exibe um gráfico de pizza em ASCII com a distribuição de óbitos."""
    
    df_obitos = df_resultado[df_resultado['Obitos_Confirmados'] > 0].sort_values('Obitos_Confirmados', ascending=False)
    
    total_obitos = df_obitos['Obitos_Confirmados'].sum()
    
    print(f"\n{'='*70}")
    print(f"{'🔺 GRÁFICO DE ÓBITOS POR COMORBIDADE':^70}")
    print(f"{'='*70}\n")
    
    # Calcular percentuais
    df_obitos_pct = df_obitos.copy()
    df_obitos_pct['Percentual'] = (df_obitos_pct['Obitos_Confirmados'] / total_obitos * 100).round(1)
    
    # Exibir gráfico de barras horizontal em ASCII
    max_width = 45
    max_obitos = df_obitos['Obitos_Confirmados'].max()
    
    for idx, row in df_obitos_pct.iterrows():
        comorb = row['Comorbidade'].replace('Comorb_', '')
        obitos = int(row['Obitos_Confirmados'])
        pct = row['Percentual']
        
        # Calcular tamanho da barra
        barra_size = int((obitos / max_obitos) * max_width)
        barra = '█' * barra_size
        
        print(f"  {comorb:20} {barra:45} {obitos:6} óbitos ({pct:5.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"  {'TOTAL':20} {' '*45} {total_obitos:6} óbitos")
    print(f"{'='*70}\n")

 
if __name__ == "__main__": 
    analisar_letalidade_comorbidades("dados")