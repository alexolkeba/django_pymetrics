import pytest
from rest_framework.test import APIClient
from behavioral_data.models import BehavioralMetric
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestTraitInferenceAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_missing_session_id(self):
        response = self.client.post('/api/traits/trait-profiles/infer/', {})
        assert response.status_code == 400
        assert 'error' in response.data
        assert response.data['error'] == 'Missing required field: session_id.'

    def test_insufficient_data(self):
        response = self.client.post('/api/traits/trait-profiles/infer/', {'session_id': 'session_123'})
        assert response.status_code == 400
        assert 'error' in response.data
        assert 'Insufficient data completeness' in response.data['error']

    def test_successful_trait_inference(self):
        # Create 10 dummy metrics for session
        for i in range(10):
            BehavioralMetric.objects.create(session_id='session_123', metric_name=f'metric_{i}', metric_value=0.8)
        response = self.client.post('/api/traits/trait-profiles/infer/', {'session_id': 'session_123'})
        assert response.status_code == 200
        assert 'risk_tolerance' in response.data
        assert 'confidence_interval' in response.data
