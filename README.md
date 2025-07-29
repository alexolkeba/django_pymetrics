# Django Pymetrics Agentic Framework

A comprehensive Django application for neuroscience-based behavioral data collection, granular event logging, and psychometric trait inference. This system implements a modular agentic architecture for robust, scalable behavioral analytics aligned with Pymetrics standards.

## 🎯 Overview

The Django Pymetrics Agentic Framework provides:

- **Granular Behavioral Data Collection**: Real-time capture of all user interactions in neuroscience-based games
- **Scientific Metric Extraction**: Aggregation of raw events into scientifically valid metrics
- **Trait Inference Engine**: Multi-dimensional psychometric trait assessment using documented logic
- **Agentic Architecture**: Modular agents for EventLogger, MetricExtractor, TraitInferencer, and ReportGenerator
- **Production-Ready Infrastructure**: Celery task queues, REST APIs, and comprehensive testing

## 🏗️ Architecture

### Core Components

```
django_pymetrics/
├── agents/                     # Agentic framework
│   ├── base_agent.py          # Base agent class with common functionality
│   ├── event_logger.py        # EventLogger agent for real-time data capture
│   ├── metric_extractor.py    # MetricExtractor agent (to be implemented)
│   ├── trait_inferencer.py    # TraitInferencer agent (to be implemented)
│   └── report_generator.py    # ReportGenerator agent (to be implemented)
├── behavioral_data/           # Behavioral data models and validation
│   ├── models.py              # Comprehensive behavioral data models
│   ├── schemas.py             # Data validation schemas
│   └── validators.py          # Scientific data validation
├── tasks/                     # Celery background tasks
│   ├── event_processing.py    # Event processing tasks
│   ├── metric_extraction.py   # Metric extraction tasks (to be implemented)
│   ├── trait_inference.py     # Trait inference tasks (to be implemented)
│   └── reporting.py           # Reporting tasks (to be implemented)
├── api/                       # REST API endpoints (to be implemented)
├── trait_mapping/             # Trait mapping logic (to be implemented)
├── tests/                     # Comprehensive test suite (to be implemented)
└── config/                    # Configuration management (to be implemented)
```

### Behavioral Data Models

The system implements comprehensive models for capturing granular behavioral data:

- **BehavioralSession**: Session-level metadata and tracking
- **BehavioralEvent**: Base model for all behavioral events
- **BalloonRiskEvent**: Specific events for balloon risk game
- **MemoryCardsEvent**: Specific events for memory cards game
- **ReactionTimerEvent**: Specific events for reaction timer game
- **BehavioralMetric**: Aggregated metrics for scientific analysis

### Agentic Framework

The system uses a modular agentic architecture:

1. **EventLogger Agent**: Captures and validates real-time behavioral events
2. **MetricExtractor Agent**: Aggregates raw events into scientific metrics
3. **TraitInferencer Agent**: Maps metrics to psychometric traits
4. **ReportGenerator Agent**: Creates reports and dashboards

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis (for Celery task queue)
- PostgreSQL (optional, SQLite for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_pymetrics
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Redis server**
   ```bash
   redis-server
   ```

8. **Start Celery worker**
   ```bash
   celery -A pymetric worker -l info
   ```

9. **Start Celery beat (for scheduled tasks)**
   ```bash
   celery -A pymetric beat -l info
   ```

10. **Run development server**
    ```bash
    python manage.py runserver
    ```

## 📊 Behavioral Data Collection

### Event Logging

The system captures granular behavioral events with millisecond precision:

```python
# Example: Logging a balloon pump event
from agents.event_logger import EventLogger

event_logger = EventLogger()

event_data = {
    'session_id': 'session_123',
    'event_type': 'balloon_risk',
    'event_data': {
        'balloon_id': 'balloon_1',
        'pump_number': 5,
        'timestamp_milliseconds': 1640995200000,
        'balloon_size': 1.2,
        'current_earnings': 0.25,
        'total_earnings': 1.50,
        'time_since_prev_pump': 1500,
        'is_new_personal_max': True,
        'is_rapid_pump': False
    }
}

result = event_logger.run(event_data)
```

### Data Validation

All behavioral data is validated using scientific schemas:

```python
from behavioral_data.schemas import BalloonRiskSchema

schema = BalloonRiskSchema()
validated_data = schema.validate_pump_event(event_data)
```

## 🔬 Scientific Validation

### Trait Mapping

The system implements scientifically validated trait mapping:

- **Risk Tolerance**: Based on average pumps per balloon and risk escalation patterns
- **Consistency**: Measured by standard deviation of behavioral patterns
- **Learning**: Adaptation over session and response to feedback
- **Decision Speed**: Reaction times and hesitation patterns
- **Emotional Regulation**: Response to losses and stress patterns

### Reproducibility

All trait mappings are versioned and documented for scientific reproducibility:

- Data schema versioning
- Assessment algorithm versioning
- Confidence intervals and statistical validation
- Audit trails for all calculations

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test behavioral_data
python manage.py test agents
python manage.py test tasks

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Structure

```
tests/
├── test_agents/              # Agent functionality tests
├── test_behavioral_data/     # Data model and validation tests
├── test_tasks/               # Celery task tests
├── test_api/                 # API endpoint tests
└── test_trait_mapping/       # Trait inference tests
```

## 📈 Performance Monitoring

### Agent Metrics

Each agent provides performance metrics:

```python
from agents.event_logger import EventLogger

event_logger = EventLogger()
metrics = event_logger.get_performance_metrics()

# Returns:
# {
#     'agent_name': 'event_logger',
#     'uptime_seconds': 3600,
#     'processed_count': 1500,
#     'error_count': 5,
#     'success_rate': 0.997,
#     'last_activity': '2024-01-01T12:00:00Z'
# }
```

### Celery Task Monitoring

Monitor background task processing:

```bash
# Start Flower for task monitoring
celery -A pymetric flower

# View task results
celery -A pymetric inspect active
celery -A pymetric inspect stats
```

## 🔒 Security & Privacy

### Data Protection

- **Anonymization**: Automatic data anonymization for privacy compliance
- **Encryption**: Sensitive data encryption at rest and in transit
- **Audit Trails**: Comprehensive logging of all data access
- **GDPR Compliance**: Data retention policies and consent management

### Access Control

- Role-based permissions (Admin, Recruiter, Candidate)
- API authentication and rate limiting
- Session management and timeout policies
- CSRF protection and security headers


## 📚 API Documentation

### REST API Endpoints

The system provides comprehensive REST APIs:

- **Event Ingestion**: Real-time behavioral event capture
- **Data Retrieval**: Session and metric data access
- **Trait Profiles**: Psychometric assessment results
- **Reports**: Dashboard and reporting data

---

### Trait Inference API (Context Engineered)

**Purpose:**
Provide multi-dimensional psychometric trait profiles for a user/session, based on scientifically validated mapping from behavioral metrics.

**Endpoint:**
`/api/traits/trait-profiles/`

**Input:**
Session ID or user ID (as query or JSON)

**Output:**
Trait profile object with dimensions, scores, and confidence intervals.

**Validation:**
- Session data completeness (minimum sample size, data completeness threshold)
- Scientific validation thresholds (quality, reliability, confidence interval)
- Error handling for missing/incomplete data

**Example Request:**
```json
{
  "session_id": "session_123"
}
```

**Example Response:**
```json
{
  "risk_tolerance": 0.85,
  "consistency": 0.92,
  "learning": 0.78,
  "decision_speed": 0.67,
  "emotional_regulation": 0.81,
  "confidence_interval": 0.95
}
```

**Error Handling:**
If data is incomplete or does not meet scientific validation thresholds, return a validation error with guidance:
```json
{
  "error": "Insufficient data completeness (required: 80%).",
  "required_fields": ["session_id", "event_data"],
  "suggestion": "Ensure session contains at least 10 valid events."
}
```

**Self-Correcting Loop:**
- If validation fails, the agent or API provides actionable feedback for correction.
- All trait mappings are versioned and documented for reproducibility.

---

### API Authentication

```python
# Example API usage
import requests

headers = {
    'Authorization': 'Bearer <token>',
    'Content-Type': 'application/json'
}

# Ingest behavioral event
response = requests.post(
    'http://localhost:8000/api/events/',
    json=event_data,
    headers=headers
)
```

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   # Set production environment variables
   export DJANGO_SETTINGS_MODULE=pymetric.settings.production
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export REDIS_URL=redis://host:port/0
   ```

2. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

3. **Celery Workers**
   ```bash
   # Start multiple workers for different queues
   celery -A pymetric worker -Q events -l info
   celery -A pymetric worker -Q metrics -l info
   celery -A pymetric worker -Q inference -l info
   ```

4. **Monitoring**
   ```bash
   # Start monitoring tools
   celery -A pymetric flower
   python manage.py runserver 0.0.0.0:8000
   ```

## 🔧 Configuration

### Settings

Key configuration options in `settings.py`:

```python
# Behavioral data settings
BEHAVIORAL_DATA_SETTINGS = {
    'DATA_RETENTION_DAYS': 365,
    'ANONYMIZATION_ENABLED': True,
    'MIN_SESSION_DURATION_MS': 30000,
    'MAX_SESSION_DURATION_MS': 7200000,
    'EVENT_BATCH_SIZE': 100,
}

# Scientific validation settings
SCIENTIFIC_VALIDATION_SETTINGS = {
    'MIN_DATA_COMPLETENESS': 80.0,
    'MIN_QUALITY_SCORE': 70.0,
    'MIN_RELIABILITY_SCORE': 75.0,
    'CONFIDENCE_INTERVAL_LEVEL': 0.95,
    'MIN_SAMPLE_SIZE': 10,
}
```

### Environment Variables

```bash
# Required environment variables
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/0
CELERY_BROKER_URL=redis://host:port/0
```

## 📖 Documentation

### Scientific Documentation

- **Behavioral Data Schemas**: Detailed documentation of all behavioral data structures
- **Trait Mapping Logic**: Scientific basis for psychometric trait inference
- **Validation Methodology**: Data quality and scientific validation procedures
- **Reproducibility Guidelines**: Ensuring scientific reproducibility

### Technical Documentation

- **API Reference**: Complete REST API documentation
- **Agent Architecture**: Detailed agent design and implementation
- **Task Processing**: Celery task configuration and monitoring
- **Deployment Guide**: Production deployment procedures

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Run the test suite**
6. **Submit a pull request**

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Ensure 90%+ test coverage
- Run code quality checks: `black`, `flake8`, `mypy`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pymetrics**: For the scientific foundation of behavioral assessment
- **Django Community**: For the excellent web framework
- **Celery Team**: For robust background task processing
- **Scientific Community**: For behavioral psychology research

## 📞 Support

For questions, issues, or contributions:

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Read the Docs](https://your-docs.readthedocs.io)
- **Email**: support@your-domain.com

---

**Built with ❤️ for scientific behavioral assessment and talent analytics.**