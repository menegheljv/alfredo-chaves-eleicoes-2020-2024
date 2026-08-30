# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os, base64, io, json

BASE = r"C:\Users\Usuario\AppData\Local\Temp\claude\C--Users-Usuario--claude\4e1e3fc3-3daa-446a-a271-77774852efe5\scratchpad\tse"
OUT = os.path.join(BASE, "output")

comp = pd.read_csv(os.path.join(OUT, "comparativo_candidato_prefeito_por_secao.csv"))
merged = pd.read_csv(os.path.join(OUT, "vencedor_por_secao.csv"))
el2020 = pd.read_csv(os.path.join(OUT, "vereadores_eleitos_2020_com_lado.csv"))
el2024 = pd.read_csv(os.path.join(OUT, "vereadores_eleitos_2024_com_lado.csv"))
with open(os.path.join(OUT, "vereadores_summary.json")) as f:
    summ = json.load(f)

# --- palette: Hugo/nossos = azul, adversarios = vermelho ---
BLUE = "#1D4E8F"
BLUE_SOFT = "#4472B0"
BLUE_TINT = "#E6ECF6"
RED = "#B23A2E"
RED_SOFT = "#C96257"
RED_TINT = "#F6E7E4"
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

charts = {}

# =====================================================================
# CHART 1 - Slope (recolor azul/vermelho)
# =====================================================================
c = comp.dropna(subset=['pct_2020', 'pct_2024']).sort_values('NR_SECAO')
fig, ax = plt.subplots(figsize=(10, 6))
for _, row in c.iterrows():
    color = BLUE if row['pct_2024'] >= 50 else RED_SOFT
    ax.plot([0, 1], [row['pct_2020'], row['pct_2024']], color=color, alpha=0.55, linewidth=1.6, zorder=2)
ax.scatter([0]*len(c), c['pct_2020'], color=RED, s=26, zorder=3, label='2020')
ax.scatter([1]*len(c), c['pct_2024'], color=BLUE, s=26, zorder=3, label='2024')
ax.axhline(50, color=GREY, linestyle='--', linewidth=1, alpha=0.7)
ax.text(1.02, 50, '50%', color=GREY, va='center', fontsize=9)
ax.set_xlim(-0.15, 1.15)
ax.set_xticks([0, 1])
ax.set_xticklabels(['2020\n(derrota, 37,8% no municipio)', '2024\n(vitoria, 56,4% no municipio)'], fontsize=10)
ax.set_ylabel('% dos votos validos ao cargo de Prefeito, por secao', fontsize=10)
ax.set_title('Evolucao do candidato a prefeito por secao eleitoral — 2020 vs 2024\nAlfredo Chaves (ES) · 36 secoes comparaveis', fontsize=12, fontweight='bold', pad=14)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
plt.tight_layout()
charts['slope'] = fig_to_b64(fig)

# =====================================================================
# CHART 2 - Grade de secoes (recolor)
# =====================================================================
m = merged.copy().sort_values('NR_SECAO')
def categoria(row):
    if pd.isna(row['vencedor_2020']):
        return 'Secao nova em 2024'
    if row['vencedor_2020'] == 'RONALDO BIANCHI' or 'HUGO' in str(row['vencedor_2020']).upper():
        return 'Ja vencida em 2020'
    return 'Virou: derrota -> vitoria'
m['categoria'] = m.apply(categoria, axis=1)

cat_colors = {
    'Virou: derrota -> vitoria': BLUE,
    'Ja vencida em 2020': BLUE_SOFT,
    'Secao nova em 2024': GREY,
}
n = len(m)
ncols = 7
nrows = -(-n // ncols)
fig, ax = plt.subplots(figsize=(ncols*1.05, nrows*1.05))
for i, (_, row) in enumerate(m.iterrows()):
    r, cidx = divmod(i, ncols)
    color = cat_colors[row['categoria']]
    rect = mpatches.FancyBboxPatch((cidx, nrows-1-r), 0.9, 0.9, boxstyle="round,pad=0.02,rounding_size=0.08",
                                     linewidth=0, facecolor=color)
    ax.add_patch(rect)
    ax.text(cidx+0.45, nrows-1-r+0.45, str(int(row['NR_SECAO'])), ha='center', va='center',
            fontsize=9, color='white', fontweight='bold')
ax.set_xlim(0, ncols)
ax.set_ylim(0, nrows)
ax.set_aspect('equal')
ax.axis('off')
handles = [mpatches.Patch(color=v, label=k) for k, v in cat_colors.items()]
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.03), ncol=3, frameon=False, fontsize=9)
ax.set_title('Todas as 42 secoes eleitorais de Alfredo Chaves em 2024 — vencedor: nosso candidato em 100%\n(numero = numero oficial da secao TSE)',
             fontsize=11, fontweight='bold', pad=10)
plt.tight_layout()
charts['grid'] = fig_to_b64(fig)

# =====================================================================
# CHART 3 - Municipio prefeito (recolor)
# =====================================================================
fig, ax = plt.subplots(figsize=(6.4, 5.6))
anos = ['2020\nRonaldo Bianchi', '2024\nHugo Luiz']
votos = [3681, 5779]
pcts = [37.8, 56.4]
bars = ax.bar(anos, votos, color=[RED, BLUE], width=0.55)
for bar, v_, p_ in zip(bars, votos, pcts):
    ax.text(bar.get_x()+bar.get_width()/2, v_+80, f"{v_} votos\n({p_}%)", ha='center', fontsize=10, fontweight='bold', color=INK)
ax.set_ylabel('Votos validos nominais ao cargo de Prefeito', fontsize=10)
ax.set_title('Resultado municipal — candidato a prefeito\nAlfredo Chaves (ES), 2020 vs 2024', fontsize=12, fontweight='bold', pad=12)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.set_ylim(0, 6600)
plt.tight_layout()
charts['municipio'] = fig_to_b64(fig)

# =====================================================================
# CHART 4 - Vereadores eleitos 2020 (por lado)
# =====================================================================
def verea_chart(df, ano, cadeiras_nossos, total):
    d = df.sort_values('QT_VOTOS_NOMINAIS_VALIDOS', ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5.0))
    colors = [BLUE if lado == 'nossos' else RED for lado in d['LADO']]
    bars = ax.barh(d['NM_URNA_CANDIDATO'] + '  (' + d['SG_PARTIDO'] + ')', d['QT_VOTOS_NOMINAIS_VALIDOS'], color=colors, height=0.62)
    for bar, val in zip(bars, d['QT_VOTOS_NOMINAIS_VALIDOS']):
        ax.text(val + 6, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=9, color=INK)
    ax.set_xlabel('Votos nominais validos', fontsize=10)
    ax.set_title(f'Vereadores eleitos em {ano} — Camara Municipal de Alfredo Chaves\n{cadeiras_nossos} de {total} cadeiras com a chapa (azul) · {total-cadeiras_nossos} com adversarios (vermelho)',
                 fontsize=11.5, fontweight='bold', pad=12)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='x', color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    handles = [mpatches.Patch(color=BLUE, label='Nossa chapa (Hugo Luiz)'),
               mpatches.Patch(color=RED, label='Adversarios')]
    ax.legend(handles=handles, loc='lower right', frameon=False, fontsize=8.5)
    plt.tight_layout()
    return fig_to_b64(fig)

charts['vereadores_2020'] = verea_chart(el2020, 2020, summ['cadeiras_2020_nossos'], summ['cadeiras_2020_total'])
charts['vereadores_2024'] = verea_chart(el2024, 2024, summ['cadeiras_2024_nossos'], summ['cadeiras_2024_total'])

# =====================================================================
# CHART 5 - Camara Municipal: composicao de cadeiras 2020 vs 2024 (barra empilhada)
# =====================================================================
fig, ax = plt.subplots(figsize=(7.5, 3.6))
anos = ['2020', '2024']
nossos = [summ['cadeiras_2020_nossos'], summ['cadeiras_2024_nossos']]
advers = [summ['cadeiras_2020_total']-summ['cadeiras_2020_nossos'], summ['cadeiras_2024_total']-summ['cadeiras_2024_nossos']]
y = range(len(anos))
ax.barh(y, nossos, color=BLUE, height=0.5, label='Nossa chapa')
ax.barh(y, advers, left=nossos, color=RED, height=0.5, label='Adversarios')
for i, (n_, a_) in enumerate(zip(nossos, advers)):
    ax.text(n_/2, i, f"{n_}", va='center', ha='center', color='white', fontsize=13, fontweight='bold')
    ax.text(n_ + a_/2, i, f"{a_}", va='center', ha='center', color='white', fontsize=13, fontweight='bold')
tot = summ['cadeiras_2020_total']
ax.axvline(tot/2, color=INK, linestyle=':', linewidth=1.2, alpha=0.6)
ax.text(tot/2, 1.75, 'maioria simples', ha='center', fontsize=8.5, color=GREY)
ax.set_yticks(list(y))
ax.set_yticklabels(['2020\n(minoria)', '2024\n(maioria)'], fontsize=11)
ax.set_xlim(0, tot + 0.6)
ax.set_xlabel('Cadeiras na Camara Municipal (9 vagas)', fontsize=10)
ax.set_title('A virada politica na Camara de Alfredo Chaves', fontsize=13, fontweight='bold', pad=14)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.tick_params(left=False)
handles = [mpatches.Patch(color=BLUE, label='Nossa chapa (Hugo Luiz)'),
           mpatches.Patch(color=RED, label='Adversarios')]
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, fontsize=9.5)
plt.tight_layout()
charts['camara'] = fig_to_b64(fig)

# =====================================================================
# CHART 6 - Total de votos dos candidatos a vereador da chapa, 2020 vs 2024
# =====================================================================
fig, ax = plt.subplots(figsize=(6.4, 5.6))
anos = ['2020', '2024']
votos = [summ['votos_2020_nossos'], summ['votos_2024_nossos']]
pcts = [summ['votos_2020_nossos']/summ['votos_2020_total']*100, summ['votos_2024_nossos']/summ['votos_2024_total']*100]
bars = ax.bar(anos, votos, color=[RED, BLUE], width=0.5)
for bar, v_, p_ in zip(bars, votos, pcts):
    ax.text(bar.get_x()+bar.get_width()/2, v_+60, f"{v_} votos\n({p_:.1f}% do pleito)", ha='center', fontsize=10, fontweight='bold', color=INK)
ax.set_ylabel('Soma de votos nominais — candidatos a vereador da chapa', fontsize=10)
ax.set_title('Votacao total dos candidatos a vereador da chapa\nAlfredo Chaves (ES), 2020 vs 2024', fontsize=12.5, fontweight='bold', pad=12)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.set_ylim(0, max(votos)*1.25)
plt.tight_layout()
charts['votos_vereadores'] = fig_to_b64(fig)

for k, b64 in charts.items():
    with open(os.path.join(OUT, f"chart_{k}.b64"), 'w') as f:
        f.write(b64)

print("Charts gerados:", list(charts.keys()))
