"

import os

# ─── Dados Fixos (fornecidos pelo usuário) ────────────────────────────────────
col_labels = ['Ano', 'Total de Óbitos', 'Óbitos com Sorotipo Nulo', 'Proporção de Nulos (%)']

data = [
    ['2021', '276', '239', '86.59%'],
    ['2022', '1052', '895', '85.08%'],
    ['2023', '1096', '811', '74.00%'],
    ['2024', '6292', '4340', '68.98%'],
    ['2025', '1761', '1018', '57.81%']
]

# ─── Layout ───────────────────────────────────────────────────────────────────
n_rows = len(data)
row_h_inch = 0.42
fig_w = 10.0
fig_h = 1.6 + (n_rows + 1) * row_h_inch

fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor='white')
ax.set_facecolor('white')
ax.axis('off')

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})

# ─── Título ───────────────────────────────────────────────────────────────────
fig.text(
    0.5, 0.95,
    "Óbitos por Ano — Sorotipo Nulo",
    ha='center', va='top',
    fontsize=14, fontweight='bold', color='black',
    fontfamily='DejaVu Serif',
)

# ─── Dimensões da tabela ──────────────────────────────────────────────────────
margin_l = 0.05
margin_r = 0.95
table_top = 0.82
total_rows_incl_header = n_rows + 1
row_h = (table_top - 0.1) / total_rows_incl_header

# Larguras relativas
col_w_rel = [0.15, 0.25, 0.35, 0.25]
col_w_abs = [w * (margin_r - margin_l) for w in col_w_rel]

table_data = [col_labels] + data

# ─── Renderização ─────────────────────────────────────────────────────────────
for ri, data_row in enumerate(table_data):
    is_header = (ri == 0)
    y_top = table_top - ri * row_h

    for ci, cell_val in enumerate(data_row):
        x0 = margin_l + sum(col_w_abs[:ci])
        w  = col_w_abs[ci]
        cell_bg = '#E0E0E0' if is_header else 'white'

        # Fundo
        rect = plt.Rectangle(
            (x0, y_top - row_h), w, row_h,
            transform=fig.transFigure, figure=fig,
            facecolor=cell_bg, edgecolor='none',
        )
        fig.add_artist(rect)

        # Texto
        fig.text(
            x0 + w / 2, y_top - row_h / 2,
            cell_val,
            ha='center', va='center',
            fontsize=10,
            fontweight='normal',
            color='black',
        )

# ─── Linhas e Bordas ──────────────────────────────────────────────────────────
line_color = '#AAAAAA'
lw = 0.8

def hline(y, color=line_color, width=lw):
    fig.add_artist(plt.Line2D([margin_l, margin_r], [y, y], transform=fig.transFigure, color=color, linewidth=width))

for ri in range(total_rows_incl_header + 1):
    y = table_top - ri * row_h
    if ri == 0 or ri == 1 or ri == total_rows_incl_header:
        hline(y)
    else:
        hline(y, color='#CCCCCC', width=0.5)

# Bordas verticais externas
table_bottom = table_top - total_rows_incl_header * row_h
fig.add_artist(plt.Line2D([margin_l, margin_l], [table_top, table_bottom], transform=fig.transFigure, color=line_color, linewidth=lw))
fig.add_artist(plt.Line2D([margin_r, margin_r], [table_top, table_bottom], transform=fig.transFigure, color=line_color, linewidth=lw))

# ─── Salva ────────────────────────────────────────────────────────────────────
fig.savefig(ARQUIVO_PNG, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)

print(f"✅ Tabela de Sorotipo Nulo salva em: {ARQUIVO_PNG}")
