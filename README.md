<div align='center'>
  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-8991EC?style=for-the-badge&logo=scipy&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Altair](https://img.shields.io/badge/Altair-E8591E?style=for-the-badge&logo=altair&logoColor=white) ![Jupyter Notebook](https://img.shields.io/badge/Jupyter_Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white) ![Render](https://img.shields.io/badge/Render-009966?style=for-the-badge&logo=render&logoColor=white)

# 🪙 **Streamlit Coin Toss Simulator:** Law of Large Numbers

A minimal, demonstrative web application built with Python and **Streamlit**, designed to simulate the toss of an unbiased coin and illustrate the fundamental principle of the **Law of Large Numbers (LLN)**. This project is hosted on **Render's free tier**.

![cover-cut-600px](https://github.com/user-attachments/assets/7f9b3b63-76ca-4bb6-881d-4b0b736c49d5)

  <a href="https://streamlit-example-8meo.onrender.com/3" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/Try%20The%20Live%20App%20_(EN/PT)-a53825?style=for-the-badge&logo=rocket&logoColor=FFFFFF" 
        alt="View Project" 
        style="border: none; height: 35px; margin-top:20px; margin-bottom: 35px;">
  </a>

  *(Note: If the app takes a moment to load, it is because it is hosted on a free tier service and is waking up from inactivity.)*

</div>

---

## Description / Descrição

<details>
 <summary>
 <b style="font-size: 1.4em;">1. 🇺🇸 English Version</b>
 </summary>

> [![VERSÃO PT-BR](https://img.shields.io/badge/🇧🇷%20VERSÃO%20PT--BR-333?style=for-the-badge&logoColor=white)](#an%C3%A1lise-estrat%C3%A9gica-de-receita-dos-planos-da-megaline-um-estudo-comparativo-surf-x-ultimate)


### 📌 Table of Contents
1.  [Key Features](#-project-summary)
2.  [Key Findings & Business Insights](#-key-findings--business-insights)
3.  [Technical Approach & Tools](#%EF%B8%8F-technical-approach--tools)
4.  [Project Files](#-project-files)
5.  [Next Steps](#%EF%B8%8F-next-steps)

<br>

# 🪙 **Streamlit Coin Toss Simulator:** Law of Large Numbers

## 💡 What This Project Does

This experiment simulates the toss of an **unbiased coin** (probability $P=0.5$). The **Law of Large Numbers** states that the more trials you run, the closer the observed mean (proportion of Heads) will approach the theoretical expected value of $0.5$.

Use the slider to set the number of trials and click **Execute** to start the simulation and watch the proportion of Heads converge toward the expected value.

---

## ✨ Key Features

* **Statistical Simulation:** Models the random process of coin flipping based on a binomial distribution.
* **Interactive LLN Demonstration:** Uses a **Streamlit slider** for user input (number of trials) and a **button** to trigger the simulation.
* **Data Visualization:** Displays the convergence of the observed proportion of Heads toward the theoretical mean ($0.5$).
* **Deployment Experience:** Successfully deployed as a live web service on Render, showcasing practical cloud deployment skills.

---

## 💻 Local Installation and Setup

To run this application on your local machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/eduardocornelsen/coin-toss-simulator.git
cd coin-toss-simulator
```

### 2. Create and Activate a Virtual Environment (Recommended)
```Bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```Bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```Bash
streamlit run app.py
```

## ⚙️ Technologies Used

## ⚙️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language for the simulation logic. |
| **Streamlit** | Framework for creating the interactive web interface. |
| **SciPy** | Used for statistical functions and computations. |
| **Pandas** | Used for data handling and manipulation. |
| **Altair** | Used for declarative data visualization. |
| **Jupyter Notebook** | Used for initial development, prototyping, and analysis. |
| **Render** | Platform for continuous deployment and web service hosting. |

<div align='center'>
  <a href="https://streamlit-example-8meo.onrender.com/3" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/Try%20The%20Live%20App%20_(EN/PT)-a53825?style=for-the-badge&logo=rocket&logoColor=FFFFFF" 
        alt="View Project" 
        style="border: none; height: 35px; margin-top:20px; margin-bottom: 35px;">
  </a>

  *(Note: If the app takes a moment to load, it is because it is hosted on a free tier service and is waking up from inactivity.)*

</div>

</details>


***

<details>
 <summary>
 <b style="font-size: 1.4em;">2. 🇧🇷 Versão em Português - BR</b>
 </summary>
 
<br>

> [![ENGLISH VERSION](https://img.shields.io/badge/🇺🇸%20ENGLISH%20VERSION-333?style=for-the-badge&logoColor=white)](#strategic-revenue-analysis-of-megalines-mobile-plans-a-comparative-study-surf-x-ultimate)

### 📌 Índice
1.  [Resumo do Projeto](#-resumo-do-projeto)
2.  [Principais Descobertas e Insights de Negócio](#-principais-descobertas-e-insights-de-neg%C3%B3cio)
3.  [Abordagem Técnica e Ferramentas](#%EF%B8%8F-abordagem-t%C3%A9cnica-e-ferramentas)
4.  [Arquivos do Projeto](#-arquivos-do-projeto)
5.  [Próximos Passos](#%EF%B8%8F-pr%C3%B3ximos-passos)

<br>

# 🪙 Simulador de Lançamento de Moeda com Streamlit: Lei dos Grandes Números

## 💡 O Que Esse Projeto Faz

Este experimento simula o lançamento de uma moeda imparcial (probabilidade $P=0.5$). A Lei dos Grandes Números (LGN) afirma que, quanto mais testes você realiza, mais próxima a média observada (proporção de 'Caras') se aproximará do valor esperado teórico de $0.5$.

Use o controle deslizante (slider) para definir o número de testes e clique em Executar para iniciar a simulação e observar a proporção de 'Caras' convergir para o valor esperado.

---

## Principais Funcionalidades

- **Simulação Estatística:** Modela o processo aleatório de lançamento de moeda com base em uma distribuição binomial.
- **Demonstração Interativa da LGN:** Utiliza um slider do Streamlit para entrada do usuário (número de testes) e um botão para iniciar a simulação.
- **Visualização de Dados:** Exibe a convergência da proporção observada de 'Caras' em direção à média teórica ($0.5$).
- **Experiência de Implantação:** Implantado com sucesso como um serviço web ativo no Render, demonstrando habilidades práticas de implantação na nuvem.

---

## Instalação e Configuração Local

Para executar esta aplicação em sua máquina local, siga estes passos:

### 1. Clone o Repositório
```
git clone https://github.com/eduardocornelsen/coin-toss-simulator.git
cd coin-toss-simulator
```

### 2. Crie e Ative um Ambiente Virtual (Recomendado)
```
python -m venv venv
source ven/bin/activate  # No Windows, use `venv\Scripts\activate`
```

### 3. Instale as Dependências
```
pip install -r requirements.txt
```

### 4. Execute o App Streamlit
```
streamlit run app.py
```


<div align='center'>
  <a href="https://streamlit-example-8meo.onrender.com/3" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/Teste%20o%20App%20ao%20Vivo%20_(EN/PT)-a53825?style=for-the-badge&logo=rocket&logoColor=FFFFFF" 
        alt="View Project" 
        style="border: none; height: 35px; margin-top:20px; margin-bottom: 35px;">
  </a>

  *(Note: If the app takes a moment to load, it is because it is hosted on a free tier service and is waking up from inactivity.)*

</div>

</details>

<p align="center">
Copyright © 2025, Eduardo Cornelsen
</p>
