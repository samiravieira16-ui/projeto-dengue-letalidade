import pandas as pd
from IPython.display import display, HTML

# Criando os dados estruturados idênticos ao PDF Oficial
documentacao_dados = [
    [1, "Tipo_Notificacao", 'TP_NOT', 'Char(1)', '1-Negativa, 2-Individual, 3-Surto', 'Identifica o tipo da notificação realizada.'],
    [2, "Agravo", 'ID_AGRAVO', 'Char(5)', 'A90 (Dengue)', 'Nome e código do agravo notificado segundo a CID-10.'],
    [3, "Data_Notificacao", 'DT_NOTIFIC', 'Data', 'dd/mm/aaaa', 'Data de preenchimento da ficha de notificação.'],
    [4, "Semana_Notificacao", 'SEM_NOT', 'Char(6)', 'Ano e Sem. Epidemiológica', 'Semana epidemiológica calculada pelo SINAN.'],
    [5, "Ano_Notificacao", 'NU_ANO', 'Char(4)', 'Ex: 2021, 2022', 'Ano da notificação extraído da data.'],
    [6, "UF_Notificacao", 'SG_UF_NOT', 'Char(2)', 'Códigos IBGE (Ex: SP)', 'Sigla da UF da Unidade de Saúde notificante.'],
    [7, "Municipio_Notificacao", 'ID_MUNICIP', 'Char(6)', 'Código IBGE 6 dígitos', 'Município de notificação da Unidade de Saúde.'],
    [8, "Regional_Saude", 'ID_REGIONA', 'Char(4)', 'Códigos regionais SUS', 'Regional Administrativa de Saúde do Município.'],
    [9, "Unidade_Saude", 'ID_UNIDADE', 'Num(7)', 'Código CNES', 'Código do Cadastro Nacional de Estabelecimentos '],
    [10, "Data_Primeiros_Sintomas", 'DT_SIN_PRI', 'Data', 'dd/mm/aaaa', 'Data do início dos primeiros sintomas referidos.'],
    [11, "Semana_Primeiros_Sintomas", 'SEM_PRI', 'Char(6)', 'Ano e Sem. Epidemiológica', 'Semana do início dos sintomas.'],
    [12, "Ano_Nascimento", 'ANO_NASC', 'Char(4)', 'Ex: 1985, 2002', 'Ano de nascimento.'],
    [13, "Idade_Paciente", 'NU_IDADE_N', 'Num(4)', 'Tipo + Idade (Ex: 4022 = 22 Anos)', 'Idade codificada na hora da consulta.'],
    [14, "Sexo_Paciente", 'CS_SEXO', 'Char(1)', 'M, F, I', 'Sexo paciente M (Masculino) / F (Feminino) / I.'],
    [15, "Paciente_Gestante", 'CS_GESTANT', 'Char(1)', '1 a 4 (Tri), 5-Não, 6-N/A', 'Idade gestacional e ocorrência de gravidez.'],
    [16, "Raca_Cor_Paciente", 'CS_RACA', 'Char(1)', '1-Branca, 2-Preta, 3-Amarela...', 'Classificação de raça segundo escopo do IBGE.'],
    [17, "Escolaridade_Paciente", 'CS_ESCOL_N', 'Char(2)', '00 a 10', 'Grau de instrução educacional final do paciente.'],
    [18, "Sintoma_Febre", 'FEBRE', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Ocorrência de quadro febril agudo.'],
    [19, "Sintoma_Mialgia", 'MIALGIA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Ocorrência de dores musculares.'],
    [20, "Sintoma_Cefaleia", 'CEFALEIA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Ocorrência de fortes dores de cabeça.'],
    [21, "Sintoma_Exantema", 'EXANTEMA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Aparecimento de erupções e manchas na pele.'],
    [22, "Sintoma_Vomito", 'VOMITO', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Episódios de vômitos gástricos.'],
    [23, "Sintoma_Nausea", 'NAUSEA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Ocorrência grave de enjoos.'],
    [24, "Sintoma_DorCostas", 'DOR_COSTAS', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Dor severa na lombar ou coluna relatada.'],
    [25, "Sintoma_Conjuntivite", 'CONJUNTVIT', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Diagnóstico de Conjuntivite inflamatória.'],
    [26, "Sintoma_Artrite", 'ARTRITE', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Inflamação excessiva das articulações.'],
    [27, "Sintoma_Artralgia", 'ARTRALGIA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Dores intensas e limitação nas articulações.'],
    [28, "Sintoma_Petequias", 'PETEQUIA_N', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Sinais de microhemorragias no tecido da pele.'],
    [29, "Sintoma_Leucopenia", 'LEUCOPENIA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Hemograma demonstra baixa imunidade de leucócitos.'],
    [30, "Sintoma_ProvaLaco", 'LACO', 'Char(1)', '1-Positivo, 2-Negativo', 'Resultado do teste clínico da Prova do Laço.'],
    [31, "Sintoma_DorRetroorbital", 'DOR_RETRO', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Dores atrás do globo ocular típicas de mosquito.'],
    [32, "Comorbidade_Diabetes", 'DIABETES', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Doença prévia diagnosticada de Diabetes.'],
    [33, "Comorbidade_Hematologica", 'HEMATOLOG', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Hemoglobinopatias, anemias e falhas sanguíneas.'],
    [34, "Comorbidade_Hepatopatia", 'HEPATOPAT', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Doenças base relacionadas a insuficiência de Fígado.'],
    [35, "Comorbidade_Renal", 'RENAL', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Condição crônica nos rins anterior ao vírus.'],
    [36, "Comorbidade_Hipertensao", 'HIPERTENSA', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Histórico atestado de pressão arterial alta.'],
    [37, "Comorbidade_AcidoPeptica", 'ACIDO_PEPT', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Pacientes em tratamento contínuo gástrico interno.'],
    [38, "Comorbidade_AutoImune", 'AUTO_IMUNE', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Agressão ou falhas nativas auto-imunes sistêmicas.'],
    [39, "Data_Investigacao", 'DT_INVEST', 'Data', 'dd/mm/aaaa', 'Processamento epidemiológico físico do município.'],
    [40, "Classificacao_Final", 'CLASSI_FIN', 'Char(2)', '10, 11 e 12 (Dengue Geral)', 'Status decisivo da moléstia infecciosa do CID-10.'],
    [41, "Criterio_Confirmacao", 'CRITERIO', 'Char(1)', '1-Laboratório, 2-Clínico', 'Metodologia que cravou o diagnóstico exato final.'],
    [42, "Caso_Autoctone", 'TPAUTOCTO', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Infectado no domicílio original / Mesma região da consulta.'],
    [43, "UF_Infeccao", 'COUFINF', 'Num(2)', 'Código IBGE', 'Estado importador caso picado em fronteira de estado (Autoctone=Não).'],
    [44, "Pais_Infeccao", 'COPAISINF', 'Num(3)', 'Código do País', 'Origem externa internacional em caso de importação.'],
    [45, "Municipio_Infeccao", 'COMUNINF', 'Num(6)', 'Código IBGE', 'Risco vetorial do local inicial assinalado da infecção provavel.'],
    [46, "Evolucao_Caso", 'EVOLUCAO', 'Char(1)', '1-Cura, 2-Obito Dengue...', 'Desfecho e encerramento clínico da sobrevivência da taxa.'],
    [47, "Data_Obito", 'DT_OBITO', 'Data', 'dd/mm/aaaa', 'Data preenchida da declaração de óbito decorrente.'],
    [48, "Data_Encerramento", 'DT_ENCERRA', 'Data', 'dd/mm/aaaa', 'Fechamento final do monitoramento e preenchimento DataSUS.'],
    [49, "Ocorreu_Hospitalizacao", 'HOSPITALIZ', 'Char(1)', '1-Sim, 2-Não, 3-Ignorado', 'Sinaliza internamento com pernoites em prontuários na unidade.']
]

# Transformando num DataFrame Pandas
df_dicionario = pd.DataFrame(documentacao_dados, columns=[
    "Seq.", "Nome do Campo (Novo)", "Campo Original", "Tipo", "Categoria / Valores Possíveis", "Descrição / Características"
])

# Para exibir uma tabela renderizada bonita no Colab:
display(HTML(df_dicionario.to_html(index=False, classes='table table-striped')))
