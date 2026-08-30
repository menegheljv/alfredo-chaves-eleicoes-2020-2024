# A Virada em Alfredo Chaves

Estudo de caso de análise de dados eleitorais comparando as eleições municipais de 2020 e 2024 em Alfredo Chaves-ES, construído inteiramente a partir de dados públicos oficiais do TSE (Tribunal Superior Eleitoral).

**[Ver o estudo de caso completo →](https://claude.ai/code/artifact/657ffe57-13bf-494e-a571-dcf90b30b295)**

## Contexto

Em 2020, a candidatura a prefeito apoiada por esta coordenação perdeu a eleição em Alfredo Chaves-ES. Em 2024, o mesmo grupo elegeu Hugo Luiz, então com 25 anos — o prefeito mais jovem da história do Espírito Santo. Este repositório documenta o pipeline de dados usado para analisar essa virada, do dado bruto do TSE ao estudo de caso final.

## O que tem aqui

- **`scripts/`** — pipeline Python (pandas) e SQL: ingestão, limpeza, normalização e junção dos dados de 2020↔2024, geração de todos os gráficos e montagem final do HTML.
- **`data/`** — CSVs brutos baixados do [dadosabertos.tse.jus.br](https://dadosabertos.tse.jus.br), filtrados para Alfredo Chaves-ES: votação por seção, resultado por candidato, prestação de contas, comparecimento/abstenção, perfil do eleitorado, perfil e bens dos candidatos.
- **`output/`** — resultado do pipeline: tabelas intermediárias (CSV), o template HTML e o `case_study.html` final.

## Datasets TSE usados

| Dataset | Uso |
|---|---|
| Votação por seção eleitoral | Mapear a virada seção a seção, 2020 → 2024 |
| Resultado por candidato (prefeito e vereador) | Comparar desempenho de toda a chapa |
| Prestação de contas eleitorais | Financiamento e eficiência de investimento por voto, todos os candidatos |
| Detalhamento de votação | Comparecimento e abstenção |
| Perfil do eleitorado | Composição por idade e gênero |
| Perfil e bens dos candidatos | Idade, escolaridade, patrimônio declarado |
| Pesquisas eleitorais registradas | Trajetória de intenção de voto ao longo da campanha de 2024 |

## Metodologia

Ingestão e limpeza em `pandas`, junção e agregações em `SQLite`, visualizações em `matplotlib`, montagem final em HTML estático com os gráficos embutidos como base64. Todo achado reportado no estudo de caso é rastreável a um dataset público do TSE — quando um dado não estava publicamente disponível, isso é declarado no texto em vez de estimado.

## Como rodar

```bash
python scripts/pipeline.py
python scripts/vereadores_analysis.py
python scripts/add_locations.py
python scripts/extra_analysis.py
python scripts/candidate_profile_analysis.py
python scripts/viz.py && python scripts/viz2.py && python scripts/viz3.py && python scripts/viz4.py && python scripts/viz5.py && python scripts/viz6.py
python scripts/build_artifact.py
```

Gera `output/case_study.html`.
