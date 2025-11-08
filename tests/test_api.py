import pytest
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'


def test_upload_no_file(client):
    response = client.post('/api/upload')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_upload_with_file(client, tmp_path):
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text("student_id,marks\n1,85\n2,65\n3,75\n")
    with open(csv_file, 'rb') as f:
        response = client.post(
            '/api/upload',
            data={'file': (f, 'test_data.csv')},
            content_type='multipart/form-data'
        )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'filename' in data
    assert 'rows' in data


def test_predict_no_filename(client):
    response = client.post(
        '/api/predict',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
