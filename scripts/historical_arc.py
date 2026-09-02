# -*- coding: utf-8 -*-
"""
Historical arc: mayoral elections in Alfredo Chaves, ES, 2004 to 2024.
Standalone script, reads directly from data/, does not touch pipeline.py's SQLite state.
Produces:
  - output/resumo_prefeito_2004_2024.csv
  - output/chart_historical_arc.b64 (base64 PNG, ready to embed in the case study template)
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import base64
from io import BytesIO

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

YEARS = [2004, 2008, 2012, 2016, 2020, 2024]

def read_secao(year):
    path = os.path.join(DATA, f"secao_{year}_alfredo_chaves.csv")
    df = pd.read_csv(path, sep=';', encoding='utf-8', dtype=str, quotechar='"')
    df.columns = [c.strip().upper() for c in df.columns]
    return df

rows = []
for year in YEARS:
    df = read_secao(year)
    pref = df[df["DS_CARGO"].str.strip().str.upper() == "PREFEITO"].copy()
    pref["QT_VOTOS"] = pd.to_numeric(pref["QT_VOTOS"], errors="coerce").fillna(0).astype(int)
    pref = pref[~pref["NM_VOTAVEL"].str.upper().isin(["VOTO BRANCO", "VOTO NULO"])]
    totals = pref.groupby("NM_VOTAVEL")["QT_VOTOS"].sum().sort_values(ascending=False)
    total_validos = int(totals.sum())
    winner = totals.index[0]
    winner_votes = int(totals.iloc[0])
    winner_pct = round(winner_votes / total_validos * 100, 1)
    runner_up = totals.index[1] if len(totals) > 1 else None
    runner_up_votes = int(totals.iloc[1]) if len(totals) > 1 else None
    runner_up_pct = round(runner_up_votes / total_validos * 100, 1) if runner_up_votes is not None else None
    our_group_won = year == 2024
    rows.append({
        "ano": year,
        "vencedor": winner,
        "pct_vencedor": winner_pct,
        "candidato_do_grupo": winner if our_group_won else runner_up,
        "pct_candidato_do_grupo": winner_pct if our_group_won else runner_up_pct,
        "resultado_do_grupo": "won" if our_group_won else "lost",
        "total_votos_validos": total_validos,
    })

summary = pd.DataFrame(rows)
summary_path = os.path.join(OUT, "resumo_prefeito_2004_2024.csv")
summary.to_csv(summary_path, index=False)
print("=== Mayoral race, Alfredo Chaves, 2004-2024 ===")
print(summary.to_string(index=False))
print(f"\nSaved: {summary_path}")

# ---------------------------------------------------------------------------
# Chart: the group's vote share across six election cycles
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.2), dpi=160)

x = summary["ano"].tolist()
y = summary["pct_candidato_do_grupo"].tolist()
colors = ["#c0392b" if r == "lost" else "#1e8449" for r in summary["resultado_do_grupo"]]

ax.plot(x, y, color="#888888", linewidth=2, zorder=1)
ax.scatter(x, y, s=180, c=colors, zorder=2, edgecolors="white", linewidths=1.5)
ax.axhline(50, color="#999999", linestyle="--", linewidth=1, zorder=0)
ax.text(x[0] - 0.3, 50.8, "50% needed to win", fontsize=9, color="#666666")

for xi, yi, name in zip(x, y, summary["candidato_do_grupo"]):
    label = f"{name.title()}\n{yi:.1f}%"
    ax.annotate(label, (xi, yi), textcoords="offset points", xytext=(0, 16),
                ha="center", fontsize=8.5, color="#333333")

ax.set_xticks(x)
ax.set_ylim(0, 70)
ax.set_ylabel("Vote share of the group's candidate")
ax.set_title("Five losses, then a win: mayoral elections in Alfredo Chaves, 2004-2024", fontsize=13, pad=14)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
buf = BytesIO()
plt.savefig(buf, format="png")
plt.close(fig)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")

chart_path = os.path.join(OUT, "chart_historical_arc.b64")
with open(chart_path, "w", encoding="utf-8") as f:
    f.write(b64)
print(f"Saved: {chart_path}")
