"""
Flask Backend API - Simple version
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime

from config import Config
from preprocessing.data_cleaning import DataCleaner
from preprocessing.feature_selection import create_new_features, prepare_for_training, create_risk_labels
from prediction.predictor import StudentPredictor
from prediction.explainability import explain_prediction, generate_class_summary

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)

predictor_rf = None
predictor_svm = None

def is_csv(filename):
    return filename.lower().endswith('.csv')

def load_models():
    global predictor_rf, predictor_svm
    
    rf_path = app.config['RANDOM_FOREST_MODEL']
    if os.path.exists(rf_path):
        predictor_rf = StudentPredictor('random_forest')
        predictor_rf.load_model(rf_path)
    else:
        predictor_rf = StudentPredictor('random_forest')
    
    svm_path = app.config['SVM_MODEL']
    if os.path.exists(svm_path):
        predictor_svm = StudentPredictor('svm')
        predictor_svm.load_model(svm_path)
    else:
        predictor_svm = StudentPredictor('svm')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'rf_ready': predictor_rf.is_trained if predictor_rf else False,
        'svm_ready': predictor_svm.is_trained if predictor_svm else False
    })

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if not file.filename or not is_csv(file.filename):
        return jsonify({'error': 'Need CSV file'}), 400
    
    filename = secure_filename(file.filename)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    df = pd.read_csv(filepath)
    return jsonify({
        'message': 'Uploaded',
        'filename': filename,
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': df.columns.tolist(),
        'preview': df.head(5).to_dict('records')
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    filename = data.get('filename')
    model_type = data.get('model_type', 'random_forest')
    
    if not filename:
        return jsonify({'error': 'No filename'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    predictor = predictor_rf if model_type == 'random_forest' else predictor_svm
    
    cleaner = DataCleaner()
    df = cleaner.load_csv(filepath)
    df = cleaner.add_student_ids(df)
    student_ids = df['student_id'].tolist()
    df = cleaner.clean_data(df)
    df = create_new_features(df)
    
    if not predictor.is_trained:
        df = create_risk_labels(df, threshold=50)
        X, y = prepare_for_training(df, 'at_risk')
        if y is not None and len(y.unique()) > 1:
            predictor.train(X, y)
            model_path = app.config['RANDOM_FOREST_MODEL'] if model_type == 'random_forest' else app.config['SVM_MODEL']
            predictor.save_model(model_path)
    
    X_pred, _ = prepare_for_training(df, 'at_risk')
    predictions, probabilities = predictor.predict(X_pred)
    
    results = []
    for i in range(len(predictions)):
        student_data = df.iloc[i].to_dict()
        pred = {
            'prediction': int(predictions[i]),
            'is_at_risk': bool(predictions[i] == 1),
            'risk_probability': float(probabilities[i][1])
        }
        explanation = explain_prediction(student_data, pred)
        results.append({
            'student_id': student_ids[i],
            'at_risk': 'Yes' if pred['is_at_risk'] else 'No',
            'risk_probability': round(pred['risk_probability'] * 100, 2),
            'risk_level': explanation['risk_level'],
            'explanation': explanation['explanation'],
            'risk_factors': explanation['risk_factors'],
            'recommendations': explanation['recommendations']
        })
    
    pred_list = [{'is_at_risk': r['at_risk'] == 'Yes', 'risk_probability': r['risk_probability']/100} for r in results]
    summary = generate_class_summary(pred_list, student_ids)
    
    return jsonify({
        'message': 'Complete',
        'model_used': model_type,
        'total_students': len(results),
        'at_risk_count': sum(1 for r in results if r['at_risk'] == 'Yes'),
        'at_risk_percentage': round(summary['at_risk_percentage'], 2),
        'predictions': results,
        'summary': summary
    })

@app.route('/api/train', methods=['POST'])
def train():
    data = request.json
    filename = data.get('filename')
    model_type = data.get('model_type', 'random_forest')
    
    if not filename:
        return jsonify({'error': 'No filename'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cleaner = DataCleaner()
    df = cleaner.load_csv(filepath)
    df = cleaner.clean_data(df)
    df = create_new_features(df)
    df = create_risk_labels(df, threshold=50)
    
    X, y = prepare_for_training(df, 'at_risk')
    predictor = StudentPredictor(model_type=model_type)
    metrics = predictor.train(X, y)
    
    model_path = app.config['RANDOM_FOREST_MODEL'] if model_type == 'random_forest' else app.config['SVM_MODEL']
    predictor.save_model(model_path)
    
    global predictor_rf, predictor_svm
    if model_type == 'random_forest':
        predictor_rf = predictor
    else:
        predictor_svm = predictor
    
    return jsonify({
        'message': 'Trained',
        'model_type': model_type,
        'train_accuracy': round(metrics['train_accuracy'] * 100, 2),
        'test_accuracy': round(metrics['test_accuracy'] * 100, 2)
    })

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message'}), 400
    
    try:
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from genai.chatbot import get_chatbot_response
        response = get_chatbot_response(message, student_id=None, students_data=data.get('students_data', []))
    except:
        response = simple_response(message)
    
    return jsonify({'response': response, 'timestamp': datetime.now().isoformat()})

def simple_response(message):
    msg = message.lower()
    if 'risk' in msg:
        return "Students are at-risk with low grades (below 50%), poor attendance (below 75%), low assignment completion, or declining performance."
    if 'intervention' in msg or 'help' in msg:
        return "Best interventions: tutoring, regular check-ins, parent communication, peer mentoring, study skills training."
    if 'attendance' in msg:
        return "Good attendance (75%+) is crucial. Remove barriers, communicate with parents, make classes engaging."
    if 'grade' in msg or 'mark' in msg:
        return "Improve grades with: targeted tutoring, identifying gaps, varied teaching, regular feedback, extra practice."
    if 'model' in msg or 'prediction' in msg:
        return "Uses Random Forest and SVM models with 80-90% accuracy. Analyzes grades, attendance, assignments."
    return "I can help with: why students are at-risk, interventions, improving attendance/grades, how the model works."

if __name__ == '__main__':
    load_models()
    app.run(host='0.0.0.0', port=5000, debug=False)
