# Observatório - Análise de Mulheres no Lattes

Este repositório contém a estruturação de dados e os scripts utilizados para analisar a presença e a evolução de pesquisadoras na plataforma Lattes ao longo dos anos (2020 a 2025).

## 📂 Estrutura do Projeto

A organização dos ficheiros segue uma estrutura padrão de análise de dados:

- **`data/raw/`**: Contém os ficheiros brutos extraídos do Lattes (`lattes_2020.csv` até `lattes_2025.csv`).
- **`data/processed/`**: Armazena a base de dados tratada e consolidada (`dados_mulheres_lattes.csv`), pronta para o cruzamento de informações.
- **`notebooks/`**: Diretório onde ficam as análises exploratórias. O ficheiro principal é o `01_analise_mulheres_lattes.ipynb`, que contém o código em Python, o tratamento dos dados e as visualizações.

## 🛠️ Tecnologias Utilizadas

- **Python** (Análise e processamento de dados)
- **Jupyter Notebook** (Ambiente de desenvolvimento)
- **Bibliotecas de Dados** (Pandas, Matplotlib/Seaborn)

## 🚀 Como Executar

1. Clone este repositório na sua máquina local.
2. Certifique-se de ter o Python e o Jupyter Notebook instalados no seu ambiente.
3. (Opcional) Crie um ambiente virtual e instale as dependências necessárias.
4. Abra o diretório `notebooks/` e execute o ficheiro `01_analise_mulheres_lattes.ipynb` para visualizar o passo a passo da análise.
