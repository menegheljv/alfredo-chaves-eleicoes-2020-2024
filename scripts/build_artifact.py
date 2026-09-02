# -*- coding: utf-8 -*-
import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "output")

with open(os.path.join(OUT, "template.html"), encoding="utf-8") as f:
    html = f.read()

chart_keys = ["historical_arc", "ibge_eleitorado", "slope", "grid", "municipio", "vereadores_2020", "vereadores_2024", "camara", "votos_vereadores",
              "financeiro_chapa", "custo_por_voto", "origem_receitas", "comparecimento",
              "idade_candidatos", "patrimonio_candidatos", "pesquisas_timeline", "pesquisas_evolucao"]
for key in chart_keys:
    with open(os.path.join(OUT, f"chart_{key}.b64"), encoding="utf-8") as f:
        b64 = f.read().strip()
    placeholder = "{{CHART_%s}}" % key.upper()
    if placeholder not in html:
        print("WARNING: placeholder not found:", placeholder)
    html = html.replace(placeholder, b64)

# ---------------------------------------------------------------------
# tabela seção a seção (com local de votação)
# ---------------------------------------------------------------------
comp = pd.read_csv(os.path.join(OUT, "comparativo_candidato_prefeito_por_secao.csv")).sort_values("NR_SECAO")

def esc(s):
    if pd.isna(s):
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

rows = []
for _, r in comp.iterrows():
    is_flip = r.get('virou_de_derrota_para_vitoria') is True
    is_new = pd.isna(r['pct_2020'])
    cls = ' class="flip"' if is_flip else ''
    v2020 = "&mdash;" if pd.isna(r['votos_candidato_2020']) else f"{int(r['votos_candidato_2020'])}"
    t2020 = "&mdash;" if pd.isna(r['total_secao_2020']) else f"{int(r['total_secao_2020'])}"
    p2020 = "&mdash;" if pd.isna(r['pct_2020']) else f"{r['pct_2020']:.1f}%"
    v2024 = f"{int(r['votos_candidato_2024'])}"
    t2024 = f"{int(r['total_secao_2024'])}"
    p2024 = f"{r['pct_2024']:.1f}%"
    var = "&mdash;" if pd.isna(r['variacao_pp']) else f"{r['variacao_pp']:+.1f} p.p."
    local = esc(r.get('local_votacao', ''))
    if is_new:
        pill = '<span class="pill new">seção nova</span>'
    elif is_flip:
        pill = '<span class="pill win">virou</span>'
    else:
        pill = ''
    rows.append(
        f'<tr{cls}><td>{int(r["NR_SECAO"])}</td><td>{local}</td><td>{v2020}</td><td>{t2020}</td><td>{p2020}</td>'
        f'<td>{v2024}</td><td>{t2024}</td><td>{p2024}</td><td>{var}</td><td>{pill}</td></tr>'
    )

html = html.replace("{{TABLE_ROWS}}", "\n".join(rows))

# ---------------------------------------------------------------------
# tabela de locais de votação únicos
# ---------------------------------------------------------------------
locais = comp.dropna(subset=['local_votacao']).groupby(['local_votacao', 'endereco_votacao'])['NR_SECAO'].apply(
    lambda s: ', '.join(str(int(x)) for x in sorted(s))
).reset_index().sort_values('local_votacao')

loc_rows = []
for _, r in locais.iterrows():
    loc_rows.append(
        f'<tr><td>{esc(r["local_votacao"])}</td><td>{esc(r["endereco_votacao"])}</td><td>{esc(r["NR_SECAO"])}</td></tr>'
    )
html = html.replace("{{TABLE_LOCAIS}}", "\n".join(loc_rows))

final_path = os.path.join(OUT, "case_study.html")
with open(final_path, "w", encoding="utf-8") as f:
    f.write(html)

remaining = html.count("{{")
print("Written:", final_path)
print("Size (KB):", os.path.getsize(final_path) / 1024)
print("Unfilled placeholders remaining:", remaining)
