# LangGraph AI Email Classifier

A beginner-friendly VS Code project using LangGraph, OpenAI, FastAPI and Streamlit.

It classifies pasted email text as `Important`, `Spam`, or `General`, routes it to a category-specific node, and creates a draft for non-spam email. It **does not connect to Gmail, send email, or delete/move messages**.

## 1. Requirements

- Python 3.10 or 3.11 recommended
- VS Code with the Python extension
- An OpenAI API key

## 2. Open in VS Code

Extract the ZIP, then open the `langgraph_email_classifier` folder in VS Code.

Open Terminal > New Terminal and run:

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation, run this once in that terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Open `.env` and replace the placeholder with your own key:

```env
OPENAI_API_KEY=your_real_key_here
OPENAI_MODEL=gpt-4o-mini
API_URL=http://localhost:8000
```

Do not share `.env` or commit it to GitHub.

## 3. Run the API

In VS Code terminal 1:

```powershell
uvicorn app.main:app --reload --port 8000
```

Check:
- Health: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

## 4. Run the Streamlit UI

Open a second VS Code terminal, activate the environment if needed, then run:

```powershell
streamlit run ui/app.py
```

The app opens at http://localhost:8501. Paste a subject and body, then click **Classify email**.

## 5. Test without the UI

Open a third terminal and run:

```powershell
curl.exe -X POST http://127.0.0.1:8000/classify `
  -H "Content-Type: application/json" `
  -d '{\"subject\":\"Client meeting tomorrow\",\"email_body\":\"Please join the client meeting tomorrow at 10 AM.\"}'
```

## 6. Run with Docker

Install Docker Desktop, create `.env` as above, then run from the project folder:

```powershell
docker compose up --build
```

Open:
- UI: http://localhost:8501
- API docs: http://localhost:8000/docs

Stop:

```powershell
docker compose down
```

## 7. Deploy to Render

1. Push this project to a **private GitHub repository** (never commit `.env`).
2. Sign in to Render and choose **New > Blueprint**.
3. Connect the repository and select `render.yaml`.
4. When prompted, enter `OPENAI_API_KEY` as a secret for the API service.
5. Deploy both services.
6. Copy the API service's public URL (for example, `https://langgraph-email-api.onrender.com`) into the UI service's `API_URL` environment variable. Include `https://`.
7. Open the UI service URL and test it.

For a public production app, do not leave the API unauthenticated. Add user authentication, rate limiting, CORS restrictions where applicable, request limits, secret rotation, monitoring, and an explicit privacy/retention policy. Restrict API access to the UI or authenticated users. Use a persistent database and audit trail before handling real mail.

## 8. Before connecting Gmail

This sample only accepts pasted text. Gmail integration is a separate feature requiring Google Cloud OAuth consent, narrowly scoped Gmail permissions, secure token storage, and review of Google's current Gmail API policies. Start with read-only access. Require human approval before sending, archiving, or deleting anything.

## Troubleshooting

- `OPENAI_API_KEY is missing`: check `.env` is in the project root and restart the API.
- `401` from OpenAI: check the API key and account billing/permissions.
- `Cannot connect to the API`: start the FastAPI server and verify `API_URL`.
- Import errors: activate `.venv` and run `pip install -r requirements.txt`.
