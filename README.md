
# Projeto Dengue Letalidade: Fatores de Risco e Evolução Clínica (2021-2025)

## 1. Tema e Problema Definido

## 👥 Membros da Equipe

* **Samira Vieira Santos Almeida**
* **Felipe Emmanuel Leite Lira**
* **Ramon Firmino Bezerra**
* **Pyerre Lima Diniz**

# Projeto Dengue Letalidade: Fatores de Risco e Evolução Clínica (2021-2025)

## 1. Tema e Problema Definido

**Tema:** Análise dos fatores determinantes da Letalidad por Dengue no Brasil a partir de dados secundários do SINAN.

**Problema:** Embora a Dengue seja uma doença sazonal conhecida, a taxa de letalidade varia drasticamente conforme o perfil do paciente. O ponto central deste projeto é identificar: **Quais combinações de fatores (comorbidades específicas, faixa etária e sexo) estão mais fortemente associadas ao óbito e qual é a janela temporal crítica (dias após o sintoma) em que esses óbitos ocorrem?** A ausência de um padrão claro sobre o tempo de evolução clínica em pacientes com comorbidades dificulta a triagem prioritária e o manejo hospitalar imediato, tornando essencial a identificação desses grupos de risco para reduzir a mortalidade evitável.

---

## 2. Descrição da Base de Dados

A base de dados é extraída do **SINAN (Sistema de Informação de Agravos de Notificação)**, disponibilizada via Kaggle. Ela contém microdados das notificações compulsórias de Dengue no Brasil de 2021 a 2025.

* **Fonte:** SINAN/DATASUS.
* **Ambiente de Análise:** Ambiente local (VS Code) com scripts modulares em Python (processamento de dados e consultas via arquivos `.parquet` para máxima performance).

### Variáveis Selecionadas para o Estudo

## 📋 Dicionário de Dados e Variáveis

Abaixo estão descritas as principais variáveis utilizadas nos scripts de análise, categorizadas por sua função no estudo epidemiológico.

| Variável | Categoria | Função na Análise |
| :--- | :--- | :--- |
| `sg_uf_not` | Geográfica | Identificar variações regionais na letalidade. |
| `dt_sin_pri` | Temporal | Marco zero do paciente. Essencial para calcular a velocidade da doença. |
| `cs_sexo` | Demográfica | Verificar disparidades de letalidade entre sexos biológicos. |
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

* **Taxa de Letalidade por Sorotipo:** Determinar a letalidade específica para cada sorotipo circulante, avaliando se há predominância de óbitos associada a uma variante viral específica.
* **Análise de Comorbidades:** Mapear a prevalência de doenças preexistentes nos casos fatais, identificando qual agravo apresenta a maior taxa de letalidade proporcional.
* **Severidade e Demografia:** Correlacionar a prevalência de formas graves da doença com as variáveis de sexo e faixa etária.
* **Dinâmica Temporal do Óbito:** Calcular o intervalo médio de dias entre o primeiro sintoma (`dt_sin_pri`) e o óbito, comparando a velocidade da doença entre diferentes grupos.
---

## 📂 Estrutura do Projeto

O projeto evoluiu de cadernos isolados (Notebooks) para uma arquitetura orientada a scripts locais consolidados e modulares, otimizado para o Python moderno:

```text
PROJETO-DENGUE-LETALIDADE/
├── analises/                   # Scripts para processamento dos Objetivos Específicos:
│   ├── Letalidade por Sorotipos
│   ├── Dinâmica Temporal (Início de Sintomas ao Óbito)
│   ├── Cruzamento de Severidade e Demografia
│   └── Mapeamento de Letalidade por Comorbidades
├── docs/                       # Documentação técnica e materiais de referência
├── Execução_dos_projetos.ipynb  # Notebook principal que integra e executa as análises
├── install_UV.txt              # Guia de configuração do ambiente via gerenciador UV
├── LICENSE                     # Licença de uso do repositório
├── README.md                   # Documentação principal e visão geral
└── requirements.txt            # Dependências Python para replicação do projeto
