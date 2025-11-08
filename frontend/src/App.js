import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultsTable from './components/ResultsTable';
import Chatbot from './components/Chatbot';
import './App.css';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [predictionResults, setPredictionResults] = useState(null);

  const handleUploadSuccess = (fileData) => {
    setUploadedFile(fileData);
    setPredictionResults(null);
  };

  const handlePredictionComplete = (results) => {
    setPredictionResults(results);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📚 Student Performance Predictor</h1>
        <p>AI-Powered Early Warning System for At-Risk Students</p>
      </header>

      <main className="App-main">
        <div className="workflow-section">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Data</h3>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Run Prediction</h3>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>View Results</h3>
          </div>
        </div>

        <section className="upload-section">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </section>

        {uploadedFile && (
          <section className="prediction-section">
            <ResultsTable 
              filename={uploadedFile.filename}
              onPredictionComplete={handlePredictionComplete}
            />
          </section>
        )}


      </main>

      <footer className="App-footer">
        <p>Predictive Analysis of Student Performance | Built with ML & GenAI</p>
        <p>Models: Random Forest & SVM | Powered by Python, Flask, React</p>
      </footer>

      {/* Floating Chatbot - only visible when predictions are available */}
      {predictionResults && (
        <Chatbot predictionResults={predictionResults} />
      )}
    </div>
  );
}

export default App;
