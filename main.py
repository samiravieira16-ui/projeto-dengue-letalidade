import os
import pandas as pd
import traceback

# Importações das funções de análise
from analises.comorbidades_view import analisar_letalidade_comorbidades
from analises.dinamica_temporal import analisar_dinamica_temporal
from analises.letalidade_sorotipos import calcular_letalidade
from analises.severidade_demografia import analisar_severidade_demografia_absoluta
from analises.analisar_obitos_ano_sorotipo import executar_analise_anual

def main():
    PASTA_DADOS = "dados"

    print(f"{'='*80}")
    print(f"{'SISTEMA INTEGRADO DE ANÁLISE EPIDEMIOLÓGICA':^80}")
    print(f"{'='*80}\n")

    try:
        # 1. Análise de Sorotipo
        print("🟡 Executando Análise de Sorotipo...")
        df_soro = calcular_letalidade(PASTA_DADOS)

        # 2. Análise de Comorbidades
        print("\n🟡 Executando Análise de Comorbidades...")
        df_comorb = analisar_letalidade_comorbidades(PASTA_DADOS)

        # 3. Análise Temporal
        print("\n🟡 Executando Análise Temporal (Sintoma ao Óbito)...")
        analisar_dinamica_temporal(PASTA_DADOS)

        # 4. Análise Demográfica
        print("\n🟡 Executando Análise Demográfica (Idade/Sexo)...")
        analisar_severidade_demografia_absoluta(PASTA_DADOS)

        # 5. Análise de Óbitos por Ano e Sorotipo
        print("\n🟡 Executando Análise de Óbitos por Ano e Sorotipo...")
        df_obitos_ano = executar_analise_anual(PASTA_DADOS)

        print(f"\n{'='*80}")
        print(f"{'✅ TODAS AS ANÁLISES CONCLUÍDAS COM SUCESSO!':^80}")
        print(f"{'='*80}")

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
