import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib
import os


class StudentPredictor:
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = None
        self.feature_names = None
        self.is_trained = False

    def create_model(self):
        if self.model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        else:
            self.model = SVC(kernel='rbf', probability=True, random_state=42)

    def train(self, X, y, test_size=0.2, random_state=42):
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values
        if hasattr(y, 'values'):
            y = y.values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.create_model()
        self.model.fit(X_train, y_train)

        train_accuracy = self.model.score(X_train, y_train)
        test_accuracy = self.model.score(X_test, y_test)
        self.is_trained = True

        return {'train_accuracy': train_accuracy, 'test_accuracy': test_accuracy}

    def predict(self, X):
        if not self.is_trained and self.model is None:
            raise Exception('Model not trained')
        if isinstance(X, pd.DataFrame):
            # Ensure columns match the feature names used during training.
            if self.feature_names:
                # add any missing columns with default 0, drop extra columns and order correctly
                missing = [c for c in self.feature_names if c not in X.columns]
                for c in missing:
                    X[c] = 0
                # Reorder / select columns to match training order
                X = X[self.feature_names]
            else:
                # Fallback: if feature names are not available but the underlying model
                # expects a fixed number of features, try to align the DataFrame by
                # trimming or padding columns to match model.n_features_in_.
                if hasattr(self.model, 'n_features_in_'):
                    expected = int(self.model.n_features_in_)
                    if X.shape[1] > expected:
                        # Drop the extra columns (prefer dropping newly engineered columns at the end)
                        X = X.iloc[:, :expected]
                    elif X.shape[1] < expected:
                        # Add zero-filled columns to match expected count
                        for i in range(expected - X.shape[1]):
                            X[f'_pad_{i}'] = 0
            X = X.values
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        return predictions, probabilities

    def predict_single_student(self, student_data):
        import pandas as _pd
        if isinstance(student_data, dict):
            student_data = _pd.DataFrame([student_data])
        elif hasattr(student_data, 'to_frame'):
            student_data = student_data.to_frame().T
        prediction, probability = self.predict(student_data)
        return {'prediction': int(prediction[0]), 'risk_probability': float(probability[0][1]), 'is_at_risk': bool(prediction[0] == 1)}

    def save_model(self, file_path):
        if not self.is_trained:
            raise Exception('Cannot save untrained model')
        model_data = {'model': self.model, 'model_type': self.model_type, 'feature_names': self.feature_names, 'is_trained': self.is_trained}
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(model_data, file_path)

    def load_model(self, file_path):
        if not os.path.exists(file_path):
            raise Exception(f'Model file not found: {file_path}')
        model_data = joblib.load(file_path)
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.feature_names = model_data.get('feature_names')
        self.is_trained = model_data.get('is_trained', False)

    def get_feature_importance(self):
        if self.model_type == 'random_forest' and self.is_trained:
            importance = self.model.feature_importances_
            if self.feature_names:
                import pandas as _pd
                return _pd.DataFrame({'feature': self.feature_names, 'importance': importance}).sort_values('importance', ascending=False)
            return importance
        return None


# Backwards-compatible alias for older code/tests
StudentPerformancePredictor = StudentPredictor
