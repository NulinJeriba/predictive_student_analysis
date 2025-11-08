import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


class DataCleaner:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}

    def load_csv(self, file_path):
        df = pd.read_csv(file_path)
        return df

    def handle_missing_values(self, df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)

        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)

        return df

    def encode_text_to_numbers(self, df):
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        for col in text_cols:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
        return df

    def clean_data(self, df):
        df = self.handle_missing_values(df)
        df = self.encode_text_to_numbers(df)
        return df

    def encode_categorical_features(self, df):
        return self.encode_text_to_numbers(df)

    def clean_pipeline(self, df, remove_outliers_flag=True, normalize_flag=True):
        df = self.handle_missing_values(df)
        df = self.encode_text_to_numbers(df)
        if normalize_flag:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        return df

    def add_student_ids(self, df):
        return add_student_ids(df)


def add_student_ids(df):
    if 'student_id' not in df.columns and 'roll_number' not in df.columns and 'id' not in df.columns:
        df.insert(0, 'student_id', range(1, len(df) + 1))
    return df


def validate_student_data(df):
    return add_student_ids(df)
