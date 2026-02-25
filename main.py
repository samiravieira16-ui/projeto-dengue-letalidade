import os
import pandas as pd
from analises.comorbidades_view import analisar_letalidade_comorbidades
from analises.dinamica_temporal import analisar_dinamica_temporal
from analises.visualization import visualizar_analise_comorbidades

def main():
    # Configurações de diretórios
    PASTA_DADOS = "dados"
    PASTA_RESULTADOS = "resultados"

    # Garantir que a pasta de saída exista
    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)

    print(f"{'='*70}")
    print(f"{'ANÁLISE DE COMORBIDADES EM DENGUE':^70}")
    print(f"{'='*70}\n")

    try:
        # Análise de Comorbidades
        print("🚀 Iniciando análise de dados...\n")
        df_comorb = analisar_letalidade_comorbidades(PASTA_DADOS, PASTA_RESULTADOS)
        
        if df_comorb is not None and len(df_comorb) > 0:
            caminho_csv = os.path.join(PASTA_RESULTADOS, "analise_comorbidades.csv")
            df_comorb.to_csv(caminho_csv, index=False)
            print(f"✅ Arquivo CSV salvo: {caminho_csv}\n")
            
            # Criar visualização
            print("📊 Gerando visualização gráfica...\n")
            caminho_grafico = visualizar_analise_comorbidades(df_comorb, PASTA_RESULTADOS)
            print(f"✅ Gráfico salvo: {caminho_grafico}\n")
            
            print(f"{'='*70}")
            print(f"{'ANÁLISE CONCLUÍDA COM SUCESSO!':^70}")
            print(f"Confira os arquivos na pasta: {PASTA_RESULTADOS}")
            print(f"  📄 {os.path.basename(caminho_csv)}")
            print(f"  📈 {os.path.basename(caminho_grafico)}")
            print(f"{'='*70}\n")
        else:
            print("❌ Nenhum dado foi processado!\n")
        
        # Análise Temporal
        print(f"{'='*70}")
        print(f"{'ANÁLISE DINÂMICA TEMPORAL EM DENGUE':^70}")
        print(f"{'='*70}\n")
        
        stats_temporal = analisar_dinamica_temporal(PASTA_DADOS)
        
        if stats_temporal is not None and len(stats_temporal) > 0:
            print(f"\n✅ Análise temporal completed! (tabela + gráfico no terminal)\n")
            print(f"{'='*70}")
            print(f"{'ANÁLISES FINALIZADAS COM SUCESSO!':^70}")
            print(f"Arquivos gerados na pasta: {PASTA_RESULTADOS}")
            print(f"  ✓ analise_comorbidades.csv")
            print(f"  ✓ analise_comorbidades.png")
            print(f"  (Análise temporal: tabela e gráfico exibidos no terminal)")
            print(f"{'='*70}\n")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE A EXECUÇÃO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()