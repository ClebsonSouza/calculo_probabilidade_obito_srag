🎯 Predição de Óbito por SRAG na Paraíba com Modelos de Machine Learning
📚 Sobre o Projeto
Este projeto aplica técnicas avançadas de Machine Learning para prever o risco de óbito em pacientes internados com Síndrome Respiratória Aguda Grave (SRAG), utilizando dados reais do sistema nacional SIVEP-Gripe entre 2022 e 2024.

O objetivo principal é fornecer apoio científico à tomada de decisão clínica, permitindo identificar com maior precisão os pacientes em situação de maior risco, otimizar o uso de recursos hospitalares e subsidiar estratégias preventivas em saúde pública.

Este aplicativo foi desenvolvido a partir do estudo:

"Risco e Previsão de Desfechos por SRAG na Paraíba com Modelos de Aprendizado de Máquina"
Clébson Freire de Souza, Renato Máximo Sátiro (USP/ESALQ)

🧠 Modelos de Machine Learning Utilizados
A aplicação implementa diferentes modelos supervisionados, todos treinados, validados e comparados criteriosamente:

Regressão Logística (referência)

Decision Tree Classifier

Random Forest Classifier

XGBoost Classifier

LightGBM Classifier (modelo com melhor desempenho)

Rede Neural Artificial (exploratória)

Os algoritmos foram escolhidos para equilibrar acurácia, interpretabilidade e robustez, garantindo aplicabilidade prática no ambiente clínico.

🚀 Funcionalidades do Aplicativo
Cálculo personalizado da probabilidade de óbito baseado em variáveis clínicas e epidemiológicas.

Resultados apresentados para:

Modelo Logístico

Decision Tree

Random Forest

XGBoost

LightGBM

Interface amigável via Streamlit, acessível diretamente no navegador.

Login e autenticação para segurança e controle de acesso.

Acesse a aplicação hospedada no Streamlit Community Cloud (insira aqui o seu link quando estiver publicado!).

🏥 Aplicações Práticas
Apoio à decisão médica em unidades de saúde.

Estratificação de risco para priorização de atendimento em emergências.

Análise preditiva para planejamento de recursos hospitalares.

Ferramenta didática para ensino de machine learning aplicado à saúde pública.

Base para políticas públicas de saúde baseadas em dados.

🔬 Rigor Científico
O desenvolvimento deste projeto foi embasado em metodologias rigorosas de:

Seleção de variáveis via procedimento Stepwise;

Validação cruzada para todos os modelos;

Avaliação de desempenho usando métricas como Acurácia, Recall, F1-Score e AUC-ROC;

Interpretação de modelos complexos utilizando SHAP Values.

Além disso, os resultados foram discutidos sob a ótica da epidemiologia clínica e das desigualdades socioeconômicas que impactam os desfechos em saúde.

🛠️ Tecnologias Utilizadas
Python

Streamlit

Scikit-Learn

XGBoost

LightGBM

TensorFlow/Keras

Pandas, NumPy, PyExcel

Unidecode
