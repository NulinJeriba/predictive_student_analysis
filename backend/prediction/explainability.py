import pandas as pd


def explain_prediction(student_data, prediction_result):
    if isinstance(student_data, pd.Series):
        student_data = student_data.to_dict()
    is_at_risk = prediction_result['is_at_risk']
    risk_probability = prediction_result['risk_probability']

    risk_factors = []
    recommendations = []

    if 'Attendance' in student_data:
        attendance = student_data['Attendance']
        if attendance < 75:
            risk_factors.append(f"Low attendance ({attendance}%)")
            recommendations.append("Improve attendance to at least 75%")

    if 'StudyHoursPerWeek' in student_data:
        study_hours = student_data['StudyHoursPerWeek']
        if study_hours < 10:
            risk_factors.append(f"Insufficient study time ({study_hours} hours/week)")
            recommendations.append("Increase study hours to at least 10 hours per week")

    if 'PreviousGrade' in student_data:
        previous_grade = student_data['PreviousGrade']
        if previous_grade < 60:
            risk_factors.append(f"Low previous grades ({previous_grade}%)")
            recommendations.append("Seek tutoring or extra help to improve grades")

    if 'AverageScore' in student_data:
        avg_score = student_data['AverageScore']
        if avg_score < 60:
            risk_factors.append(f"Low average score ({avg_score:.1f}%)")
            recommendations.append("Focus on understanding core concepts")

    if 'ParticipationRate' in student_data:
        participation = student_data['ParticipationRate']
        if participation < 50:
            risk_factors.append(f"Low class participation ({participation:.1f}%)")
            recommendations.append("Participate more actively in class discussions")

    if 'FailureRate' in student_data:
        failure_rate = student_data['FailureRate']
        if failure_rate > 30:
            risk_factors.append(f"High failure rate ({failure_rate:.1f}%)")
            recommendations.append("Focus on improving performance in failing subjects")

    if is_at_risk:
        if risk_factors:
            explanation = f"Student is at risk (confidence: {risk_probability:.1%}). Main concerns: " + ", ".join(risk_factors[:3])
        else:
            explanation = f"Student is at risk (confidence: {risk_probability:.1%}) based on overall performance patterns."
    else:
        explanation = f"Student is performing well (risk probability: {risk_probability:.1%}). Keep up the good work!"
        recommendations = ["Maintain current study habits", "Continue regular attendance"]

    return {'explanation': explanation, 'risk_factors': risk_factors, 'recommendations': recommendations, 'risk_level': 'High' if risk_probability > 0.7 else 'Medium' if risk_probability > 0.4 else 'Low'}


def generate_class_summary(predictions, student_ids=None):
    total_students = len(predictions)
    at_risk_count = sum(1 for p in predictions if p['is_at_risk'])
    avg_risk = sum(p['risk_probability'] for p in predictions) / total_students
    high_risk = sum(1 for p in predictions if p['risk_probability'] > 0.7)
    medium_risk = sum(1 for p in predictions if 0.4 < p['risk_probability'] <= 0.7)
    low_risk = total_students - high_risk - medium_risk
    summary = {'total_students': total_students, 'at_risk_count': at_risk_count, 'at_risk_percentage': (at_risk_count / total_students * 100) if total_students > 0 else 0, 'average_risk': avg_risk, 'high_risk_count': high_risk, 'medium_risk_count': medium_risk, 'low_risk_count': low_risk}
    return summary
