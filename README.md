
# Projeto Dengue Letalidade: Fatores de Risco e Evolução Clínica (2021-2025)

## 👥 Membros da Equipe

* **Samira Vieira Santos Almeida**
* **Felipe Emmanuel Leite Lira**
* **Ramon Firmino Bezerra**
* **Pyerre Lima Diniz**

## 1. Tema e Problema

**Tema:** Análise dos fatores determinantes da letalidade por Dengue no Brasil a partir de dados secundários do SINAN (2021–2025).

**Problema:** Embora a Dengue seja uma doença sazonal conhecida, a taxa de letalidade varia drasticamente conforme o perfil do paciente. O projeto busca responder: **Quais combinações de fatores (comorbidades, faixa etária e sexo) estão mais fortemente associadas ao óbito, e qual é a janela temporal crítica (dias após o início dos sintomas) em que esses óbitos ocorrem?**

---

## 2. Base de Dados

- **Fonte:** SINAN (Sistema de Informação de Agravos de Notificação) / DATASUS, disponibilizado via Kaggle.
- **Período:** 2021 a 2025 (casos confirmados de Dengue).
- **Formato:** Arquivos `.parquet` particionados por ano para máxima performance de leitura.

### Dicionário de Variáveis

| Variável | Categoria | Função na Análise |
| :--- | :--- | :--- |
| `sg_uf_not` | Geográfica | Variações regionais na letalidade |
| `dt_sin_pri` | Temporal | Marco zero do paciente (início dos sintomas) |
| `cs_sexo` | Demográfica | Disparidades de letalidade entre sexos |
| `nu_idade_n` | Demográfica | Base para criação de faixas etárias |
| `dt_obito` | Desfecho | Cálculo do intervalo de sobrevivência |
| `sorotipo` | Viral | Análise de letalidade por DENV-1 a DENV-4 |
| **Comorbidades** | Clínica | Variáveis binárias (Sim/Não) para risco relativo |

> **Comorbidades incluídas:** Diabetes, Doenças Hematológicas, Hepatopatias, Doença Renal, Hipertensão, Ácido Péptico e Doenças Autoimunes.

---

## 3. Objetivos do Projeto

### Geral
Investigar o perfil epidemiológico e clínico dos pacientes que evoluíram para óbito por dengue no Brasil, correlacionando vulnerabilidades biológicas à velocidade de progressão da doença.

### Específicos

1. **Evolução Anual de Óbitos por Sorotipo** — variação histórica e predominância entre DENV-1 a DENV-4.
2. **Impacto das Comorbidades** — mapeamento das doenças preexistentes com maior taxa de letalidade proporcional.
3. **Dinâmica Temporal** — intervalo médio de dias entre o primeiro sintoma e o óbito por sorotipo.
4. **Letalidade por Sorotipo** — comparação direta da gravidade clínica entre variantes virais.
5. **Perfil Demográfico** — distribuição de óbitos por faixa etária e sexo.

---

## 4. Estrutura do Projeto

```text
PROJETO-DENGUE-LETALIDADE/
│
├── analises/                           # Scripts modulares de análise
│   ├── analisar_obitos_ano_sorotipo.py # Seção 1: Evolução anual e sorotipos
│   ├── comorbidades_view.py            # Seção 2: Impacto das comorbidades
│   ├── dinamica_temporal.py            # Seção 3: Dias até o óbito
│   ├── letalidade_sorotipos.py         # Seção 4: Letalidade por sorotipo
│   └── severidade_demografia.py        # Seção 5: Perfil demográfico dos óbitos
│
├── dados/                              # Dados processados (não versionados)
│   ├── dengue_limpo_part_dengue_2021_confirmados.parquet
│   ├── dengue_limpo_part_dengue_2022_confirmados.parquet
│   ├── dengue_limpo_part_dengue_2023_confirmados.parquet
│   ├── dengue_limpo_part_dengue_2024_confirmados.parquet
│   ├── dengue_limpo_part_dengue_2025_confirmados.parquet
│   └── dicionario.py                   # Mapeamento e codificação das variáveis
│
├── docs/                               # Documentação técnica e materiais de referência
│
├── executar_relatorio.py               # ▶ Script principal — gera o relatório consolidado
├── main.py                             # Script auxiliar de entrada
├── Limpeza_dos_dados.ipynb             # Notebook de limpeza e pré-processamento dos dados brutos
├── install_UV.txt                      # Guia de configuração do ambiente via gerenciador UV
├── requirements.txt                    # Dependências Python
└── README.md                           # Este arquivo
```

---

## 5. Como Executar

### Pré-requisitos

- Python 3.10+
- Dependências listadas em `requirements.txt`

### Instalação

```bash
pip install -r requirements.txt
```

### Gerar o Relatório Consolidado

Execute o script principal a partir da raiz do projeto:

```bash
python executar_relatorio.py
```

O relatório será gerado diretamente no console, organizado em **5 seções** na seguinte ordem:
1. Evolução Anual de Óbitos e Sorotipos
2. Impacto das Comorbidades na Letalidade
3. Dinâmica Temporal — Dias até o Óbito
4. Letalidade Específica por Sorotipo
5. Perfil Demográfico dos Óbitos

---

## 6. Dependências

| Biblioteca | Versão | Uso |
| :--- | :--- | :--- |
| `pandas` | 3.0.1 | Manipulação e análise dos dados |
| `pyarrow` | 23.0.1 | Leitura dos arquivos `.parquet` |
| `tabulate` | 0.9.0 | Formatação de tabelas no terminal |
| `matplotlib` | latest | Geração de gráficos |
| `seaborn` | latest | Visualizações estatísticas |
| `jupyter` | latest | Execução dos notebooks |

---

## 7. Licença

Este projeto está licenciado sob os termos descritos em [LICENSE](./LICENSE).
