import pandas as pd
import os

ARQUIVO = "data/processed/dados_lattes_consolidado.csv"
PASTA_OUT = "data/processed/resumos"
os.makedirs(PASTA_OUT, exist_ok=True)

df = pd.read_csv(ARQUIVO)
df.columns = [c.strip() for c in df.columns]

# Padroniza sexo — mantém só Feminino e Masculino
df = df[df["Sexo"].isin(["Feminino", "Masculino"])]

print(f"Total de registros (sem 'Não declarado'): {len(df):,}")
print(f"Anos: {sorted(df['Ano'].unique())}")
print()

# ── 1. Participação feminina geral por ano ────────────────────────────────────
tab1 = df.groupby(["Ano", "Sexo"]).size().unstack(fill_value=0)
tab1["Total"] = tab1.sum(axis=1)
tab1["% Feminino"] = (tab1["Feminino"] / tab1["Total"] * 100).round(1)
print("=== 1. Participação feminina geral por ano ===")
print(tab1.to_string())
tab1.to_csv(f"{PASTA_OUT}/1_participacao_geral_por_ano.csv")
print()

# ── 2. Participação feminina por Grande Área de Formação e Ano ───────────────
tab2 = df.groupby(["Ano", "Grande Área (Formação)", "Sexo"]).size().unstack(fill_value=0)
tab2["Total"] = tab2.sum(axis=1)
tab2["% Feminino"] = (tab2["Feminino"] / tab2["Total"] * 100).round(1)
print("=== 2. % Feminino por Grande Área (Formação) e Ano ===")
print(tab2[["Feminino", "Total", "% Feminino"]].to_string())
tab2.to_csv(f"{PASTA_OUT}/2_por_grande_area_formacao.csv")
print()

# ── 3. Participação feminina em STEM — Formação e Atuação ────────────────────
# STEM = Grande Área in {"Ciências Exatas e da Terra", "Engenharias"}.
# Strings verificadas contra distinct_grande_area_formacao.csv / _atuacao.csv.
# Subespecialidades de Computação (Ciência de Dados, IA, Engenharia de Software,
# Redes de Computadores, Sistemas de Informação) não existem como categoria
# separada nessa taxonomia — ficam em "Ciência da Computação" / Exatas.
# Robótica, Mecatrônica e Automação e Microeletrônica são classificadas em
# "Outra" pelo CNPq, portanto ficam fora do recorte STEM.
# Lista de 8 áreas específicas usada anteriormente (referência histórica):
# areas_stem_legado = [
#     "Ciência da Computação", "Matemática", "Física", "Probabilidade e Estatística",
#     "Engenharia Elétrica", "Engenharia de Produção", "Engenharia Mecânica", "Engenharia Civil",
# ]
GRANDES_AREAS_STEM = {"Ciências Exatas e da Terra", "Engenharias"}

df_stem = df[df["Grande Área (Formação)"].isin(GRANDES_AREAS_STEM)]
tab3 = df_stem.groupby(["Ano", "Área (Formação)", "Sexo"]).size().unstack(fill_value=0)
tab3["Total"] = tab3.sum(axis=1)
tab3["% Feminino"] = (tab3["Feminino"] / tab3["Total"] * 100).round(1)
print("=== 3. % Feminino em STEM por Área (Formação) ===")
print(tab3[["Feminino", "Total", "% Feminino"]].to_string())
tab3.to_csv(f"{PASTA_OUT}/3_areas_stem_formacao.csv")
print()

# Recorte análogo para Atuação
df_stem_atu = df[df["Grande Área (Atuação)"].isin(GRANDES_AREAS_STEM)]
tab3b = df_stem_atu.groupby(["Ano", "Área (Atuação)", "Sexo"]).size().unstack(fill_value=0)
tab3b["Total"] = tab3b.sum(axis=1)
tab3b["% Feminino"] = (tab3b["Feminino"] / tab3b["Total"] * 100).round(1)
print("=== 3b. % Feminino em STEM por Área (Atuação) ===")
print(tab3b[["Feminino", "Total", "% Feminino"]].to_string())
tab3b.to_csv(f"{PASTA_OUT}/3b_areas_stem_atuacao.csv")
print()

# ── 4. Participação feminina por Nível de Formação e Ano ────────────────────
tab4 = df.groupby(["Ano", "Nível (Formação)", "Sexo"]).size().unstack(fill_value=0)
tab4["Total"] = tab4.sum(axis=1)
tab4["% Feminino"] = (tab4["Feminino"] / tab4["Total"] * 100).round(1)
print("=== 4. % Feminino por Nível de Formação ===")
print(tab4[["Feminino", "Total", "% Feminino"]].to_string())
tab4.to_csv(f"{PASTA_OUT}/4_por_nivel_formacao.csv")
print()

# ── 5. Bolsistas PQ (pesquisa) por sexo e ano ────────────────────────────────
if "Bolsista - PQ" in df.columns:
    pq = df[df["Bolsista - PQ"] == "Sim"]
    tab5 = pq.groupby(["Ano", "Sexo"]).size().unstack(fill_value=0)
    tab5["Total"] = tab5.sum(axis=1)
    tab5["% Feminino"] = (tab5["Feminino"] / tab5["Total"] * 100).round(1)
    print("=== 5. Bolsistas PQ por sexo e ano ===")
    print(tab5.to_string())
    tab5.to_csv(f"{PASTA_OUT}/5_bolsistas_pq.csv")
    print()

# ── 6. Área (Atuação) em Computação por sexo e ano ───────────────────────────
comp_atu = df[df["Área (Atuação)"] == "Ciência da Computação"]
tab6 = comp_atu.groupby(["Ano", "Sexo"]).size().unstack(fill_value=0)
tab6["Total"] = tab6.sum(axis=1)
tab6["% Feminino"] = (tab6["Feminino"] / tab6["Total"] * 100).round(1)
print("=== 6. Atuação em Ciência da Computação por sexo e ano ===")
print(tab6.to_string())
tab6.to_csv(f"{PASTA_OUT}/6_atuacao_computacao.csv")
print()

# ── 7. Região de atuação em Computação por sexo ──────────────────────────────
tab7 = comp_atu.groupby(["Região (Atuação)", "Sexo"]).size().unstack(fill_value=0)
tab7["Total"] = tab7.sum(axis=1)
tab7["% Feminino"] = (tab7["Feminino"] / tab7["Total"] * 100).round(1)
print("=== 7. Atuação em Computação por Região ===")
print(tab7[["Feminino", "Total", "% Feminino"]].to_string())
tab7.to_csv(f"{PASTA_OUT}/7_computacao_por_regiao.csv")
print()

print(f"✅ Todos os resumos salvos em: {PASTA_OUT}/")