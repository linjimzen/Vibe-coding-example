# AI Nutrition Analysis Tool  
An AI-powered web tool that analyzes food nutrition using an LLM model via Ollama.

---

## 🚀 Features 

- Input food name + amount → Get instant nutrition estimation  
  輸入食物名稱與份量即可獲得即時營養分析

- Generates calories, protein, fat, carbs  
  自動產生熱量、蛋白質、脂肪、碳水數值

- Provides AI-generated suggestions  
  提供 AI 建議改善飲食習慣

- Visualizes nutrition data with a pie chart  
  圓餅圖可視化呈現三大營養素

- Clean, simple web UI (Flask + Chart.js)  
  使用 Flask + Chart.js 的簡潔前端介面

---

# 📦 Project Structure
```
project/
│── app.py # Flask backend + Ollama integration
│── requirements.txt # Python packages
│── static/
│ └── styles.css # Frontend CSS
│── templates/
│ └── index.html # Frontend UI
```



---
# Project Setup and Execution Guide

## 1. Ollama Installation and Model Download
### 1. Download Ollama

Please download and install Ollama from the [Ollama official website](https://ollama.com/download) according to your operating system.

Confirm successful installation:

```bash
ollama --version
```

### 2. Pull a Model

After installation, open the terminal and execute the following command to download the required model (e.g., `llama3`):

```bash
Start Ollama Service
ollama pull llama3
```

To download other models, replace `llama3` with the name of the model you need. You can find more available models in the [Ollama Library](https://ollama.com/library).

You can change the model name in `app.py`:
```python
OLLAMA_MODEL = "llama3"
```

## 2. Python Virtual Environment Setup

To avoid dependency conflicts between projects, it is highly recommended to use a Python virtual environment. Please follow the steps below:

1.  **Create virtual environment**:

    ```bash
    python -m venv venv
    ```

2.  **Activate environment**:

    *   **Windows**:

        ```bash
        .\venv\Scripts\activate
        ```

    *   **macOS / Linux**:

        ```bash
        source venv/bin/activate
        ```

## 3. Install Python Libraries

After activating the virtual environment, please execute the following command to install the libraries required for the project:

```bash
pip install -r requirement.txt
```
