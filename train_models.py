import os
import sys
import pandas as pd
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from preprocessing.data_cleaning import DataCleaner, validate_student_data
from preprocessing.feature_selection import FeatureEngineer, create_risk_label
from prediction.predictor import StudentPerformancePredictor
from config import Config


def train_models(data_path='backend/data/sample_data.csv'):
    cleaner = DataCleaner()
    df = cleaner.load_csv(data_path)
    df = validate_student_data(df)
    df_cleaned = cleaner.clean_pipeline(df.copy(), remove_outliers_flag=False, normalize_flag=False)
    engineer = FeatureEngineer()
    df_features = engineer.create_derived_features(df_cleaned)
    df_features = create_risk_label(df_features, threshold=Config.RISK_THRESHOLD)
    X, y = engineer.prepare_features_for_training(df_features, target_column='at_risk')

    predictor_rf = StudentPerformancePredictor(model_type='random_forest')
    metrics_rf = predictor_rf.train(X, y)
    rf_path = Config.RANDOM_FOREST_MODEL
    predictor_rf.save_model(rf_path)

    predictor_svm = StudentPerformancePredictor(model_type='svm')
    metrics_svm = predictor_svm.train(X, y)
    svm_path = Config.SVM_MODEL
    predictor_svm.save_model(svm_path)

    feature_importance = predictor_rf.get_feature_importance()
    return {
        'rf_metrics': metrics_rf,
        'svm_metrics': metrics_svm,
        'feature_importance': feature_importance
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='backend/data/sample_data.csv')
    args = parser.parse_args()
    train_models(args.data)
