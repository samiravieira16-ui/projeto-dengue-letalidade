import sys
from pathlib import Path

# Garantir que a raiz do projeto esteja no caminho de importação
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dados.dicionario import df_dicionario

# === RELATÓRIO DE DICIONÁRIO DE DADOS CONSOLIDADO ===

df_interativo = df_dicionario.set_index('Seq.')

print("DICIONÁRIO DE DADOS CONSOLIDADO (DENGUE BR)")


print("\nDESCRIÇÃO DA TABELA:")
print(f"- Linhas: {df_interativo.shape[0]}, Colunas: {df_interativo.shape[1]}")
print("- Colunas: Seq., Nome Novo, Original, Tipo, Valores Possíveis, Descricao")
print("- 'Seq.': número sequencial do campo;")
print("- 'Nome Novo': nome padronizado usado no projeto;")
print("- 'Original': nome original da base/SINAN;")
print("- 'Tipo' e 'Valores Possíveis': formato e códigos esperados;")
print("- 'Descricao': explicação do significado do campo.")

print(df_interativo)
