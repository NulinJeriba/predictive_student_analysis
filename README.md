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

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp ../.env.example ../.env
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## 📊 Usage

### 1. Upload Student Data

- Click "Upload" or drag-and-drop a CSV file
- The system accepts files with columns like:
  - `student_id` or `roll_number`
  - Academic marks (e.g., `math_marks`, `science_marks`)
  - `attendance` and `total_classes`
  - `assignments_completed` and `total_assignments`

### 2. Run Prediction

- Select model type (Random Forest or SVM)
- Click "Run Prediction"
- View results with risk probabilities

### 3. Analyze Results

- View overall class statistics
- Click on individual students for detailed analysis
- See risk factors and recommendations

### 4. Use AI Chatbot

- Ask questions about predictions
- Get intervention recommendations
- Understand factors affecting student performance

## 🧪 Sample Data

A sample dataset is included at `backend/data/sample_data.csv` with 40 student records including:
- Subject marks (Math, Science, English, History)
- Attendance rates
- Assignment completion rates
- Previous performance data

## 🔬 Machine Learning Models

### Random Forest Classifier
- Ensemble learning method
- Handles non-linear relationships
- Provides feature importance
- Robust to outliers

### Support Vector Machine (SVM)
- Effective for binary classification
- Works well with high-dimensional data
- Kernel-based approach

### Model Training
Models automatically train on first data upload if pre-trained models don't exist. Training includes:
- Data preprocessing and feature engineering
- 80-20 train-test split
- Cross-validation (5-fold)
- Performance metrics (accuracy, precision, recall, F1-score)

## 🤖 GenAI Integration

### Chatbot Features
- Rule-based responses (fallback)
- OpenAI GPT integration (optional)
- Context-aware answers using RAG

### RAG Pipeline
- Indexes student data for quick retrieval
- Maintains educational knowledge base
- Retrieves similar cases for comparison
- Provides intervention strategies

## 📈 API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload` - Upload CSV file
- `POST /api/predict` - Run predictions
- `POST /api/train` - Train new model
- `GET /api/explain/<student_id>` - Get detailed explanation

## 🧪 Testing

Run backend tests:
```bash
cd tests
pytest -v
```

Tests cover:
- Data preprocessing
- Model training and prediction
- API endpoints
- Feature engineering

## 🔧 Configuration

Edit `backend/config.py` or `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-api-key
RISK_THRESHOLD=50
```

## 📦 Dependencies

### Backend (Python)
- Flask - Web framework
- scikit-learn - ML models
- pandas - Data manipulation
- numpy - Numerical computing
- flask-cors - CORS support
- openai - GenAI integration (optional)

### Frontend (React)
- React 18
- react-scripts
- CSS3 for styling

## 🎨 Features Highlights

### For Teachers
- Identify at-risk students early
- Get personalized intervention strategies
- Track class performance trends
- Data-driven decision making

### For Administrators
- Class-level analytics
- Resource allocation insights
- Performance tracking
- Evidence-based reporting

### For Counselors
- Student risk profiles
- Intervention planning
- Progress monitoring
- Holistic support strategies

## 🚦 Model Performance

Models typically achieve:
- **Accuracy**: 80-90%
- **Precision**: 75-85%
- **Recall**: 80-90%
- **F1-Score**: 78-87%

*Note: Performance varies based on data quality and quantity*

## 🔐 Privacy & Ethics

- Student data is processed locally
- No data is shared externally (except OpenAI API if enabled)
- Predictions are tools for human decision-making, not replacements
- Teachers should verify and contextualize predictions

## 🛠️ Troubleshooting

**Backend won't start:**
- Check Python version (3.8+)
- Verify all dependencies installed
- Check port 5000 is available

**Frontend won't connect:**
- Ensure backend is running
- Check CORS settings
- Verify API URL in fetch calls

**Predictions fail:**
- Check CSV file format
- Ensure minimum required columns
- Verify data quality (no corrupted values)

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Add new ML models

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built as a comprehensive educational AI application demonstrating:
- Machine Learning (Random Forest, SVM)
- Web Development (Flask, React)
- GenAI Integration (RAG, Chatbots)
- Data Science (pandas, scikit-learn)

## 🔮 Future Enhancements

- [ ] Add more ML models (XGBoost, Neural Networks)
- [ ] Real-time data streaming
- [ ] Mobile app version
- [ ] Advanced visualizations
- [ ] Multi-language support
- [ ] Integration with school management systems
- [ ] Automated report generation
- [ ] Parent portal

## 📞 Support

For questions or issues:
1. Check documentation
2. Review sample data format
3. Check console logs for errors
4. Verify environment setup

---

**Built with ❤️ for Education**
