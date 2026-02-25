#!/usr/bin/env python
"""Script de teste para gerar gráficos das análises"""

from analises.comorbidades_view import analisar_letalidade_comorbidades
import os

# Criar pasta de resultados
os.makedirs('resultados', exist_ok=True)

print("🚀 Gerando análise de comorbidades com gráficos...")
df = analisar_letalidade_comorbidades('dados', 'resultados')

print("\n✅ Análise concluída com sucesso!")
print(f"\nResumo dos resultados:")
print(df.to_string(index=False))

# Listar arquivos gerados
print("\n📁 Arquivos gerados em 'resultados/':")
for arquivo in sorted(os.listdir('resultados')):
    caminho = os.path.join('resultados', arquivo)
    tamanho = os.path.getsize(caminho)
    print(f"  ✓ {arquivo} ({tamanho:,} bytes)")
