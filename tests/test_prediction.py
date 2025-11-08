import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from prediction.predictor import StudentPerformancePredictor
from preprocessing.data_cleaning import DataCleaner
from preprocessing.feature_selection import FeatureEngineer, create_risk_label


@pytest.fixture
def sample_training_data():
    np.random.seed(42)
    n_samples = 100
    df = pd.DataFrame({
        'student_id': range(1, n_samples + 1),
        'math_marks': np.random.randint(30, 100, n_samples),
        'science_marks': np.random.randint(30, 100, n_samples),
        'attendance': np.random.randint(50, 100, n_samples),
        'assignments_completed': np.random.randint(5, 20, n_samples),
        'total_assignments': [20] * n_samples
    })
    df['average_marks'] = df[['math_marks', 'science_marks']].mean(axis=1)
    df = create_risk_label(df, threshold=60)
    return df


def test_predictor_initialization():
    predictor = StudentPerformancePredictor(model_type='random_forest')
    assert predictor.model_type == 'random_forest'
    assert predictor.is_trained == False


def test_predictor_training(sample_training_data):
    engineer = FeatureEngineer()
    X, y = engineer.prepare_features_for_training(
        sample_training_data,
        target_column='at_risk'
    )
    predictor = StudentPerformancePredictor(model_type='random_forest')
    metrics = predictor.train(X, y, test_size=0.3)
    assert predictor.is_trained == True
    assert 'train_accuracy' in metrics
    assert 'test_accuracy' in metrics
    assert metrics['train_accuracy'] > 0
    assert metrics['test_accuracy'] > 0


def test_predictor_prediction(sample_training_data):
    engineer = FeatureEngineer()
    X, y = engineer.prepare_features_for_training(
        sample_training_data,
        target_column='at_risk'
    )
    predictor = StudentPerformancePredictor(model_type='random_forest')
    predictor.train(X, y, test_size=0.3)
    predictions, probabilities = predictor.predict(X[:10])
    assert len(predictions) == 10
    assert probabilities.shape == (10, 2)
    assert all(p in [0, 1] for p in predictions)


def test_single_student_prediction(sample_training_data):
    engineer = FeatureEngineer()
    X, y = engineer.prepare_features_for_training(
        sample_training_data,
        target_column='at_risk'
    )
    predictor = StudentPerformancePredictor(model_type='random_forest')
    predictor.train(X, y, test_size=0.3)
    student_data = X.iloc[0]
    result = predictor.predict_single_student(student_data)
    assert 'prediction' in result
    assert 'risk_probability' in result
    assert 'is_at_risk' in result
    assert isinstance(result['is_at_risk'], bool)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
