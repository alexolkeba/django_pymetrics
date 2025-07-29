name: "Django Pymetrics Agentic Framework: Neuroscience-Based Behavioral Data Collection & Trait Inference"
description: |

## Purpose
Build a comprehensive Django agentic framework for neuroscience-based behavioral data collection, granular event logging, and psychometric trait inference. This system will implement modular agents as Django modules and Celery tasks for robust, scalable behavioral analytics aligned with Pymetrics standards.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and scientific validation
2. **Validation Loops**: Provide executable tests and validation steps for scientific reproducibility
3. **Information Dense**: Use behavioral data schemas and trait mapping logic from research
4. **Progressive Success**: Start with core models, then expand to agents and APIs
5. **One-Pass Implementation**: Ensure all context and validation steps are present for first-try success

---

## Goal
Create a production-ready Django application with agentic capabilities for behavioral data collection, metric extraction, trait inference, and reporting. The system should capture granular behavioral data from neuroscience-based games, transform it into scientifically valid metrics, and infer psychometric traits using documented logic.

## Why
- **Scientific Value**: Enables reproducible behavioral data collection and analysis
- **Business Value**: Provides objective talent assessment and candidate matching
- **Technical Value**: Demonstrates advanced Django patterns with agentic architecture
- **Problems Solved**: Eliminates bias in hiring, provides granular behavioral insights, enables data-driven talent decisions

## What
A Django application with the following components:

### Core Agents (Django Modules/Celery Tasks)
- **EventLogger**: Logs all user interactions with granular detail
- **MetricExtractor**: Aggregates raw events into summary metrics
- **TraitInferencer**: Maps metrics to bi-directional trait dimensions
- **ReportGenerator**: Creates reports and dashboards

### Behavioral Data Collection
- Granular event logging for all game interactions
- Real-time data capture via AJAX/WebSocket
- JSON storage for flexibility and future-proofing

### Trait Inference System
- Multi-dimensional trait mapping (risk tolerance, working memory, etc.)
- Scientific validation and reproducibility
- Dynamic success model comparison

### REST API & Frontend Integration
- Event ingestion and retrieval endpoints
- Real-time data streaming
- Dashboard and reporting interfaces

### Success Criteria
- [ ] All agents successfully process behavioral data
- [ ] Granular event logging captures all relevant interactions
- [ ] Metric extraction produces scientifically valid summaries
- [ ] Trait inference generates accurate multi-dimensional profiles
- [ ] REST APIs handle real-time data ingestion and retrieval
- [ ] Frontend games integrate seamlessly with backend
- [ ] All tests pass and code meets scientific standards
- [ ] Privacy and ethical standards are maintained

## All Needed Context

### Documentation & References
# MUST READ - Include these in your context window
- url: https://docs.djangoproject.com/
  why: Django ORM and framework patterns
- url: https://www.django-rest-framework.org/
  why: DRF API development and serialization
- url: https://docs.celeryproject.org/
  why: Celery task queue for background processing
- url: https://pymetrics.com/
  why: Pymetrics behavioral assessment methodology
- url: https://docs.pytest.org/
  why: Testing framework for scientific validation

### Current Codebase Structure
```bash
django_pymetrics/
├── accounts/                    # User management
│   ├── models.py               # User, RecruiterProfile, CandidateProfile
│   ├── views.py                # User views and authentication
│   └── urls.py                 # User routing
├── games/                      # Game sessions and results
│   ├── models.py               # GameSession, GameResult
│   ├── views.py                # Game views and logic
│   ├── md_files/               # Behavioral data schemas
│   └── templates/              # Game templates
├── ai_model/                   # Trait profiles and inference
│   ├── models.py               # TraitProfile
│   ├── ai_scoring.py           # Basic scoring logic
│   └── train_and_export.py     # Model training
├── pymetric/                   # Core settings
├── django_backend/             # Static assets
├── examples/                   # Code examples
│   ├── event_logging.py        # Event logging patterns
│   └── trait_inference.py      # Trait inference patterns
├── PRPs/                       # Product Requirements Prompts
├── research/                   # Research documentation
└── manage.py                   # Django management
```

### Desired Codebase Structure with New Files
```bash
django_pymetrics/
├── agents/                     # NEW: Agentic framework
│   ├── __init__.py            # Package init
│   ├── event_logger.py        # EventLogger agent
│   ├── metric_extractor.py    # MetricExtractor agent
│   ├── trait_inferencer.py    # TraitInferencer agent
│   ├── report_generator.py    # ReportGenerator agent
│   └── base_agent.py          # Base agent class
├── api/                       # NEW: REST API endpoints
│   ├── __init__.py            # Package init
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API views
│   ├── urls.py                # API routing
│   └── permissions.py         # API permissions
├── tasks/                     # NEW: Celery tasks
│   ├── __init__.py            # Package init
│   ├── event_processing.py    # Event processing tasks
│   ├── metric_extraction.py   # Metric extraction tasks
│   ├── trait_inference.py     # Trait inference tasks
│   └── reporting.py           # Reporting tasks
├── behavioral_data/           # NEW: Behavioral data models
│   ├── __init__.py            # Package init
│   ├── models.py              # Event and metric models
│   ├── schemas.py             # Data schemas
│   └── validators.py          # Data validation
├── trait_mapping/             # NEW: Trait mapping logic
│   ├── __init__.py            # Package init
│   ├── mappings.py            # Trait mapping functions
│   ├── success_models.py      # Success model logic
│   └── validation.py          # Scientific validation
├── tests/                     # NEW: Comprehensive tests
│   ├── __init__.py            # Package init
│   ├── test_agents/           # Agent tests
│   ├── test_api/              # API tests
│   ├── test_tasks/            # Task tests
│   ├── test_models/           # Model tests
│   └── test_trait_mapping/    # Trait mapping tests
├── static/                    # NEW: Frontend assets
│   ├── js/                    # JavaScript for games
│   ├── css/                   # Stylesheets
│   └── games/                 # Game-specific assets
├── templates/                 # NEW: Frontend templates
│   ├── games/                 # Game templates
│   ├── dashboard/             # Dashboard templates
│   └── reports/               # Report templates
├── config/                    # NEW: Configuration
│   ├── __init__.py            # Package init
│   ├── settings/              # Django settings
│   ├── celery.py              # Celery configuration
│   └── logging.py             # Logging configuration
├── requirements.txt           # Updated dependencies
├── celery.py                  # Celery app configuration
├── .env.example               # Environment variables
└── README.md                  # Updated documentation
```

### Behavioral Data Schemas (from md_files/)
The system must implement granular event logging based on these schemas:

#### Balloon Risk Game Events
- **Session Events**: start/end timestamps, device info, total balloons
- **Balloon Events**: color, index, start/end times, outcome (popped/cashed)
- **Pump Events**: timestamp, pump number, time intervals, balloon size, earnings
- **Cash Out Events**: timestamp, pumps before cash out, earnings collected
- **Pop Events**: timestamp, pumps at pop, earnings lost

#### Trait Mapping Logic
- **Risk Tolerance**: Average pumps per balloon, risk escalation patterns
- **Consistency**: Standard deviation of pumps, behavioral patterns
- **Learning**: Adaptation over session, response to feedback
- **Decision Speed**: Reaction times, hesitation patterns
- **Emotional Regulation**: Response to losses, stress patterns

### Known Gotchas & Library Quirks
```python
# Django ORM Gotchas
- Use select_related() and prefetch_related() for efficient queries
- JSONField requires proper serialization/deserialization
- DateTimeField auto_now_add vs auto_now differences

# Celery Gotchas
- Tasks must be idempotent for reliability
- Use retry mechanisms for transient failures
- Monitor task queues for performance

# DRF Gotchas
- Serializer validation vs model validation
- Nested serializers for complex data structures
- Permission classes for data access control

# Behavioral Data Gotchas
- Timestamp precision matters for scientific validity
- Event ordering must be preserved
- Data anonymization for privacy compliance
```

## Implementation Plan

### Phase 1: Core Models and Data Structures
1. **Extend Behavioral Data Models**
   - Create granular event models for each game type
   - Implement JSON field schemas for flexibility
   - Add validation for scientific data integrity

2. **Enhance Trait Profile Models**
   - Extend TraitProfile with additional dimensions
   - Add success model comparison fields
   - Implement versioning for reproducibility

3. **Create Event Logging Infrastructure**
   - Build base event logging models
   - Implement event serialization/deserialization
   - Add event validation and sanitization

### Phase 2: Agentic Framework Implementation
1. **Base Agent Class**
   - Create abstract base agent with common functionality
   - Implement logging, error handling, and monitoring
   - Add configuration management

2. **EventLogger Agent**
   - Implement real-time event capture
   - Add event validation and storage
   - Create event streaming capabilities

3. **MetricExtractor Agent**
   - Build metric aggregation logic
   - Implement session-level and game-level metrics
   - Add metric validation and caching

4. **TraitInferencer Agent**
   - Implement trait mapping algorithms
   - Add success model comparison logic
   - Create trait profile generation

5. **ReportGenerator Agent**
   - Build dashboard data aggregation
   - Implement report generation
   - Add export capabilities

### Phase 3: API and Frontend Integration
1. **REST API Development**
   - Create event ingestion endpoints
   - Implement data retrieval APIs
   - Add authentication and permissions

2. **Frontend Game Integration**
   - Build JavaScript event capture
   - Implement real-time data streaming
   - Add game state management

3. **Dashboard and Reporting**
   - Create admin dashboards
   - Implement user reports
   - Add data visualization

### Phase 4: Celery Task Integration
1. **Background Processing**
   - Implement event processing tasks
   - Add metric extraction tasks
   - Create trait inference tasks

2. **Task Monitoring**
   - Add task queue monitoring
   - Implement error handling and retries
   - Create performance metrics

### Phase 5: Testing and Validation
1. **Unit Tests**
   - Test all agent functionality
   - Validate API endpoints
   - Verify trait mapping logic

2. **Integration Tests**
   - Test end-to-end data flow
   - Validate real-time processing
   - Verify scientific accuracy

3. **Performance Tests**
   - Test scalability and throughput
   - Validate memory usage
   - Verify response times

## Validation Gates

### Code Quality Gates
```bash
# Run these commands and ensure they pass
python manage.py check
python manage.py makemigrations --check
python manage.py test --verbosity=2
flake8 --max-line-length=100 --exclude=migrations
black --check --line-length=100 .
```

### Scientific Validation Gates
```bash
# Validate behavioral data integrity
python manage.py validate_behavioral_data

# Test trait mapping accuracy
python manage.py test_trait_mapping

# Verify event logging completeness
python manage.py verify_event_logging
```

### Performance Gates
```bash
# Test API response times
python manage.py test_api_performance

# Validate Celery task throughput
python manage.py test_task_performance

# Check memory usage
python manage.py monitor_memory_usage
```

## Success Metrics

### Technical Metrics
- [ ] All tests pass with >90% coverage
- [ ] API response times <200ms for 95% of requests
- [ ] Event processing latency <1 second
- [ ] Memory usage <512MB for typical session
- [ ] Database query optimization (N+1 queries eliminated)

### Scientific Metrics
- [ ] Behavioral data capture completeness >99%
- [ ] Trait mapping accuracy validated against known patterns
- [ ] Event ordering preserved with millisecond precision
- [ ] Data anonymization implemented for privacy
- [ ] Reproducible results across multiple sessions

### Business Metrics
- [ ] Real-time event processing operational
- [ ] Dashboard provides actionable insights
- [ ] API supports frontend integration
- [ ] Reporting system generates comprehensive profiles
- [ ] System scales to handle concurrent users

## Error Handling & Edge Cases

### Data Validation Errors
- Invalid event data format
- Missing required fields
- Timestamp inconsistencies
- Duplicate event IDs

### Processing Errors
- Celery task failures
- Database connection issues
- Memory overflow scenarios
- Network timeouts

### Scientific Validation Errors
- Trait mapping inconsistencies
- Metric calculation errors
- Success model comparison failures
- Data integrity violations

## Security & Privacy Considerations

### Data Protection
- Implement data anonymization
- Add encryption for sensitive data
- Create audit trails for data access
- Ensure GDPR compliance

### Access Control
- Role-based permissions
- API authentication
- Session management
- Rate limiting

### Scientific Ethics
- Informed consent mechanisms
- Data retention policies
- Bias detection and mitigation
- Transparent algorithms

## Documentation Requirements

### Code Documentation
- Comprehensive docstrings for all functions
- API documentation with examples
- Architecture diagrams and flow charts
- Deployment and configuration guides

### Scientific Documentation
- Behavioral data schema documentation
- Trait mapping logic explanations
- Validation methodology descriptions
- Reproducibility guidelines

### User Documentation
- Game integration guides
- API usage examples
- Dashboard user manuals
- Troubleshooting guides

## Future Extensibility

### Modular Design
- Plugin architecture for new games
- Extensible trait mapping system
- Configurable success models
- Customizable reporting templates

### Scalability Considerations
- Horizontal scaling capabilities
- Database sharding strategies
- Caching layer implementation
- Load balancing preparation

### Integration Points
- Third-party assessment tools
- HR system integrations
- Analytics platform connections
- Machine learning pipeline integration

---

## Confidence Score: 9/10

This PRP provides comprehensive context for implementing a Django Pymetrics agentic framework with scientific rigor and production readiness. The implementation plan is detailed, validation gates are clear, and all necessary documentation and examples are included for one-pass success.

## Next Steps
1. Execute this PRP to implement the complete system
2. Run all validation gates to ensure quality
3. Deploy and monitor for production readiness
4. Document any discovered edge cases or improvements 