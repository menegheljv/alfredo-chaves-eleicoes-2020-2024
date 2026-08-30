# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os, base64, io
from datetime import datetime

BASE = r"C:\Users\Usuario\AppData\Local\Temp\claude\C--Users-Usuario--claude\4e1e3fc3-3daa-446a-a271-77774852efe5\scratchpad\tse"
OUT = os.path.join(BASE, "output")

BLUE = "#1D4E8F"
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

# Registro das 9 pesquisas eleitorais para Alfredo Chaves, 2024
# fonte: pesqele-divulgacao.tse.jus.br, consulta as pesquisas registradas
polls = [
    ("ES-09808/2024", "SOLUÇÃO TREINAMENTO MKT E PESQUISAS", "19/04/2024"),
    ("ES-03038/2024", "I9 - INOVE CONSULTORIA", "20/06/2024"),
    ("ES-03088/2024", "DIRETA PROPAGANDA E EVENTOS", "13/08/2024"),
    ("ES-08806/2024", "INSTITUTO VERITA", "29/08/2024"),
    ("ES-08536/2024", "DIRETA PROPAGANDA E EVENTOS", "11/09/2024"),
    ("ES-04825/2024", "I9 - INOVE CONSULTORIA", "18/09/2024"),
    ("ES-08726/2024", "DIRETA PROPAGANDA E EVENTOS", "26/09/2024"),
    ("ES-00808/2024", "IPOPES PESQUISA DE OPINIÃO", "26/09/2024"),
    ("ES-06358/2024", "I9 - INOVE CONSULTORIA", "27/09/2024"),
]
dates = [datetime.strptime(p[2], "%d/%m/%Y") for p in polls]
labels = [f"{p[1]}\n{p[0]}" for p in polls]
eleicao = datetime(2024, 10, 6)

fig, ax = plt.subplots(figsize=(10.5, 5.4))
y = range(len(polls))
ax.hlines(y, [dates[0]]*len(y), dates, color=GRID, linewidth=1, zorder=1)
ax.scatter(dates, y, s=90, color=GOLD, zorder=3, edgecolor=INK, linewidth=0.6)
ax.axvline(eleicao, color=BLUE, linewidth=1.6, linestyle='--', zorder=2)
ax.text(eleicao, len(polls)-0.3, ' dia da eleição\n 06/10/2024', color=BLUE, fontsize=9, fontweight='bold', va='top')

for yi, d in zip(y, dates):
    ax.text(d, yi, f"  {d.strftime('%d/%m')}", va='center', fontsize=8.5, color=INK)

ax.set_yticks(list(y))
ax.set_yticklabels(labels, fontsize=8.8)
ax.invert_yaxis()
ax.set_xlim(datetime(2024,4,1), datetime(2024,10,15))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.spines[['top','right','left']].set_visible(False)
ax.tick_params(left=False)
ax.grid(axis='x', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.set_title("Registro das 9 pesquisas eleitorais — Alfredo Chaves, 2024", fontsize=13, fontweight='bold', pad=14)
plt.tight_layout()
b64 = fig_to_b64(fig)
with open(os.path.join(OUT, "chart_pesquisas_timeline.b64"), 'w') as f:
    f.write(b64)
print("Chart gerado: pesquisas_timeline")
