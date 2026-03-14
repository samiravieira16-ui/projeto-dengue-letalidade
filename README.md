## 👥 Membros da Equipe

* **Samira Vieira Santos Almeida**
* **Felipe Emmanuel Leite Lira**
* **Ramon Firmino Bezerra**
* **Pyerre Lima Diniz**

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

| Variável | Categoria | Função na Análise |
| :--- | :--- | :--- |
| `Desfecho_Caso` | Desfecho | Variável alvo base para filtrar incidência de óbitos (valor `2`) ou cura/sobrevivência. |
| `Data_Inicio_Sintomas` | Temporal | Marco inicial da enfermidade do paciente, essencial para os cálculos de velocidade da doença. |
| `Data_Obito` | Desfecho | Variável final do ciclo da doença, usada no cálculo da Dinâmica Temporal. |
| `Sexo` | Demográfica | Verificar a distribuição demográfica dos óbitos entre os sexos biológicos. |
| `Idade_Em_Anos` | Demográfica | Base quantitativa para a estruturação em diferentes faixas etárias (ex: 0-4 até 80+). |
| `SOROTIPO` | Viral | Análise fundamental do percentual da letalidade e óbitos brutos associados às cepas virais (DENV). |
| **Comorbidades*** | Clínica | Extração de features booleanas (1=Sim) para medir cruzamento de letalidade por subgrupo clínico. |

> **(*) Variáveis de Comorbidades incluídas:** `Comorb_Diabetes`, `Comorb_Hematolog`, `Comorb_Hepatopat`, `Comorb_Renal`, `Comorb_Hipertensao`, `Comorb_AcidoPeptica`, `Comorb_AutoImune`.

---

## 3. Objetivos do Projeto

### Objetivo Geral
Investigar o perfil epidemiológico e clínico dos pacientes que evoluíram para óbito por dengue no Brasil, estabelecendo a correlação entre vulnerabilidades biológicas e a velocidade da progressão da doença.

### Objetivos Específicos

* **Evolução de Óbitos (Ano e Sorotipo):** Consolidar o número absoluto de óbitos de forma anual e realizar seu cruzamento em matriz com os respectivos sorotipos identificados (`analisar_obitos_ano_sorotipo.py`).
* **Taxa de Letalidade por Sorotipo:** Determinar percentualmente a letalidade (`Letalidade_%`) para cada variante viral circulante, definindo assim o potencial fatal destas cepas (`letalidade_sorotipos.py`).
* **Mapeamento Clínico de Comorbidades:** Avaliar a força em total de casos, volume de mortes e a correlacionada taxa percentual de letalidade de acordo com cada doença pré-existente (`comorbidades_view.py`).
* **Severidade e Demografia:** Expor graficamente e em valores absolutos como os óbitos se distribuem agrupados pelas variáveis de sexo e múltiplas faixas etárias segmentadas (`severidade_demografia.py`).
* **Dinâmica Temporal do Óbito:** Processar não apenas a média (em dias) entre o primeiro sintoma e a consolidação do óbito, mas extrair a mediana e o desvio padrão organizados estatisticamente por Sorotipo (`dinamica_temporal.py`).
---

## 📂 Estrutura do Projeto

O projeto evoluiu de cadernos isolados (Notebooks) para uma arquitetura orientada a scripts locais consolidados e modulares, otimizado para o Python moderno:

```text
PROJETO-DENGUE-LETALIDADE/
├── analises/                           # Scripts modulares para os Objetivos Específicos:
│   ├── analisar_obitos_ano_sorotipo.py # Análise e contagem de óbitos cruzada com ano e sorotipo
│   ├── comorbidades_view.py            # Mapeamento da incidência e letalidade por comorbidades
│   ├── dinamica_temporal.py            # Avaliação em dias do início de sintomas ao óbito
│   ├── letalidade_sorotipos.py         # Determinação do potencial letal de cada sorotipo viral
│   └── severidade_demografia.py        # Correlação da gravidade dos casos com sexo e faixas etárias
├── dados/                              # Base de dados estruturada para alto desempenho
│   ├── dengue_limpo_part_*.parquet     # Arquivos parquet particionados (2021 a 2025)
│   └── dicionario.py                   # Script para consulta ao dicionário de variáveis do dataset
├── docs/                               # Documentação e referências auxiliares
├── executar_relatorio.py               # Script centralizado para geração do relatório completo
├── main.py                             # Ponto de entrada do sistema / orquestrador principal
├── Limpeza_dos_dados.ipynb             # Histórico iterativo do saneamento preliminar em Notebook
├── install_UV.txt                      # Comando para instanciar/gerenciar o virtualenv moderno (UV)
├── LICENSE                             # Licença de Código Aberto
├── README.md                           # Documento de visão geral (este arquivo)
└── requirements.txt                    # Dependências mapeadas de bibliotecas e pacotes Python
```

### 🚀 Como Executar

A integração de todas as frentes de análise pode ser disparada através do script central de relatório. No terminal de sua preferência (estando virtualenv ativo), execute:

```bash
python executar_relatorio.py
```
Isso produzirá um log detalhado contendo a correlação de dados e projeções estatísticas de todas as seções (Demografia, Sorotipos, Comorbidades e Dinâmica).
