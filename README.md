
# Projeto Dengue Mortalidade: Fatores de Risco e Evolução Clínica (2021-2025)

## 1. Tema e Problema Definido

**Tema:** Análise dos fatores determinantes da mortalidade por Dengue no Brasil a partir de dados secundários do SINAN.

**Problema:** Embora a Dengue seja uma doença sazonal conhecida, a taxa de letalidade varia drasticamente conforme o perfil do paciente. O ponto central deste projeto é identificar: **Quais combinações de fatores (comorbidades específicas, faixa etária e sexo) estão mais fortemente associadas ao óbito e qual é a janela temporal crítica (dias após o sintoma) em que esses óbitos ocorrem?** A ausência de um padrão claro sobre o tempo de evolução clínica em pacientes com comorbidades dificulta a triagem prioritária e o manejo hospitalar imediato, tornando essencial a identificação desses grupos de risco para reduzir a mortalidade evitável.

---

## 2. Descrição da Base de Dados

A base de dados é extraída do **SINAN (Sistema de Informação de Agravos de Notificação)**, disponibilizada via Kaggle. Ela contém microdados das notificações compulsórias de Dengue no Brasil de 2021 a 2025.

* **Fonte:** SINAN/DATASUS.
* **Ambiente de Análise:** Google Colab (processamento em nuvem via upload).

### Variáveis Selecionadas para o Estudo

| Variável | Categoria | Função na Análise |
| :--- | :--- | :--- |
| `sg_uf_not` | Geográfica | Identificar variações regionais na letalidade. |
| `dt_sin_pri` | Temporal | Marco zero do paciente. Essencial para calcular a velocidade da doença. |
| `cs_sexo` | Demográfica | Verificar disparidades de mortalidade entre sexos biológicos. |
| `nu_idade_n` | Demográfica | Base para criação de faixas etárias (infantil, adulto, idoso). |
| `dt_obito` | Desfecho | Variável alvo para o cálculo do intervalo de tempo de sobrevivência. |
| `sorotipo` | Viral | Analisar se sorotipos específicos (DENV-1 a 4) são mais letais em grupos de risco. |
| **Comorbidades*** | Clínica | Variáveis binárias (Sim/Não) para cálculo de risco relativo. |

> **(*) Comorbidades incluídas:** Diabetes, Doenças Hematológicas, Hepatopatias, Doença Renal, Hipertensão, Ácido Péptico e Doenças Autoimunes.

---

## 3. Objetivos do Projeto

### Objetivo Geral
Investigar o perfil epidemiológico e clínico dos pacientes que evoluíram para óbito por dengue no Brasil, estabelecendo a correlação entre vulnerabilidades biológicas e a velocidade da progressão da doença.

### Objetivos Específicos
* **Mapear a Taxa de Mortalidade por Comorbidade:** Identificar qual agravo preexistente apresenta a maior taxa de letalidade proporcional no banco de dados.
* **Analisar a Variável "Tempo":** Calcular o intervalo médio de dias entre o primeiro sintoma (`dt_sin_pri`) e o óbito, comparando a velocidade da doença em diferentes grupos.
* **Cruzar Perfil Demográfico e Gravidade:** Verificar a prevalência de formas graves da doença por sexo e faixa etária.
* **Subsídio à Triagem:** Propor, com base nos dados, perfis de pacientes que devem ser classificados como "Risco Imediato" no momento da notificação.

---

## 📂 Estrutura de Diretórios (Local)

Para espelhar o trabalho realizado no Colab em seu ambiente local (VS Code), utilize a seguinte estrutura:

```text
PROJETO_DENGUE_SINAN/
├── data/
│   ├── raw/                # CSV original do Kaggle
│   └── processed/          # Dados limpos exportados do Colab
├── docs/                   # Dicionário de dados (PDF) e referências
├── notebooks/
│   ├── 01_notebook_limpeza.ipynb    # Limpeza, tratamento de datas e comorbidades
│   └── 02_analise_mortalidade.ipynb # Análise estatística e cruzamentos
├── results/
│   └── visualizacao.py     # Script para geração automática de gráficos
├── requirements.txt        # Bibliotecas (pandas, numpy, seaborn, matplotlib)
└── README.md               # Documentação do projeto
