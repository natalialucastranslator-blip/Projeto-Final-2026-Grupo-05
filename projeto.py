# O Projeto: um panorama da família Flaviviridae
#
# Leia o enunciado completo no README (seção "O Projeto")
#
# A ideia é construir UMA tabela (pandas) descrevendo os vírus e, a partir dela,
# tirar duas conclusões:
#   - o conteúdo GC é aleatório? (Parte 2)
#   - quão grande é a proteína de cada vírus? (Parte 3)
#
# Vá preenchendo as partes abaixo, uma de cada vez.
# Obs: Se preferir fazer esse processo num jupyter notebook, sem problemas!! Fica a critério do grupo

import pandas as pd

pd.set_option('display.max_columns', None)   # mostra todas as colunas
pd.set_option('display.width', None)         # não quebra linha por largura do terminal
pd.set_option('display.max_colwidth', 30)

from bio.ler_fasta import ler_fasta
from bio.sequencia import (
    traduzir,
    calcular_percentual_gc,
    encontrar_inicio,
)


# ------------------------------------------------------------------
# Parte 1 — Monte a tabela
# ------------------------------------------------------------------
organismos = ler_fasta("arquivos/Flaviviridae-genomes.fasta")
df = pd.DataFrame(organismos)
# print(df.head())
df["tamanho"] = df["sequencia"].apply(len)
print(df.head())


# ------------------------------------------------------------------
# Parte 2 — O conteúdo GC é aleatório?
# ------------------------------------------------------------------
# 1) crie a coluna "gc" com df["sequencia"].apply(calcular_percentual_gc)
# 2) mostre os 10 maiores e os 10 menores GC (com o nome!) -> usar função sort_values do pandas
# 3) escreva sua conclusão sobre o padrão que observou
df["gc"] = df["sequencia"].apply(calcular_percentual_gc)
print(df[["nome", "gc"]].head())
df_ordenado = df.sort_values("gc", ascending=False)
print(df_ordenado[["nome", "gc"]].head(10))
print(df_ordenado[["nome", "gc"]].tail(10))

# Conclusão (Parte 2):
# O conteúdo GC não é aleatório. Os 10 vírus com maior GC são quase
# todos "pegivirus", e os 10 vírus com menor GC são quase todos "pestivirus". isso indica
# que vírus do mesmo gênero tendem a ter conteúdo GC semelhante, e que o conteúdo GC é uma característica do gênero viral.




# ------------------------------------------------------------------
# Parte 3 — Encontre a proteína (a poliproteína viral)
# ------------------------------------------------------------------
# 1) coluna "proteina": traduzir(encontrar_inicio(seq), parar=True)
# 2) coluna "tamanho_proteina": len da proteína
# 3) coluna "cobertura": (tamanho_proteina * 3) / tamanho
# 4) escreva sua conclusão (qual a cobertura típica? faz sentido ser 1 poliproteína?)
df["sequencia"] = df["sequencia"].apply(encontrar_inicio)
df["proteina"] = df["sequencia"].apply(lambda seq: traduzir(seq, parar=True))
df["tamanho_proteina"] = df["proteina"].apply(len)
print(df[["nome", "tamanho", "tamanho_proteina"]].head(10))

df["cobertura"] = (df["tamanho_proteina"] * 3) / df["tamanho"]
print(df["cobertura"].describe())
print("Mediana:", df["cobertura"].median())

# Conclusão (Parte 3):
# A cobertura típica varia, mas a mediana de 0.92 sugere que a maioria dos vírus
# tem uma cobertura significativa da sequência genômica ocupada pela poliproteína.
# Isso faz sentido, pois a poliproteína é uma parte essencial do vírus
# Porém, uma parte dos vírus, mostrou cobertura bem baixa, quase
# zero. Nesses casos o primeiro ATG que a função encontrou não era o começo
# real do gene, então a tradução topou com um stop codon logo no início. Isso
# acontece porque a nossa função encontrar_inicio pega sempre o primeiro ATG
# da sequência, sem checar se é o ATG certo.

# ------------------------------------------------------------------
# Parte 4 — Salve o resultado
# ------------------------------------------------------------------
# 1) filtre os vírus com gc > 0.5 (quantos são?)
# 2) df.to_csv("resultado.csv", index=False)
virus_gc_alto = df[df["gc"] > 0.5]
print(f"Vírus com GC > 0.5: {len(virus_gc_alto)} de {len(df)}")
df.to_csv("resultado.csv", index=False)
