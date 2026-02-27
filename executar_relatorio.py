import sys
import os

# LOG DE DIAGNÓSTICO INICIAL (Para garantir que o script está rodando)
print("\n>>> SCRIPT INICIADO: Verificando ambiente...", flush=True)

import pandas as pd

# Adiciona o diretório 'analises' ao path para permitir importações dos scripts
caminho_analises = os.path.join(os.getcwd(), 'analises')
print(f">>> Procurando análises em: {caminho_analises}", flush=True)

if caminho_analises not in sys.path:
    sys.path.append(caminho_analises)

# Importação das funções dos arquivos originais
try:
    from analisar_obitos_ano_sorotipo import executar_analise_anual, exibir_tabela_obitos_ano, exibir_grafico_ascii_obitos, exibir_tabela_sorotipo
    from comorbidades_view import analisar_letalidade_comorbidades, exibir_grafico_ascii_comorbidades
    from dinamica_temporal import analisar_dinamica_temporal, exibir_tabela_temporal, exibir_grafico_temporal_ascii
    from letalidade_sorotipos import calcular_letalidade, exibir_tabela_letalidade, exibir_grafico_ascii as exibir_grafico_letalidade_sorotipo
    from severidade_demografia import analisar_severidade_demografia_absoluta, exibir_grafico_demografico_ascii
except ImportError as e:
    print(f"❌ Erro ao importar scripts de análise: {e}")
    sys.exit(1)

def separador():
    print("\n" + "="*80)
    print("="*80 + "\n")

def titulo_secao(titulo):
    print(f"\n{'>' * 5} {titulo.upper()} {'>' * 5}")
    print("-" * 50)

def exibir_comentarios(texto):
    print("\n--- DESCRIÇÃO E COMENTÁRIOS ---")
    print(texto)
    print("-" * 31 + "\n")

def main():
    pasta_dados = 'dados'
    
    print("\n" + "╔" + "═"*78 + "╗", flush=True)
    print("║" + "RELATÓRIO CONSOLIDADO DE LETALIDADE E DINÂMICA DA DENGUE".center(78) + "║", flush=True)
    print("║" + "Status: Iniciando processamento de 5 seções...".center(78) + "║", flush=True)
    print("╚" + "═"*78 + "╝\n", flush=True)

    # --- SEÇÃO 1: EVOLUÇÃO ANUAL E SOROTIPOS ---
    separador()
    titulo_secao("Seção 1: Evolução Anual de Óbitos e Sorotipos")
    print("⏳ Carregando dados anuais e sorotipos...", flush=True)
    try:
        df_consolidado = executar_analise_anual(pasta_dados)
        
        exibir_comentarios(
            "Esta seção apresenta a evolução histórica de óbitos. Observa-se a variação anual "
            "e a predominância de diferentes sorotipos ao longo do tempo."
        )
    except Exception as e:
        print(f"❌ Erro na Seção 1: {e}", flush=True)

    # --- SEÇÃO 2: LETALIDADE POR COMORBIDADES ---
    separador()
    titulo_secao("Seção 2: Impacto das Comorbidades na Letalidade")
    print("⏳ Carregando dados de comorbidades...")
    try:
        df_comorb = analisar_letalidade_comorbidades(pasta_dados)
        
        exibir_comentarios(
            "A presença de comorbidades eleva significativamente o risco de óbito. "
            "Diabetes e Hipertensão costumam ser os fatores mais prevalentes."
        )
    except Exception as e:
        print(f"❌ Erro na Seção 2: {e}")

    # --- SEÇÃO 3: DINÂMICA TEMPORAL (DIAS ATÉ ÓBITO) ---
    separador()
    titulo_secao("Seção 3: Dinâmica Temporal - Dias até o Óbito")
    print("⏳ Carregando dados temporais...")
    try:
        df_temporal = analisar_dinamica_temporal(pasta_dados)
        
        exibir_comentarios(
            "Análise do intervalo entre o início dos sintomas e o desfecho fatal. "
            "Essencial para entender a velocidade de agravamento da doença por sorotipo."
        )
    except Exception as e:
        print(f"❌ Erro na Seção 3: {e}")

    # --- SEÇÃO 4: LETALIDADE POR SOROTIPO ---
    separador()
    titulo_secao("Seção 4: Letalidade Específica por Sorotipo")
    print("⏳ Carregando letalidade por sorotipo...")
    try:
        df_letal_soro = calcular_letalidade(pasta_dados)
        
        exibir_comentarios(
            "Comparação direta da letalidade entre DENV-1, DENV-2, DENV-3 e DENV-4. "
            "Permite identificar qual sorotipo apresenta maior gravidade clínica absoluta."
        )
    except Exception as e:
        print(f"❌ Erro na Seção 4: {e}")

    # --- SEÇÃO 5: PERFIL DEMOGRÁFICO ---
    separador()
    titulo_secao("Seção 5: Perfil Demográfico dos Óbitos")
    print("⏳ Carregando dados demográficos...")
    try:
        df_demog = analisar_severidade_demografia_absoluta(pasta_dados)
        
        exibir_comentarios(
            "Distribuição de óbitos por faixa etária e sexo. Dados fundamentais para "
            "estratégias de vacinação e grupos de risco priorizados."
        )
    except Exception as e:
        print(f"❌ Erro na Seção 5: {e}")

    separador()
    print("✅ RELATÓRIO FINALIZADO".center(80))
    print("="*80)

if __name__ == "__main__":
    main()
