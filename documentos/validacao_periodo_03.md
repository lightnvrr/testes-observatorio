# Relatório de Validação — Período 03

**Data:** Julho/2026  
**Escopo:** Verificação e correção de quatro problemas no pipeline e no documento `periodo_03_estrutura_metodologica.md`.  
**Arquivos verificados:** `consolidar_lattes.py`, `agregar_lattes.py`, `data/raw/lattes_2020–2026.csv`, `data/processed/dados_lattes_consolidado.csv`

---

## Problema 1 — Contagem de registros não fecha

### Constatação

O documento afirmava totais incorretos. Contagem real por arquivo bruto (UTF-16, sep=`\t`):

| Ano | Registros brutos | No consolidado | Diferença |
|---|---|---|---|
| 2020 | 58.584 | 58.584 | 0 |
| 2021 | 66.559 | 66.559 | 0 |
| 2022 | 71.596 | 71.596 | 0 |
| 2023 | 79.937 | 79.937 | 0 |
| 2024 | 76.655 | 76.655 | 0 |
| 2025 | 62.589 | 62.589 | 0 |
| 2026 | 22.424 | — (excluído) | — |
| **Total** | **438.344** | **415.920** | **0** |

### Diagnóstico

**O pipeline não perde nenhum registro.** A diferença entre bruto e consolidado é exatamente o extrato de 2026 (22.424), que é excluído de forma **intencional** pela variável `ANOS = [2020, 2021, 2022, 2023, 2024, 2025]` em `consolidar_lattes.py`.

Os números incorretos no documento (438.351 e 415.921) eram estimativas erradas feitas antes da contagem real. Não há bug no pipeline.

A remoção de 2.874 registros com `Sexo = "Não declarado"` ocorre em `agregar_lattes.py` (filtro de análise), não em `consolidar_lattes.py` — é intencional e já documentada na seção de Limitações.

### Correção aplicada

- `periodo_03_estrutura_metodologica.md` — corrigidos os totais:
  - `438.351` → **`438.344`**
  - `415.921` → **`415.920`**
  - Adicionada explicação de que a exclusão de 2026 é intencional (lista `ANOS` do script).

---

## Problema 2 — Lista STEM com 6 áreas inexistentes na base

### Constatação

A lista `areas_stem` em `agregar_lattes.py` continha 13 itens. Validação contra os 99 valores distintos reais de `Área (Formação)`:

| Área no código | Existe na base? | Freq (Formação) | Freq (Atuação) |
|---|---|---|---|
| Ciência da Computação | ✓ | 7.173 | 8.997 |
| **Ciência de Dados** | **✗** | **0** | **0** |
| **Sistemas de Informação** | **✗** | **0** | **0** |
| **Engenharia de Software** | **✗** | **0** | **0** |
| **Inteligência Artificial** | **✗** | **0** | **0** |
| **Redes de Computadores** | **✗** | **0** | **0** |
| Matemática | ✓ | 5.386 | 7.783 |
| Física | ✓ | 4.979 | 5.650 |
| Engenharia Elétrica | ✓ | 6.168 | 5.246 |
| Engenharia de Produção | ✓ | 3.146 | 2.631 |
| Engenharia Mecânica | ✓ | 4.337 | 3.630 |
| Engenharia Civil | ✓ | 5.748 | 6.075 |
| **Estatística** | **✗** | **0** | **0** |

### Diagnóstico

- As 5 áreas (Ciência de Dados, IA, Eng. de Software, Redes de Computadores, Sistemas de Informação) **não existem como categorias independentes** nessa taxonomia CNPq. Na Plataforma Lattes, essas especialidades são registradas dentro de "Ciência da Computação". Não há grafia alternativa — simplesmente não constam.
- `"Estatística"` **não existe**; a grafia correta na base é **`"Probabilidade e Estatística"`** (586 registros em Formação, 1.014 em Atuação).

### Correção aplicada

**`agregar_lattes.py`** — lista STEM substituída de 13 para 8 áreas validadas:

```python
# ANTES (13 áreas, 6 inexistentes = zero registros)
areas_stem = [
    "Ciência da Computação", "Ciência de Dados", "Sistemas de Informação",
    "Engenharia de Software", "Inteligência Artificial", "Redes de Computadores",
    "Matemática", "Física", "Engenharia Elétrica", "Engenharia de Produção",
    "Engenharia Mecânica", "Engenharia Civil", "Estatística"
]

# DEPOIS (8 áreas, todas com registros reais)
areas_stem = [
    "Ciência da Computação",
    "Matemática", "Física", "Probabilidade e Estatística",
    "Engenharia Elétrica", "Engenharia de Produção",
    "Engenharia Mecânica", "Engenharia Civil",
]
```

**`periodo_03_estrutura_metodologica.md`** — descrição do indicador STEM atualizada para refletir as 8 áreas reais e explicar por que as demais não existem.

---

## Problema 3 — Variações de grafia

### Constatação

Busca por normalização unicode (remoção de acentos, lower, strip) sobre os 99 valores distintos de `Área (Formação)`: **nenhum par duplicado encontrado**. A taxonomia é bem controlada.

Busca manual por termos relacionados (`computac`, `informatica`, `sistemas`, `redes`, `intelig`, `dados`, `estatistic`):

| Termo buscado | Encontrado em `Área (Formação)` | Freq |
|---|---|---|
| `computac` | Ciência da Computação | 7.173 |
| `estatistic` | Probabilidade e Estatística | 586 |
| Demais termos | — | 0 |

### Diagnóstico

O Problema 3 não é de variação de grafia, mas de **nomes errados** (inexistentes) na lista STEM — já resolvido pelo Problema 2. Não é necessário nenhum passo de normalização adicional no pipeline.

### Impacto da correção (Problemas 2 + 3 combinados)

| Coluna analisada | Registros STEM antes | Registros STEM depois | Δ Total | Feminino antes | Feminino depois | Δ Feminino |
|---|---|---|---|---|---|---|
| Área (Formação) | 36.619 | 37.191 | **+572 (+1,6%)** | 9.800 | 10.006 | **+206** |
| Área (Atuação) | 39.696 | 40.692 | **+996 (+2,5%)** | 10.996 | 11.344 | **+348** |

O ganho vem inteiramente da inclusão de `"Probabilidade e Estatística"`. As 5 outras áreas removidas não tinham registros e não alteram nenhum cômputo.

---

## Problema 4 — Link da fonte inconsistente no documento

### Constatação

| Seção | Link | Situação |
|---|---|---|
| Seção 1 — "Link para acesso à fonte" | `dadosabertos.cnpq.br/dataset/lattes` | **Incorreto** — portal de dados abertos, não é a fonte usada |
| Seção 5 — linha principal | `bi.cnpq.br/painel/formacao-atuacao-lattes/` | **Correto** — fonte real |

O código (`consolidar_lattes.py`) não contém nenhuma URL — lê apenas arquivos locais de `data/raw/`. A origem dos arquivos foi confirmada pelo time como o Painel BI do CNPq.

Os dois caminhos são rotas independentes para a mesma informação base (dados Lattes/CNPq), mas com formatos e conteúdos distintos:
- **Painel BI** (`bi.cnpq.br`): exportação CSV/Excel interativa com filtros; foi o que gerou os arquivos `data/raw/`.
- **Portal de Dados Abertos** (`dadosabertos.cnpq.br`): dataset tabular em bulk; poderia ser uma rota alternativa, mas não foi usada.

### Correção aplicada

**`periodo_03_estrutura_metodologica.md`:**
- Seção 1: link corrigido para `bi.cnpq.br`, com nota explicando que o portal de dados abertos é rota alternativa não utilizada.
- Seção 5: linha principal renomeada para "fonte efetivamente utilizada"; portal de dados abertos adicionado como linha secundária com ressalva.

---

## Mudança de definição STEM — Nova definição por Grande Área (julho/2026)

### Motivação

A lista de 8 áreas específicas era incompleta: Química (7.065), Geociências (3.838), Engenharia de Materiais (3.589), Engenharia Química (3.204), Engenharia Sanitária (1.805), Engenharia Biomédica (922), etc. ficavam de fora. A solução estrutural é filtrar pela **Grande Área** em vez de enumerar áreas específicas.

### Strings exatas verificadas

| Grande Área | Grafia exata na base | Formação | Atuação |
|---|---|---|---|
| `"Ciências Exatas e da Terra"` | Verificada contra `distinct_grande_area_formacao.csv` | 29.817 | 37.744 |
| `"Engenharias"` | Verificada contra `distinct_grande_area_atuacao.csv` | 32.630 | 26.793 |
| **Total STEM** | | **62.447** | **64.537** |

### Casos de fronteira verificados

| Área | Grande Área real | Entra no STEM? | Observação |
|---|---|---|---|
| Engenharia Agrícola | Ciências Agrárias (1.314/1.316) | **Não** ✓ | 2 registros de ruído em "Engenharias" |
| Recursos Florestais e Eng. Florestal | Ciências Agrárias (1.897/1.901) | **Não** ✓ | 3 registros de ruído |
| Recursos Pesqueiros e Eng. de Pesca | Ciências Agrárias (678/678) | **Não** ✓ | Limpo |
| Desenho Industrial | Ciências Sociais Aplicadas (1.278/1.279) | **Não** ✓ | 1 registro de ruído |
| Robótica, Mecatrônica e Automação | **Outra** (83/87 Formação; 659/660 Atuação) | **Não** ⚠️ | CNPq classifica como "Outra" — limitação da taxonomia |
| Microeletrônica | **Outra** (16/19 Formação; 113/113 Atuação) | **Não** ⚠️ | Idem |

### Tabela de impacto acumulado (estado inicial → pós P2/P3 → pós nova definição STEM)

| Métrica | Inicial (13 áreas, 6 erradas) | Pós P2/P3 (8 áreas corretas) | Nova STEM (Grande Área) | Δ total |
|---|---|---|---|---|
| **Total Formação** | 36.619 | 37.191 | **61.843** | +25.224 (+68,9%) |
| **Feminino Formação** | 9.800 | 10.006 | **21.465** | +11.665 |
| **% Fem. Formação** | 26,8% | 26,9% | **34,7%** | +7,9 pp |
| **Total Atuação** | 39.696 | 40.692 | **63.920** | +24.224 (+61,0%) |
| **Feminino Atuação** | 10.996 | 11.344 | **22.446** | +11.450 |
| **% Fem. Atuação** | 27,7% | 27,9% | **35,1%** | +7,4 pp |

O aumento de ~7–8 pp no % feminino ocorre porque Química, Geociências e outras Ciências Exatas têm representação feminina mais alta que as Engenharias que já constavam no STEM anterior.

### Limitação nova identificada

`Grande Área (Atuação)` tem **17,4%** de registros com valor `"Não informado"` (72.592 registros). Esses pesquisadores ficam fora do indicador STEM de Atuação mesmo que a área específica deles seja STEM. `Grande Área (Formação)` tem apenas 5,6% — mais aceitável.

### Diff aplicado em `agregar_lattes.py`

Bloco STEM (seção 3) substituído de lista `areas_stem` fixa com filtro em `Área (Formação)` para máscara `GRANDES_AREAS_STEM` com filtro em `Grande Área (Formação)` / `Grande Área (Atuação)`. Lista antiga mantida como comentário de referência histórica. Adicionado recorte análogo para Atuação (tab3b → `3b_areas_stem_atuacao.csv`).

---

## Arquivos gerados nesta validação

| Arquivo | Descrição |
|---|---|
| `documentos/distinct_area_formacao.csv` | 99 valores distintos de `Área (Formação)` com frequência |
| `documentos/distinct_area_atuacao.csv` | 103 valores distintos de `Área (Atuação)` com frequência |
| `documentos/distinct_grande_area_formacao.csv` | 11 valores distintos de `Grande Área (Formação)` com frequência |
| `documentos/distinct_grande_area_atuacao.csv` | 11 valores distintos de `Grande Área (Atuação)` com frequência |
| `documentos/stem_validacao.csv` | Checklist item a item da lista STEM vs. base |
| `documentos/stem_match_aproximado.txt` | Candidatos aproximados para as áreas inexistentes |
| `documentos/spelling_variations.txt` | Resultado da busca por variações de grafia |
| `documentos/impacto_stem.txt` | Contagens da 1ª correção STEM (P2/P3) |
| `documentos/impacto_stem_v2.txt` | Contagens antes/depois da nova definição STEM por Grande Área |
| `documentos/areas_stem_resultantes.csv` | 70 valores de `Área (Formação)` que caem na máscara STEM |
| `documentos/casos_fronteira.txt` | Verificação de Grande Área para 6 áreas específicas de fronteira |

## Resumo das correções aplicadas

| Arquivo | Tipo | O que mudou |
|---|---|---|
| `agregar_lattes.py` | Código | STEM: lista de 13 áreas → lista de 8 → máscara por `Grande Área` (`GRANDES_AREAS_STEM`); lista legada mantida em comentário; adicionado recorte de Atuação (tab3b) |
| `documentos/periodo_03_estrutura_metodologica.md` | Documento | Totais corrigidos; link seção 1 corrigido; indicador STEM redefinido por Grande Área; limitações 4/4b/4c adicionadas |
