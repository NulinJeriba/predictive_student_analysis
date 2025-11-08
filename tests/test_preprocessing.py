import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from preprocessing.data_cleaning import DataCleaner, validate_student_data


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5],
        'math_marks': [85, 65, np.nan, 45, 75],
        'science_marks': [90, 70, 55, np.nan, 80],
        'attendance': [95, 80, 65, 50, 88],
        'gender': ['M', 'F', 'M', None, 'F']
    })


def test_data_cleaner_initialization():
    cleaner = DataCleaner()
    assert cleaner is not None
    assert cleaner.scaler is not None
    assert isinstance(cleaner.label_encoders, dict)


def test_handle_missing_values(sample_data):
    cleaner = DataCleaner()
    df_cleaned = cleaner.handle_missing_values(sample_data.copy())
    assert df_cleaned.isnull().sum().sum() == 0
    assert df_cleaned['math_marks'].notna().all()
    assert df_cleaned['science_marks'].notna().all()


def test_encode_categorical_features(sample_data):
    cleaner = DataCleaner()
    df_cleaned = cleaner.handle_missing_values(sample_data.copy())
    df_encoded = cleaner.encode_categorical_features(df_cleaned)
    assert pd.api.types.is_numeric_dtype(df_encoded['gender'])


def test_validate_student_data():
    df_no_id = pd.DataFrame({
        'marks': [85, 90, 75],
        'attendance': [95, 88, 92]
    })
    df_validated = validate_student_data(df_no_id)
    assert 'student_id' in df_validated.columns


def test_clean_pipeline(sample_data):
    cleaner = DataCleaner()
    df_cleaned = cleaner.clean_pipeline(sample_data.copy(), normalize_flag=False)
    assert df_cleaned.isnull().sum().sum() == 0
    for col in df_cleaned.columns:
        assert pd.api.types.is_numeric_dtype(df_cleaned[col])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
