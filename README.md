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
* **Ambiente de Análise:** Google Colab (processamento em nuvem via upload).

### Variáveis Selecionadas para o Estudo

## 📋 Dicionário de Dados e Variáveis

Abaixo estão descritas as principais variáveis utilizadas nos scripts de análise, categorizadas por sua função no estudo epidemiológico.

| Variável | Categoria | Função na Análise |
| :--- | :--- | :--- |
| **sg_uf_not** | Geográfica | Identificar variações regionais e disparidades na letalidade entre estados. |
| **dt_sin_pri** | Temporal | Marco zero do paciente. Essencial para calcular o tempo de progressão da doença. |
| **cs_sexo** | Demográfica | Analisar se existe maior vulnerabilidade ou exposição entre sexos biológicos. |
| **nu_idade_n** | Demográfica | Base para converter a idade em faixas etárias (infantil, adulto, idoso). |
| **dt_obito** | Desfecho | Marco final para o cálculo do intervalo de tempo de sobrevivência (Sintoma ➔ Óbito). |
| **evolucao** | Desfecho | **Variável Alvo (Target):** Define se o registro entra no cálculo de letalidade (Óbito vs Cura). |
| **sorotipo** | Viral | Crucial para identificar qual variante (DENV-1 a 4) é mais agressiva no cenário atual. |
| **Comorbidades*** | Clínica | Conjunto de 7 variáveis para medir o risco prévio do paciente. |
| **classi_fin** | Clínica | Confirma se o caso foi tecnicamente classificado como Grave ou com Sinais de Alarme. |

---

### 📝 Notas Adicionais

* **Comorbidades (*):** O estudo considera especificamente um conjunto de 7 condições: *Diabetes, Hematológica, Hepatopatia, Renal, Hipertensão, Ácido-Péptica e Autoimune*.
* **Tempo Médio:** A combinação das variáveis `dt_sin_pri` e `dt_obito` é o que gera os cálculos para o gráfico de **"Dinâmica Temporal"** apresentado no relatório.
> **(*) Comorbidades incluídas:** Diabetes, Doenças Hematológicas, Hepatopatias, Doença Renal, Hipertensão, Ácido Péptico e Doenças Autoimunes.

---

## 3. Objetivos do Projeto

### Objetivo Geral
Investigar o perfil epidemiológico e clínico dos pacientes que evoluíram para óbito por dengue no Brasil, estabelecendo a correlação entre vulnerabilidades biológicas e a velocidade da progressão da doença.

### Objetivos Específicos

* **analisar_obitos_ano_sorotipo:** 
* **Taxa de Letalidade por Sorotipo:** Determinar a letalidade específica para cada sorotipo circulante, avaliando se há predominância de óbitos associada a uma variante viral específica.
* **Análise de Comorbidades:** Mapear a prevalência de doenças preexistentes nos casos fatais, identificando qual agravo apresenta a maior taxa de letalidade proporcional.
* **Severidade e Demografia:** Correlacionar a prevalência de formas graves da doença com as variáveis de sexo e faixa etária.
* **Dinâmica Temporal do Óbito:** Calcular o intervalo médio de dias entre o primeiro sintoma (`dt_sin_pri`) e o óbito, comparando a velocidade da doença entre diferentes grupos.
---

## 📂 Estrutura de Diretórios (Local)

Para espelhar o trabalho realizado no Colab em seu ambiente local (VS Code), utilize a seguinte estrutura:

```text
PROJETO-DENGUE-LETALIDADE/
├── analises/                   # Scripts modulares de análise:
│   ├── analisar_obitos_ano_sorotipo.py
│   ├── comorbidades_view.py
│   ├── dinamica_temporal.py
│   ├── letalidade_sorotipos.py
│   └── severidade_demografia.py
├── dados/                       # Base de dados e dicionários:
│   ├── dicionario.py            # Estrutura de variáveis do Sinan
│   └── *.parquet                # Microdados de 2021 a 2025
├── docs/                        # Documentação técnica de referência
├── executar_relatorio.py        # Script centralizador do relatório no terminal
├── Execução_dos_projetos.ipynb  # Notebook integrado de análises
├── install_UV.txt               # Guia de configuração do ambiente
├── LICENSE                      # Licença do repositório
├── README.md                    # Documentação principal
└── requirements.txt             # Dependências Python atualizadas

