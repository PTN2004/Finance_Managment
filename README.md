# AI Agent for Personal Finance Management

An intelligent AI-powered personal finance management system that helps users track expenses, analyze spending patterns, and receive personalized financial advice.

## Features

- 🤖 AI-powered financial advisor using LLaMA model
- 💬 Natural language conversation for expense tracking
- 📊 Automated financial analysis and reporting
- 💡 Smart budgeting and investment suggestions
- 🔔 Real-time financial alerts and notifications
- 📈 Periodic financial reports generation
- 🎯 Personalized financial goals tracking

## System Architecture

```
Client (Mobile/Web)
    |
LangChain Backend (Python)
    |
Router & Chain Engine
    |
Tools (VectorStore, Calculator, DocumentStore, API Tools)
    |
LLaMA LLM (via HuggingFace/Ollama)
    |
Database (PostgreSQL) + Redis cache
```

## Core Components

1. **AI ChatBot**
   - Natural language financial advice
   - Expense tracking through conversation
   - Financial queries and analysis

2. **Transaction Management**
   - Automatic transaction recording
   - Voice input support
   - Category classification

3. **Financial Analysis**
   - Spending pattern analysis
   - Budget tracking
   - Investment suggestions

4. **Reporting System**
   - Automated periodic reports
   - Custom report generation
   - Financial insights

## Technology Stack

- **Backend**: Python, FastAPI, LangChain
- **Database**: PostgreSQL, Redis
- **AI/ML**: LLaMA, FAISS/Chroma
- **Task Queue**: Celery
- **Frontend**: Next.js/Flutter (to be implemented)
- **Authentication**: JWT
- **Deployment**: Docker

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
4. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```
5. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Development

- Backend API documentation available at `/docs`
- Follow PEP 8 style guide for Python code
- Use conventional commits for version control

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 