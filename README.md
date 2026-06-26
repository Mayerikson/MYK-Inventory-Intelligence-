# MYK Inventory Intelligence

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/)

Plataforma de **Supply Chain Analytics** desenvolvida sob o paradigma local-first para otimização estocástica de estoques, mitigando rupturas e reduzindo o capital imobilizado.

##  Link do Dashboard em Nuvem
O painel executivo interativo com as sugestões automáticas de compra foi implantado e está disponível publicamente em:
➔ **[(https://myksca.streamlit.app/)]**

##  Visão Executiva e Impacto de Negócio
A automação baseada em dados substitui o planejamento de compras reativo da rede MYK, entregando:
* **Capital de Giro Liberado:** R$ 6.500.000,00 (Redução do inventário ocioso)
* **Economia Operacional (Opex):** Redução de R$ 1.625.000,00/ano no custo de carregamento.
* **Margem de Contribuição Recuperada:** + R$ 3.072.000,00 pelo fim das quebras de gôndola.
* **Retorno sobre o Investimento (ROI):** **682%** no primeiro ano.

##  Origem e Governança dos Dados (Data Sourcing)
Para garantir a reprodutibilidade e conformidade do ecossistema analítico, os dados históricos de transações e séries temporais foram extraídos de repositórios públicos de referência em Supply Chain:
* **Base de Dados Primária:** Desafio Histórico de Vendas de Itens de Varejo ([Disponível publicamente no Kaggle](https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data)).
* **Volumetria:** ~913.000 registros transacionais cobrindo o histórico diário de 50 produtos em 10 lojas ao longo de 5 anos.
* **Ingestão:** Os dados brutos são processados via pipeline local-first utilizando `Polars` e armazenados de forma estruturada e compactada no banco de dados analítico integrado `DuckDB`.

##  Stack Tecnológica e Modelagem
* **Dados:** `Polars` para manipulação vetorizada em Rust e `DuckDB` como storage OLAP em formato Apache Arrow.
* **Machine Learning:** `LightGBM` para forecasting diário e `Gaussian Mixture Models (GMM)` para Curva ABC probabilística.
* **Estatística Avançada:** `Hidden Markov Models (HMM)` via algoritmo de Viterbi para detecção precoce de regimes latentes de demanda.
* **MLOps:** `MLflow` para governança de artefatos e `Papermill` para orquestração batch parametrizada.

---
