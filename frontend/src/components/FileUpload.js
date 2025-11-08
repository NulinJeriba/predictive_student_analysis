import React, { useState } from 'react';
import './FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setPreview(data);
        onUploadSuccess(data);
      } else {
        setError(data.error || 'Upload failed');
      }
    } catch (err) {
      setError('Failed to connect to server: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please drop a CSV file');
    }
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Student Data</h2>
      
      <div
        className="drop-zone"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          id="file-input"
          style={{ display: 'none' }}
        />
        <label htmlFor="file-input" className="file-input-label">
          {file ? (
            <p>✓ {file.name}</p>
          ) : (
            <p>Click to select or drag and drop CSV file here</p>
          )}
        </label>
      </div>

      {error && <div className="error-message">{error}</div>}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="upload-button"
      >
        {uploading ? 'Uploading...' : 'Upload & Preview'}
      </button>

      {preview && (
        <div className="preview-section">
          <h3>File Preview</h3>
          <div className="preview-stats">
            <p><strong>Rows:</strong> {preview.rows}</p>
            <p><strong>Columns:</strong> {preview.columns}</p>
            <p><strong>Columns:</strong> {preview.column_names.join(', ')}</p>
          </div>
          
          <div className="preview-table">
            <table>
              <thead>
                <tr>
                  {preview.column_names.map((col, idx) => (
                    <th key={idx}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {preview.preview.slice(0, 5).map((row, idx) => (
                  <tr key={idx}>
                    {preview.column_names.map((col, colIdx) => (
                      <td key={colIdx}>{row[col]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
