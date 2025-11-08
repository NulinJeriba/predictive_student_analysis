import pandas as pd


class FeatureEngineer:
    def __init__(self):
        self.selected_features = None

    def create_new_features(self, df):
        mark_cols = [col for col in df.columns if 'mark' in col.lower() or 'score' in col.lower()]
        if len(mark_cols) > 1:
            df['average_marks'] = df[mark_cols].mean(axis=1)
            df['marks_std'] = df[mark_cols].std(axis=1)
            df['marks_min'] = df[mark_cols].min(axis=1)
            df['marks_max'] = df[mark_cols].max(axis=1)

        if 'attendance' in df.columns and 'total_classes' in df.columns:
            df['attendance_rate'] = (df['attendance'] / df['total_classes']) * 100

        if 'assignments_completed' in df.columns and 'total_assignments' in df.columns:
            df['assignment_completion_rate'] = (df['assignments_completed'] / df['total_assignments']) * 100

        if 'average_marks' in df.columns and 'previous_marks' in df.columns:
            df['marks_improvement'] = df['average_marks'] - df['previous_marks']

        return df

    def prepare_for_training(self, df, target_column='at_risk'):
        id_cols = ['student_id', 'roll_number', 'id', 'name']
        feature_df = df.copy()
        for col in id_cols:
            if col in feature_df.columns:
                feature_df = feature_df.drop(columns=[col])

        if target_column in feature_df.columns:
            y = feature_df[target_column]
            X = feature_df.drop(columns=[target_column])
        else:
            X = feature_df
            y = None

        return X, y

    def prepare_features_for_training(self, df, target_column='at_risk'):
        return self.prepare_for_training(df, target_column)


def create_risk_labels(df, threshold=50):
    if 'average_marks' in df.columns:
        df['at_risk'] = (df['average_marks'] < threshold).astype(int)
    return df


def create_risk_label(df, threshold=50):
    return create_risk_labels(df, threshold)


def prepare_for_training(df, target='at_risk'):
    return FeatureEngineer().prepare_for_training(df, target_column=target)


def create_new_features(df):
    return FeatureEngineer().create_new_features(df)
