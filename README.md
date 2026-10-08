# Banking-Agent-POC: Personal loan recomendation System

An AI-powered loan origination and underwriting proof of concept. Built with Streamlit, Pandas, Plotly, and LangChain, the application processes loan application parameters, generates credit scores and risk ratings, recommends interest terms, compiles amortization tables, and uses Groq's `openai/gpt-oss-20b` model to generate committee summaries.

---

## Underwriting Workflow

```
Customer Input (main.py Form)
      │
      ▼
Calculate Credit Score & Risk Rating (utils.py)
      │
      ▼
Determine Loan Offer & Amortization (utils.py)
      │
      ▼
Inference: Generate Committee Summary (agent.py via Groq API)
      │
      ▼
Render Dashboard (main.py) & Compile PDF Proposal (utils.py)
```

---

## Key Features

- **Automated Credit Scoring**: Evaluates creditworthiness and risk profiles based on age, income, and debt ratios.
- **AI Loan Committee Summaries**: Uses Groq's `openai/gpt-oss-20b` model to write concise, professional loan summaries for internal bank committee reviews.
- **Amortization Engine**: Computes monthly schedules, tracking principal, interest, and remaining balances over the tenure.
- **Plotly Visualizations**: Renders interactive charts showing the reduction in loan balance over time.
- **PDF Proposal Generator**: Generates and compiles a downloadable PDF loan proposal containing complete terms and approval status.

---

## Tech Stack

- **Frontend UI**: Streamlit
- **Agentic Orchestration**: LangChain
- **Language Model**: `openai/gpt-oss-20b` (via Groq API)
- **Data Manipulation**: Pandas
- **Data Visualization**: Plotly
- **PDF Compilation**: ReportLab (via utils)
- **Development Language**: Python (v3.9+)

---

## Project Structure

```
Banking-Agent-POC/
├── main.py              # Streamlit dashboard layout and submission handler
├── agent.py             # LangChain LLaMA 3 model setup and summary prompt logic
├── utils.py             # Math engines (amortization, risk rules) and PDF compiler
├── requirements.txt     # Python dependency configuration
└── assets/              # Static assets and animation JSONs
```

---

## Setup & Running Locally

### Prerequisites
- Python 3.9 or higher
- A Groq API key

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/programmingxpert/Banking-Agent-POC.git
   cd Banking-Agent-POC
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Groq API key**
      Add your key to the local `.env` file. Do not commit that file or share its contents.

4. **Launch Application**
   ```bash
   streamlit run main.py
   ```
   *Note: Access the application in your browser at `http://localhost:8501`.*

---

## Deployment on Render

### Push the project to GitHub

Create an empty GitHub repository named `Banking-Agent-POC`. From the project directory, run the following commands (replace the remote URL with your repository URL):

```bash
git init
git add .gitignore agent.py main.py utils.py requirements.txt README.md LICENSE assets templates
git commit -m "Prepare Banking Agent for Render"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/Banking-Agent-POC.git
git push -u origin main
```

If this directory already has a Git remote, keep it and use its URL rather than adding a second `origin`. The `.env` file is ignored; never commit or push an API key.

### Create the Render Web Service

1. In Render, choose **New** > **Web Service** and connect the GitHub repository.
2. Set the runtime to **Python**.
3. Set the build command to:

      ```bash
      pip install -r requirements.txt
      ```

4. Set the start command to:

      ```bash
      streamlit run main.py --server.address 0.0.0.0 --server.port $PORT
      ```

5. In the service's **Environment** settings, add `GROQ_API_KEY` with your Groq API key as its value. Keep the key in Render's environment settings only; never commit it, include it in the README, or expose it in frontend code or screenshots.
6. Deploy the service. When the deployment is live, open the public `onrender.com` URL shown on the Render service page.

---

## Author

**Manoj Kumar**  
