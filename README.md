# MYK Inventory Intelligence

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Plataforma de **Supply Chain Analytics** desenvolvida sob o paradigma local-first para otimização  de estoques, mitigando rupturas e reduzindo o capital imobilizado.

##  Visão Executiva e Impacto de Negócio
A automação baseada em dados substitui o planejamento de compras reativo da rede MYK, entregando:
* **Capital de Giro Liberado:** R$ 6.500.000,00 (Redução do inventário ocioso)
* **Economia Operacional (Opex):** Redução de R$ 1.625.000,00/ano no custo de carregamento.
* **Margem de Contribuição Recuperada:** + R$ 3.072.000,00 pelo fim das quebras de gôndola.
* **Retorno sobre o Investimento (ROI):** **682%** no primeiro ano.

##  Stack Tecnológica e Modelagem
* **Dados:** `Polars` para manipulação vetorizada em Rust e `DuckDB` como storage OLAP em formato Apache Arrow.
* **Machine Learning:** `LightGBM` para forecasting diário e `Gaussian Mixture Models (GMM)` para Curva ABC probabilística.
* **Estatística Avançada:** `Hidden Markov Models (HMM)` via algoritmo de Viterbi para detecção precoce de regimes latentes de demanda.
* **MLOps:** `MLflow` para governança de artefatos e `Papermill` para orquestração batch parametrizada.

---
