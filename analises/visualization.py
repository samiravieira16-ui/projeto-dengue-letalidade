"""
Módulo de Visualização - Gráficos para análises epidemiológicas de dengue
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('Agg')  # Backend não-interativo


def criar_grafico_barras(df, coluna_x, coluna_y, titulo, xlabel, ylabel, 
                         pasta_saida, nome_arquivo, largura=12, altura=6, 
                         cores=None, rotacao=45):
    """
    Cria um gráfico de barras vertical ou horizontal.
    
    Parâmetros:
    - df: DataFrame com os dados
    - coluna_x: Coluna para eixo X
    - coluna_y: Coluna para eixo Y
    - titulo: Título do gráfico
    - xlabel: Rótulo do eixo X
    - ylabel: Rótulo do eixo Y
    - pasta_saida: Pasta para salvar o gráfico
    - nome_arquivo: Nome do arquivo PNG
    - largura, altura: Dimensões do gráfico
    - cores: Paleta de cores (opcional)
    - rotacao: Ângulo de rotação dos rótulos X
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(largura, altura))
    
    if cores is None:
        cores = plt.cm.viridis(range(len(df)))
    
    barras = ax.bar(df[coluna_x], df[coluna_y], color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    plt.xticks(rotation=rotacao, ha='right')
    
    # Adicionar valores nas barras
    for barra in barras:
        altura_barra = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura_barra,
                f'{altura_barra:.1f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho


def criar_grafico_historico_temporal(df, data_col, valor_col, titulo, ylabel,
                                     pasta_saida, nome_arquivo, largura=14, altura=6):
    """
    Cria um gráfico de linha para séries temporais.
    
    Parâmetros:
    - df: DataFrame com os dados
    - data_col: Coluna com datas
    - valor_col: Coluna com valores
    - titulo: Título do gráfico
    - ylabel: Rótulo do eixo Y
    - pasta_saida: Pasta para salvar
    - nome_arquivo: Nome do arquivo PNG
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(largura, altura))
    
    ax.plot(df[data_col], df[valor_col], linewidth=2.5, color='#2ecc71', marker='o', markersize=6)
    ax.fill_between(df[data_col], df[valor_col], alpha=0.3, color='#2ecc71')
    
    ax.set_xlabel('Data', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho


def criar_grafico_scatter(df, coluna_x, coluna_y, titulo, xlabel, ylabel,
                          pasta_saida, nome_arquivo, tamanho=100, largura=10, altura=6):
    """
    Cria um gráfico de dispersão.
    
    Parâmetros:
    - df: DataFrame com os dados
    - coluna_x, coluna_y: Colunas para os eixos
    - titulo, xlabel, ylabel: Títulos
    - pasta_saida, nome_arquivo: Localização
    - tamanho: Tamanho dos pontos
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(largura, altura))
    
    scatter = ax.scatter(df[coluna_x], df[coluna_y], s=tamanho, alpha=0.6, 
                        c=range(len(df)), cmap='plasma', edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    plt.colorbar(scatter, ax=ax)
    plt.tight_layout()
    
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho


def criar_multiplos_graficos_comparacao(df, coluna_categoria, colunas_metricas, titulo,
                                        pasta_saida, nome_arquivo, largura=14, altura=8):
    """
    Cria múltiplos gráficos lado-a-lado para comparação.
    
    Parâmetros:
    - df: DataFrame
    - coluna_categoria: Coluna com categorias
    - colunas_metricas: Lista de colunas para comparar
    - titulo: Título geral
    - pasta_saida, nome_arquivo: Localização
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    n_plots = len(colunas_metricas)
    fig, axes = plt.subplots(1, n_plots, figsize=(largura, altura))
    
    if n_plots == 1:
        axes = [axes]
    
    cores_palette = plt.cm.Set2(range(len(df)))
    
    for idx, (ax, col) in enumerate(zip(axes, colunas_metricas)):
        ax.bar(df[coluna_categoria], df[col], color=cores_palette, alpha=0.8, edgecolor='black')
        ax.set_title(col, fontsize=12, fontweight='bold')
        ax.set_xlabel('', fontsize=10)
        ax.set_ylabel('Quantidade', fontsize=10, fontweight='bold')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    fig.suptitle(titulo, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho


def criar_heatmap(df, titulo, pasta_saida, nome_arquivo, largura=10, altura=6):
    """
    Cria um mapa de calor (heatmap).
    
    Parâmetros:
    - df: DataFrame (com índice e colunas bem definidos)
    - titulo: Título do gráfico
    - pasta_saida, nome_arquivo: Localização
    """
    
    import seaborn as sns
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(largura, altura))
    
    sns.heatmap(df, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Frequência'}, ax=ax)
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho


def imprimir_resumo_grafico(titulo, lista_arquivos):
    """
    Imprime um resumo dos gráficos gerados com formatação.
    
    Parâmetros:
    - titulo: Título do resumo
    - lista_arquivos: Lista de caminhos dos arquivos gerados
    """
    
    print(f"\n{'='*70}")
    print(f"📈 {titulo}")
    print(f"{'='*70}")
    
    for idx, arquivo in enumerate(lista_arquivos, 1):
        nome = os.path.basename(arquivo)
        print(f"  ✅ [{idx}] {nome}")
    
    print(f"{'='*70}\n")


def visualizar_analise_comorbidades(df_resultado, pasta_saida, nome_arquivo='analise_comorbidades.png'):
    """
    Cria um gráfico de barras mostrando a taxa de letalidade por comorbidade.
    
    Parâmetros:
    - df_resultado: DataFrame com os resultados da análise de comorbidades
    - pasta_saida: Pasta para salvar o gráfico
    - nome_arquivo: Nome do arquivo PNG
    """
    
    # Preparar dados
    df_plot = df_resultado.sort_values('Letalidade_%', ascending=True)
    
    # Criar figura
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Cores gradientes baseadas na taxa de letalidade
    cores = plt.cm.RdYlGn_r(df_plot['Letalidade_%'] / df_plot['Letalidade_%'].max())
    
    # Criar gráfico de barras horizontal
    barras = ax.barh(df_plot['Comorbidade'].str.replace('Comorb_', ''), 
                     df_plot['Letalidade_%'], 
                     color=cores, 
                     edgecolor='black', 
                     linewidth=1.5,
                     alpha=0.85)
    
    # Adicionar valores nas barras
    for idx, (barra, valor) in enumerate(zip(barras, df_plot['Letalidade_%'])):
        ax.text(valor + 0.5, idx, f'{valor:.2f}%', 
                va='center', fontsize=10, fontweight='bold')
    
    # Configurar rótulos e título
    ax.set_xlabel('Taxa de Letalidade (%)', fontsize=12, fontweight='bold')
    ax.set_title('Taxa de Letalidade por Comorbidade em Casos de Dengue', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Adicionar grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar gráfico
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho


def visualizar_dinamica_temporal(df_estatisticas, pasta_saida, nome_arquivo='dinamica_temporal.png'):
    """
    Cria um gráfico de barras mostrando a média de dias até o óbito por sorotipo.
    
    Parâmetros:
    - df_estatisticas: DataFrame com estatísticas da análise temporal
    - pasta_saida: Pasta para salvar o gráfico
    - nome_arquivo: Nome do arquivo PNG
    """
    
    # Preparar dados
    df_plot = df_estatisticas.sort_values('Media_Dias_Sintoma_ao_Obito', ascending=True)
    
    # Criar figura
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Cores gradientes baseadas na média de dias
    max_dias = df_plot['Media_Dias_Sintoma_ao_Obito'].max()
    cores = plt.cm.viridis(df_plot['Media_Dias_Sintoma_ao_Obito'] / max_dias)
    
    # Criar gráfico de barras horizontal
    barras = ax.barh(df_plot.index, 
                     df_plot['Media_Dias_Sintoma_ao_Obito'], 
                     color=cores, 
                     edgecolor='black', 
                     linewidth=1.5,
                     alpha=0.85)
    
    # Adicionar valores nas barras
    for idx, (barra, valor) in enumerate(zip(barras, df_plot['Media_Dias_Sintoma_ao_Obito'])):
        ax.text(valor + 0.2, idx, f'{valor:.1f} dias', 
                va='center', fontsize=10, fontweight='bold')
    
    # Configurar rótulos e título
    ax.set_xlabel('Média de Dias (Sintomas → Óbito)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sorotipo', fontsize=12, fontweight='bold')
    ax.set_title('Dinâmica Temporal: Média de Dias até Óbito por Sorotipo', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Adicionar grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar gráfico
    caminho = os.path.join(pasta_saida, nome_arquivo)
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho
