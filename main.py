import os
import pandas as pd
from analises.letalidade_sorotipos import analisar_letalidade_completa
from analises.dinamica_temporal import analisar_dinamica_temporal
from analises.severidade_demografia import analisar_severidade_demografia_absoluta
from analises.comorbidades_view import analisar_letalidade_comorbidades

def main():
    # Configurações de diretórios
    PASTA_DADOS = "dados"
    PASTA_RESULTADOS = "resultados"

    # Garantir que a pasta de saída exista
    if not os.path.exists(PASTA_RESULTADOS):
        os.makedirs(PASTA_RESULTADOS)

    print(f"{'='*60}")
    print(f"{'SISTEMA DE ANÁLISE EPIDEMIOLÓGICA - DENGUE':^60}")
    print(f"{'='*60}\n")

    try:
        # 1. Análise de Letalidade por Sorotipo (Samira)
        print("🚀 [1/4] Iniciando Análise de Letalidade por Sorotipo...")
        df_let = analisar_letalidade_completa(PASTA_DADOS)
        df_let.to_csv(os.path.join(PASTA_RESULTADOS, "1_letalidade_sorotipo.csv"), index=False)
        print("✅ Sucesso: Tabela de letalidade gerada.\n")

        # 2. Dinâmica Temporal (Felipe)
        print("🚀 [2/4] Iniciando Análise de Dinâmica Temporal...")
        stats_temp, _ = analisar_dinamica_temporal(PASTA_DADOS, PASTA_RESULTADOS)
        print("✅ Sucesso: Estatísticas temporais calculadas.\n")

        # 3. Severidade e Demografia (Ramon)
        print("🚀 [3/4] Iniciando Distribuição Demográfica Absoluta...")
        df_demo = analisar_severidade_demografia_absoluta(PASTA_DADOS, PASTA_RESULTADOS)
        print("✅ Sucesso: Perfil demográfico mapeado.\n")

        # 4. Mapeamento de Comorbidades (Pierry)
        print("🚀 [4/4] Iniciando Mapeamento de Comorbidades (View)...")
        df_comorb = analisar_letalidade_comorbidades(PASTA_DADOS, PASTA_RESULTADOS)
        df_comorb.to_csv(os.path.join(PASTA_RESULTADOS, "4_letalidade_comorbidades.csv"), index=False)
        print("✅ Sucesso: Letalidade por comorbidade finalizada.\n")

        print(f"{'='*60}")
        print(f"{'ANÁLISE COMPLETA FINALIZADA COM SUCESSO!':^60}")
        print(f"Confira os arquivos na pasta: {PASTA_RESULTADOS}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO DURANTE A EXECUÇÃO: {e}")

if __name__ == "__main__":
    main()