# 📊 Guia de Visualizações - Análises de Dengue

Este guia explica como usar o módulo de visualização para criar gráficos dos resultados das análises epidemiológicas.

## 📁 Estrutura

```
analises/
├── visualization.py          # Módulo com funções de gráficos reutilizáveis
├── comorbidades_view.py     # Análise de comorbidades COM visualizações
├── letalidade_sorotipos.py  # Análise de sorotipos
├── dinamica_temporal.py     # Análise temporal
└── severidade_demografia.py # Análise demográfica
```

## 🎨 Módulo de Visualização

O arquivo `visualization.py` fornece funções prontas para criar diversos tipos de gráficos:

### 1. **Gráfico de Barras Vertical/Horizontal**
```python
from analises.visualization import criar_grafico_barras

criar_grafico_barras(
    df=dados,
    coluna_x='Categoria',
    coluna_y='Valor',
    titulo='Meu Gráfico',
    xlabel='Eixo X',
    ylabel='Eixo Y',
    pasta_saida='resultados',
    nome_arquivo='meu_grafico.png',
    largura=12,
    altura=6,
    rotacao=45
)
```

### 2. **Gráfico de Série Temporal**
```python
from analises.visualization import criar_grafico_historico_temporal

criar_grafico_historico_temporal(
    df=dados_temporais,
    data_col='Data',
    valor_col='Casos',
    titulo='Série Temporal de Casos',
    ylabel='Número de Casos',
    pasta_saida='resultados',
    nome_arquivo='temporal.png'
)
```

### 3. **Gráfico de Dispersão (Scatter)**
```python
from analises.visualization import criar_grafico_scatter

criar_grafico_scatter(
    df=dados,
    coluna_x='Idade',
    coluna_y='Dias_Internacao',
    titulo='Relação Idade vs Internação',
    xlabel='Idade (anos)',
    ylabel='Dias de Internação',
    pasta_saida='resultados',
    nome_arquivo='scatter.png',
    tamanho=100
)
```

### 4. **Múltiplos Gráficos de Comparação**
```python
from analises.visualization import criar_multiplos_graficos_comparacao

criar_multiplos_graficos_comparacao(
    df=dados,
    coluna_categoria='Regiao',
    colunas_metricas=['Casos', 'Obitos', 'Recuperados'],
    titulo='Comparação por Região',
    pasta_saida='resultados',
    nome_arquivo='comparacao.png'
)
```

### 5. **Mapa de Calor (Heatmap)**
```python
from analises.visualization import criar_heatmap

criar_heatmap(
    df=matriz_dados,
    titulo='Matriz de Correlação',
    pasta_saida='resultados',
    nome_arquivo='heatmap.png'
)
```

### 6. **Resumo Formatado**
```python
from analises.visualization import imprimir_resumo_grafico

imprimir_resumo_grafico(
    titulo='GRÁFICOS GERADOS',
    lista_arquivos=['resultados/grafico1.png', 'resultados/grafico2.png']
)
```

## 📈 Exemplo Completo

```python
import pandas as pd
from analises.visualization import criar_grafico_barras, imprimir_resumo_grafico

# Carregar dados
df = pd.read_csv('dados.csv')

# Criar pasta de saída
import os
os.makedirs('resultados', exist_ok=True)

# Gerar múltiplos gráficos
graficos = []

# Gráfico 1
g1 = criar_grafico_barras(
    df, 'Comorbidade', 'Letalidade_%',
    'Taxa de Letalidade por Comorbidade',
    'Comorbidade', 'Letalidade (%)',
    'resultados', '01_letalidade.png'
)
graficos.append(g1)

# Gráfico 2
g2 = criar_grafico_barras(
    df, 'Sorotipo', 'Casos',
    'Distribuição de Casos por Sorotipo',
    'Sorotipo', 'Número de Casos',
    'resultados', '02_casos_sorotipo.png'
)
graficos.append(g2)

# Exibir resumo
imprimir_resumo_grafico('VISUALIZAÇÕES FINAIS', graficos)
```

## 🚀 Executar Análises com Gráficos

### Opção 1: Usar o main.py
```bash
python main.py
```

Isso executará todas as análises, incluindo a geração de gráficos de comorbidades.

### Opção 2: Executar análise específica
```bash
python -c "from analises.comorbidades_view import analisar_letalidade_comorbidades; analisar_letalidade_comorbidades('dados')"
```

### Opção 3: Usar diretamente no Jupyter/Colab
```python
from analises.comorbidades_view import analisar_letalidade_comorbidades

df_resultado = analisar_letalidade_comorbidades('dados', 'resultados')
print(df_resultado)
```

## 📋 Arquivos de Saída

Após executar as análises, os seguintes gráficos são gerados em `resultados/`:

### Comorbidades
- `1_grafico_letalidade_comorbidades.png` - Taxa de letalidade por comorbidade
- `2_grafico_casos_comorbidades.png` - Total de casos
- `3_grafico_obitos_comorbidades.png` - Total de óbitos
- `4_grafico_pizza_obitos_comorbidades.png` - Distribuição proporcional

## 🎨 Personalizações

### Alterar Cores
```python
cores_customizadas = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
criar_grafico_barras(..., cores=cores_customizadas)
```

### Alterar Dimensões
```python
criar_grafico_barras(
    ...,
    largura=16,  # Mais largo
    altura=8     # Mais alto
)
```

### Rotação de Rótulos
```python
criar_grafico_barras(
    ...,
    rotacao=90  # Rótulos verticais
)
```

## 📊 Paletas de Cores Disponíveis

As funções usam as seguintes paletas do matplotlib:
- `viridis` - Azul ao amarelo
- `plasma` - Roxo ao amarelo
- `RdYlGn_r` - Vermelho-Amarelo-Verde (invertida)
- `Set2` - Cores pastel
- `Set3` - Cores vibrantes

## ⚙️ Requisitos

Certifique-se de ter instalado:
```bash
pip install matplotlib seaborn pandas
```

Ou use o arquivo de requisitos:
```bash
pip install -r requirements.txt
```

## 💡 Dicas

1. **Alta Resolução**: Os gráficos são salvos com `dpi=300` para impressão
2. **Automatizado**: Use `matplotlib.use('Agg')` em ambientes sem display(como servidores)
3. **Limpeza**: Os gráficos são fechados com `plt.close()` para liberar memória
4. **Reutilizável**: O módulo `visualization.py` funciona com qualquer DataFrame pandas

## 📖 Para Mais Informações

Consulte a documentação do matplotlib: https://matplotlib.org/
E do pandas: https://pandas.pydata.org/
