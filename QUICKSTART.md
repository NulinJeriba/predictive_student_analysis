# 🚀 Quick Start Guide

## Get Started in 5 Minutes!

### Step 1: Setup (First Time Only)

Open Terminal and navigate to the project:

```bash
cd "predictive-student-performance"
```

Run the setup script (Mac/Linux):
```bash
chmod +x setup.sh
./setup.sh
```

**Or manually:**

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### Step 2: Try the Quick Demo

```bash
python3 quickstart.py
```

This will:
- Load sample student data
- Train a model (if needed)
- Make predictions
- Show at-risk students
- Display detailed analysis

### Step 3: Run the Full Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Browser:**
Open http://localhost:3000

### Step 4: Use the Application

1. **Upload CSV File**
   - Use the sample file: `backend/data/sample_data.csv`
   - Or create your own with columns: student_id, marks, attendance, etc.

2. **Run Prediction**
   - Choose Random Forest or SVM
   - Click "Run Prediction"

3. **View Results**
   - See overall statistics
   - Click on students for details
   - Get intervention recommendations

4. **Use AI Chatbot**
   - Ask questions about predictions
   - Get advice on helping students

---

## Sample CSV Format

Your CSV should have these columns (at minimum):

```csv
student_id,math_marks,science_marks,attendance,total_classes
1,85,90,95,100
2,45,50,65,100
3,75,80,88,100
```

Additional helpful columns:
- `name` - Student name
- `english_marks`, `history_marks` - More subjects
- `assignments_completed`, `total_assignments` - Assignment tracking
- `previous_marks` - Historical performance
- `class_participation` - Engagement score

---

## Troubleshooting

**"Module not found" errors:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Backend won't start:**
- Check if port 5000 is available
- Make sure you activated the virtual environment

**Can't connect to API:**
- Ensure backend is running on port 5000
- Check console for CORS errors

---

## Configuration (Optional)

Edit `.env` file for:
- OpenAI API key (for advanced chatbot)
- Model settings
- CORS origins

Copy from example:
```bash
cp .env.example .env
```

---

## Training Custom Models

Train models with your own data:

```bash
python3 train_models.py --data path/to/your/data.csv
```

---

## Project Structure

```
predictive-student-performance/
├── backend/              # Python Flask API
│   ├── app.py           # Main API server
│   ├── config.py        # Configuration
│   ├── preprocessing/   # Data cleaning
│   ├── prediction/      # ML models
│   └── data/           # Sample data
├── frontend/            # React app
│   └── src/
│       ├── App.js      # Main app
│       └── components/ # UI components
├── genai/              # AI chatbot
├── tests/              # Unit tests
├── quickstart.py       # Quick demo
├── train_models.py     # Model training
└── README.md           # Full documentation
```

---

## Next Steps

1. ✅ Run the quick demo
2. ✅ Start the full app
3. ✅ Upload sample data
4. ✅ Explore the results
5. 📖 Read full README.md
6. 🎨 Customize for your needs
7. 📊 Upload your own data
8. 🚀 Deploy to production

---

## Need Help?

- Check `README.md` for detailed documentation
- Review sample data format in `backend/data/sample_data.csv`
- Check console logs for error messages
- Ensure all dependencies are installed

---

**Built with Python, Flask, React, scikit-learn, and OpenAI** 🎓
