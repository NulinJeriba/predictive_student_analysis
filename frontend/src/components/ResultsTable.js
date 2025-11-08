import React, { useState } from 'react';
import './ResultsTable.css';

const ResultsTable = ({ filename, onPredictionComplete }) => {
  const [predicting, setPredicting] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [modelType, setModelType] = useState('random_forest');
  const [selectedStudent, setSelectedStudent] = useState(null);

  const handlePredict = async () => {
    setPredicting(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filename: filename,
          model_type: modelType,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResults(data);
        onPredictionComplete(data);
      } else {
        setError(data.error || 'Prediction failed');
      }
    } catch (err) {
      setError('Failed to connect to server: ' + err.message);
    } finally {
      setPredicting(false);
    }
  };

  const getRiskColor = (probability) => {
    if (probability >= 70) return '#f44336';
    if (probability >= 50) return '#ff9800';
    if (probability >= 30) return '#ffc107';
    return '#4CAF50';
  };

  const showStudentDetails = (student) => {
    setSelectedStudent(student);
  };

  return (
    <div className="results-container">
      <div className="prediction-controls">
        <h2>Run Prediction</h2>
        
        <div className="model-selector">
          <label>
            <input
              type="radio"
              value="random_forest"
              checked={modelType === 'random_forest'}
              onChange={(e) => setModelType(e.target.value)}
            />
            Random Forest
          </label>
          <label>
            <input
              type="radio"
              value="svm"
              checked={modelType === 'svm'}
              onChange={(e) => setModelType(e.target.value)}
            />
            SVM
          </label>
        </div>

        <button
          onClick={handlePredict}
          disabled={!filename || predicting}
          className="predict-button"
        >
          {predicting ? 'Analyzing...' : 'Run Prediction'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {results && (
        <div className="results-display">
          <div className="summary-cards">
            <div className="summary-card">
              <h3>{results.total_students}</h3>
              <p>Total Students</p>
            </div>
            <div className="summary-card risk">
              <h3>{results.at_risk_count}</h3>
              <p>At Risk</p>
            </div>
            <div className="summary-card percentage">
              <h3>{results.at_risk_percentage}%</h3>
              <p>Risk Percentage</p>
            </div>
          </div>

          <h3>Student Predictions</h3>
          <div className="results-table">
            <table>
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Status</th>
                  <th>Risk Probability</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {results.predictions.map((student, idx) => (
                  <tr key={idx} className={student.at_risk === 'Yes' ? 'at-risk-row' : ''}>
                    <td>{student.student_id}</td>
                    <td>
                      <span className={`status-badge ${student.at_risk === 'Yes' ? 'risk' : 'safe'}`}>
                        {student.at_risk === 'Yes' ? '⚠️ At Risk' : '✓ Safe'}
                      </span>
                    </td>
                    <td>
                      <div className="probability-bar">
                        <div
                          className="probability-fill"
                          style={{
                            width: `${student.risk_probability}%`,
                            backgroundColor: getRiskColor(student.risk_probability)
                          }}
                        />
                        <span className="probability-text">{student.risk_probability}%</span>
                      </div>
                    </td>
                    <td>
                      <button
                        className="details-button"
                        onClick={() => showStudentDetails(student)}
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selectedStudent && (
            <div className="student-details-modal" onClick={() => setSelectedStudent(null)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="close-button" onClick={() => setSelectedStudent(null)}>×</button>
                <h3>Student {selectedStudent.student_id} - Detailed Analysis</h3>
                
                <div className="detail-section">
                  <h4>Risk Assessment</h4>
                  <p><strong>Status:</strong> {selectedStudent.at_risk === 'Yes' ? '⚠️ At Risk' : '✓ Not at Risk'}</p>
                  <p><strong>Risk Probability:</strong> {selectedStudent.risk_probability}%</p>
                </div>

                {selectedStudent.explanation && (
                  <>
                    {selectedStudent.explanation.risk_factors && selectedStudent.explanation.risk_factors.length > 0 && (
                      <div className="detail-section risk-factors">
                        <h4>Risk Factors</h4>
                        <ul>
                          {selectedStudent.explanation.risk_factors.map((factor, idx) => (
                            <li key={idx}>{factor}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {selectedStudent.explanation.strengths && selectedStudent.explanation.strengths.length > 0 && (
                      <div className="detail-section strengths">
                        <h4>Strengths</h4>
                        <ul>
                          {selectedStudent.explanation.strengths.map((strength, idx) => (
                            <li key={idx}>{strength}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {selectedStudent.explanation.recommendations && selectedStudent.explanation.recommendations.length > 0 && (
                      <div className="detail-section recommendations">
                        <h4>Recommended Actions</h4>
                        <ul>
                          {selectedStudent.explanation.recommendations.map((rec, idx) => (
                            <li key={idx}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResultsTable;
