import os
import sys
import pandas as pd

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from preprocessing.data_cleaning import DataCleaner, validate_student_data
from preprocessing.feature_selection import FeatureEngineer, create_risk_label
from prediction.predictor import StudentPerformancePredictor
from prediction.explainability import PredictionExplainer
from config import Config


def quick_start():
    data_path = 'backend/data/sample_data.csv'
    cleaner = DataCleaner()
    df = cleaner.load_csv(data_path)
    df = validate_student_data(df)
    df_cleaned = cleaner.clean_pipeline(df.copy(), remove_outliers_flag=False, normalize_flag=False)

    engineer = FeatureEngineer()
    df_features = engineer.create_derived_features(df_cleaned)
    df_features = create_risk_label(df_features, threshold=50)

    rf_model_path = Config.RANDOM_FOREST_MODEL
    if not os.path.exists(rf_model_path):
        X, y = engineer.prepare_features_for_training(df_features, target_column='at_risk')
        predictor = StudentPerformancePredictor(model_type='random_forest')
        metrics = predictor.train(X, y)
        os.makedirs(os.path.dirname(rf_model_path), exist_ok=True)
        predictor.save_model(rf_model_path)
    else:
        predictor = StudentPerformancePredictor(model_type='random_forest')
        predictor.load_model(rf_model_path)

    X, _ = engineer.prepare_features_for_training(df_features, target_column='at_risk')
    predictions, probabilities = predictor.predict(X)

    df_results = df.copy()
    df_results['prediction'] = predictions
    df_results['risk_probability'] = (probabilities[:, 1] * 100).round(2)
    df_results['at_risk'] = df_results['prediction'].map({0: 'No', 1: 'Yes'})

    at_risk_students = df_results[df_results['at_risk'] == 'Yes'].copy()
    if len(at_risk_students) > 0:
        sample_idx = at_risk_students.index[0]
        sample_student = df_features.loc[sample_idx].to_dict()
        explainer = PredictionExplainer(predictor)
        prediction_result = {
            'is_at_risk': True,
            'risk_probability': probabilities[sample_idx, 1],
            'safe_probability': probabilities[sample_idx, 0]
        }
        explanation = explainer.explain_prediction(sample_student, prediction_result)
        return {
            'results': df_results,
            'explanation': explanation
        }
    return {'results': df_results}


if __name__ == '__main__':
    quick_start()
