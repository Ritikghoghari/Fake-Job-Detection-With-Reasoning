# 🛡️ Fake Job Description Detection System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/Demo-Click%20Here-green?style=flat&logo=streamlit)](https://fake-job-detection.streamlit.app/)

## 🚀 Overview
**Fake Job Detection** is an advanced AI-powered system designed to analyze job postings and determine their authenticity. By combining traditional Machine Learning (LightGBM) with modern Large Language Models (GPT-4o), web verification, and integrity checks, this tool provides a robust defense against job scams, phishing attempts, and modified/tampered job listings.

The application features a modern, responsive **Streamlit** interface that gives users detailed insights into *why* a posting might be fake.

## ✨ Key Features

### 🧠 Multi-Layer Analysis
*   **ML Probability Model**: Uses TF-IDF and LightGBM to calculate a baseline scam probability.
*   **AI Reasoning Engine**: Leverages OpenAI's **GPT-4o-mini** to provide human-readable explanations and a realism score.
*   **Web Verification**: Automatically searches the web to verify if the company exists and if the job listing is consistent with their known presence.
*   **Email Logic Check**: Validates email addresses found in the text for domain reputation and format.
*   **Integrity & Tamper Detection**: novel feature that detects if a legitimate job posting from a big brand (e.g., Amazon, Google) has been subtley modified by a scammer.

### 📊 Comprehensive Dashboard
*   **Real-time Scoring**: View "Scam Probability", "Realism Score", and "Tamper Score" at a glance.
*   **Visual Indicators**: Color-coded badges (e.g., `✅ LIKELY REAL`, `🚨 SCAM DETECTED`, `⚠️ MODIFIED`) for immediate feedback.
*   **Suspicious Keyword Highlighting**: Automatically extracts and displays phrases commonly used in fraudulent listings.

## 🛠️ Tech Stack
*   **Frontend**: [Streamlit](https://streamlit.io/) (Custom CSS styled)
*   **Machine Learning**: `scikit-learn`, `lightgbm`, `joblib`
*   **Deep Learning**: `sentence-transformers` (all-MiniLM-L6-v2) for embeddings.
*   **LLM Integration**: `openai` (GPT-4o-mini)
*   **Language**: Python 3.11+

## 📥 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Ritikghoghari/Fake-Job-Detection-With-Reasoning.git
    cd Fake-Job-Detection-With-Reasoning
    ```

2.  **Install Dependencies**
    It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_sk_key_here
    ```

## ▶️ Usage

Run the Streamlit application locally:

```bash
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`. Simply paste a job description into the text area and click **Analyze Posting**.

## 📂 Project Structure

```text
.
├── data/                  # Raw and processed datasets
├── model_artifacts/       # Saved LightGBM models, TF-IDF vectorizers
├── src/
│   ├── app.py             # Main Streamlit application entry point
│   ├── predict_utils.py   # Core prediction logic & pipelining
│   ├── explain_with_openai.py # GPT-4 integration
│   ├── web_verification.py# Web search & verification logic
│   └── styles.py          # Custom CSS for UI
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
