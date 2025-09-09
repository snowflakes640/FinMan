# FinMan

FinMan is an intelligent personal finance management application that leverages cutting-edge AI to help users track, analyze, and optimize their financial activities. It features a modern web frontend, a robust Python backend API, and seamless integration with Google Gemini AI for smart transaction classification and insights.

## Features
- **Conversational Finance Tracking:** Add income and expense entries using natural language commands (e.g., "salary 8000").
- **AI-Powered Categorization:** Automatically classifies transactions and detects ambiguities, asking for clarification when needed.
- **Real-Time Balance & Reports:** Instantly view your current balance, detailed income/expense breakdowns, and insightful financial reports.
- **Modern Web UI:** Responsive, user-friendly interface with tabbed navigation for expenses, incomes, and reports.

---

## Architecture Overview

### 1. Frontend (finman.html)
- **Built with HTML, CSS, and JavaScript**
- Interactive chat interface for entering transactions and viewing responses
- Tabbed sidebar for quick access to balance, income, expense, and report views
- Fetches data and interacts with backend via RESTful API endpoints

### 2. Backend API (finmanAPI.py)
- **Python FastAPI (recommended) or Flask**
- Exposes endpoints for:
  - `/chat` — Handles chat messages and returns AI-processed responses
  - `/incomes` — Returns all income entries
  - `/expenses` — Returns all expense entries
  - `/balance` — Returns current balance
- Reads and writes to a local JSON database (`finman.json`)

### 3. AI Engine (finmanAI2.py)
- **Powered by Google Gemini (via google-genai)**
- Processes user commands, classifies transaction type and category
- Handles ambiguities and generates clarifying questions
- Produces structured responses for frontend consumption
- Generates personalized financial reports and insights

---

## Getting Started

1. **Clone the repository**
2. **Install dependencies:**
   - Python packages: `google-genai`, `pydantic`, `python-dotenv`, `Flask`
   - Frontend: No build step required
3. **Set up Google Gemini API credentials** in a `.env` file
4. **Run the backend server:**
   ```powershell
   python finmanAPI.py
   ```
5. **Open `finman.html` in your browser**

---

## Use Cases & Benefits
- **Effortless Tracking:** Log transactions with simple chat commands—no manual categorization needed
- **Smart Insights:** Get instant, AI-generated reports and recommendations to improve your financial health
- **Clarity & Control:** The app asks for clarification when entries are ambiguous, ensuring accurate records
- **Privacy-First:** All data is stored locally in `finman.json`—no cloud required

---

