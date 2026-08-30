# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os, base64, io
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "output")

BLUE = "#1D4E8F"
RED = "#B23A2E"
GOLD = "#A8791F"
GREY = "#7A8B94"
BG = "#FFFFFF"
GRID = "#E4E9EC"
INK = "#142B32"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
})

def fig_to_b64(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('ascii')
    plt.close(fig)
    return b64

# 6 pesquisas reais (documento original da pesquisa em mãos) + resultado oficial TSE.
# Metodologia "estimulada" em todos os pontos (2 vias em abril, 3 vias a partir de agosto).
main_dates = [datetime(2024,4,16), datetime(2024,8,30), datetime(2024,9,21),
              datetime(2024,9,28), datetime(2024,10,2), datetime(2024,10,6)]
hugo   = [54.8, 57.4, 51.2, 47.75, 51.5, 58.05]
rolmar = [21.6, 30.8, 25.4, 16.25, 29.5, 31.91]
boldrini_dates = [datetime(2024,8,30), datetime(2024,9,21), datetime(2024,9,28), datetime(2024,10,2), datetime(2024,10,6)]
boldrini = [11.8, 11.5, 12.25, 9.4, 10.04]

outlier_date = datetime(2024,9,17)
outlier_hugo, outlier_rolmar, outlier_boldrini = 22.90, 53.23, 12.58

labels = ["16/abr\nInst. Solução", "30/ago\nInst. Veritá", "21/set\nInove Consult.",
          "28/set\nIpopes", "02/out\nI9-Inove", "06/out\nResultado\noficial TSE"]

fig, ax = plt.subplots(figsize=(11, 6.2))

ax.plot(main_dates, hugo, color=BLUE, linewidth=2.8, marker='o', markersize=8, zorder=5, label='Hugo Luiz (nossos)')
ax.plot(main_dates, rolmar, color=RED, linewidth=2.2, marker='o', markersize=7, zorder=4, label='Rolmar Botecchia')
ax.plot(boldrini_dates, boldrini, color=GOLD, linewidth=1.8, marker='o', markersize=6, zorder=3, linestyle='--', label='Boldrini')

# outlier de 17/set, plotado à parte, sem conectar a linha principal
ax.scatter([outlier_date], [outlier_hugo], marker='D', s=70, color=BLUE, alpha=0.35, zorder=6, edgecolor=INK, linewidth=0.8)
ax.scatter([outlier_date], [outlier_rolmar], marker='D', s=70, color=RED, alpha=0.35, zorder=6, edgecolor=INK, linewidth=0.8)
ax.annotate("pesquisa de\n17/set\n(atípica)", xy=(outlier_date, outlier_rolmar), xytext=(outlier_date, 68),
            ha='center', fontsize=8, color=GREY, fontweight='bold',
            arrowprops=dict(arrowstyle='-', color=GREY, linewidth=0.9, shrinkA=2, shrinkB=8))

for d, v in zip(main_dates, hugo):
    ax.text(d, v+2.6, f"{v:.1f}%", ha='center', fontsize=10, fontweight='bold', color=BLUE)
for d, v in zip(main_dates, rolmar):
    ax.text(d, v-4.4, f"{v:.1f}%", ha='center', fontsize=8.8, fontweight='bold', color=RED)

ax.set_xticks(main_dates)
ax.set_xticklabels(labels, fontsize=8.6)
ax.set_ylim(0, 72)
ax.set_ylabel('% intenção de voto (estimulada) / votos válidos', fontsize=10)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.legend(loc='lower left', frameon=False, fontsize=9.5, ncol=3)
ax.set_title("Seis pesquisas reais, abril a outubro: Hugo Luiz nunca saiu da liderança", fontsize=12.5, fontweight='bold', pad=14)
plt.tight_layout()
b64 = fig_to_b64(fig)
with open(os.path.join(OUT, "chart_pesquisas_evolucao.b64"), 'w') as f:
    f.write(b64)
print("Chart gerado: pesquisas_evolucao (6 pontos reais + outlier + resultado)")
