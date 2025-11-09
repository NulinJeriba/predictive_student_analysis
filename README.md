# Predictive Analysis of Student Performance

An AI-powered educational application that predicts at-risk students using machine learning models and provides intelligent insights through GenAI chatbot integration.

## 🎯 Project Overview

This application helps schools and teachers identify students who might need extra academic support by analyzing historical marks, attendance, and related information. The system uses supervised machine learning (Random Forest and SVM) combined with modern GenAI tools to provide actionable insights and intervention recommendations.

## ✨ Key Features

- **CSV Data Upload**: Upload student mark sheets with academic records
- **ML Prediction Engine**: Random Forest and SVM models for risk classification
- **Real-time Analysis**: Instant predictions with confidence scores
- **Explainability**: Detailed explanations for each prediction
- **Risk Visualization**: Interactive dashboard with risk indicators
- **GenAI Chatbot**: AI assistant for answering questions and providing guidance
- **Intervention Planning**: Automated recommendations for at-risk students
- **Class-level Analytics**: Summary statistics and insights for entire classes

## 🏗️ Architecture

```
predictive-student-performance/
├── backend/              # Python Flask API
│   ├── preprocessing/    # Data cleaning and feature engineering
│   ├── prediction/       # ML models and prediction logic
│   ├── data/            # Sample data and uploads
│   └── models/          # Trained ML models
├── frontend/            # React web application
│   ├── src/
│   │   ├── components/  # React components
│   │   └── App.js       # Main application
│   └── public/
├── genai/               # GenAI chatbot and RAG pipeline
│   ├── chatbot.py       # Chatbot implementation
│   └── rag_pipeline.py  # Retrieval-Augmented Generation
└── tests/               # Unit tests
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup
````markdown
# Predictive Analysis of Student Performance

An AI-powered application to help teachers and administrators identify at-risk students by analyzing marks, attendance, and other signals. This repository contains a Flask backend (ML + API), a React frontend, and optional GenAI components for explanation and guidance.

## What you'll find here

- backend/: Flask API, preprocessing, model code, sample data and models
- frontend/: React UI and components
- genai/: Chatbot + RAG pipeline (optional OpenAI integration)
- tests/: Unit tests for preprocessing, prediction and API
- quickstart.py, train_models.py, setup.sh — helper scripts

## Key features

- Upload CSVs and run batch predictions
- Random Forest and SVM models with explainability
- Interactive dashboard with risk indicators
- GenAI chatbot (optional) for guidance and explanations
- Unit tests and example data

## Quick contract (inputs / outputs)

- Input: CSV file with at least `student_id` and academic/attendance columns
- Output: per-student risk probabilities and explanations (JSON / UI)
- Error modes: malformed CSV, missing required columns, model missing

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm (or yarn)

## Setup (recommended: one-liner)

From project root, make the setup script executable and run it (Unix/macOS):

```bash
chmod +x setup.sh
./setup.sh
```

If you prefer manual setup, follow the backend/frontend steps below.

### Backend (manual)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # then edit .env as needed
python app.py
```

Default backend URL: http://localhost:5000

### Frontend

```bash
cd frontend
npm install
npm start
```

Default frontend URL: http://localhost:3000

## Quick demo

To run the quick demo which loads sample data, trains models (if needed) and runs predictions:

```bash
python3 quickstart.py
```

## Data format (sample)

At minimum, include these columns in your CSV:

```csv
student_id,name,math_marks,science_marks,attendance,total_classes
1,John Doe,85,90,95,100
2,Jane Smith,45,50,65,100
```

Recommended extra columns: `assignments_completed`, `total_assignments`, `previous_marks`, `class_participation`.

## Common commands

- Run tests:

```bash
pytest -q
```

- Train models with your data:

```bash
python3 train_models.py --data path/to/your/data.csv
```

## API (useful endpoints)

- GET /api/health — health check
- POST /api/upload — multipart form upload (CSV)
- POST /api/predict — JSON {"filename":"<uploaded.csv>", "model_type":"random_forest"}
- POST /api/train — trigger model training
- GET /api/explain/<id> — per-student explanation

## Troubleshooting

- Port 5000 in use:

```bash
lsof -ti:5000 | xargs kill -9
```

- Backend module errors: ensure venv is activated and `pip install -r requirements.txt` ran
- Frontend dependency issues: delete `node_modules` and reinstall
- CSV upload problems: check file extension and required column headers

## Notes on privacy & ethics

- By default processing is local. If you enable OpenAI, keys must be provided in `.env` and are used by the GenAI module.
- Predictions are decision-support only. Use human judgment before acting on model output.

## Project structure (short)

```
predictive-student-performance/
├── backend/
├── frontend/
├── genai/
├── tests/
├── quickstart.py
├── train_models.py
└── setup.sh
```

## Next steps (suggested)

1. Run `./setup.sh` or follow manual setup above
2. Run `python3 quickstart.py` to validate end-to-end
3. Start the backend and frontend to use the UI
4. Add your own data and retrain models with `train_models.py`

## Contributing

Please open issues and PRs. Add tests for any behavior changes.

## License & contact

- Keep secrets (API keys) out of the repo — use `.env`
- If you want help, open an issue in this repo or contact the maintainer.

---

Short and actionable: open http://localhost:3000 after starting the frontend and use the UI to upload a CSV and run predictions.

````
