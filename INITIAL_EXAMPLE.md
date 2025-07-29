# Professional Context Engineering for Django Pymetrics

## Project Awareness & Context
- Modular Django apps: `accounts`, `ai_model`, `games`, `pymetric`, and `django_backend/static/emotional_faces`.
- Models for users, game sessions/results, and trait profiles.
- Designed for neuroscience-based behavioral data collection, granular event logging, and psychometric trait inference.

## Data Collection & Event Logging
- Implement robust event logging for all user interactions in each game.
- Use Django models to capture session, trial, action, and meta-events.
- Store raw behavioral data in JSON fields for flexibility.

## Metric Extraction & Trait Inference
- Aggregate raw events into summary metrics after each session.
- Map metrics to bi-directional trait dimensions using documented logic.
- Document transformation logic for scientific reproducibility.

## API & Frontend Integration
- Provide REST API endpoints for event ingestion, retrieval, and trait profile access.
- Ensure frontend games send granular event data to the backend in real time.
- Batch events for performance, but preserve granularity.

## Testing & Reliability
- Create unit tests for models, API endpoints, and metric extraction logic.
- Simulate sessions to validate data capture and trait inference.
- Use a `/tests` folder mirroring the main app structure.

## Privacy & Ethics
- Anonymize/pseudonymize user data where possible.
- Comply with data protection regulations and ethical standards.
- Ensure all behavioral data handling is scientifically valid and reproducible.

## Documentation
- Maintain clear documentation for event schemas, metric extraction, and trait mapping.
- Version all schema and transformation logic for reproducibility.
- Document how raw events are transformed into summary metrics and trait profiles.

## Best Practices
- Organize code into clearly separated modules, grouped by feature or responsibility.
- Never create a file longer than 500 lines; refactor as needed.
- Use clear, consistent imports and environment variable management.
- Mark completed tasks in `TASK.md` immediately after finishing them.
- Reference official Django and DRF documentation, as well as your own research files.

---

## Implementation Guidance
- Review and refactor existing models to ensure all necessary fields and relationships are present for behavioral analytics.
- Expand event logging to cover all granular behavioral data points for each game.
- Implement metric extraction and trait inference logic as modular, testable Django/Celery tasks.
- Build REST APIs for all core data flows and ensure frontend integration for real-time event capture.
- Document every schema, transformation, and trait mapping for future developers and scientific validation.

---

This context engineering guide is designed to enable AI coding assistants and developers to update, extend, and implement all necessary features for a fully functional Django Pymetrics application, ensuring one-pass implementation success and alignment with the highest standards of behavioral data science.

## FEATURE:

- Build a Django REST API for granular behavioral event logging and trait inference for Balloon Game
- Implement Django models for session, balloon, pump, cash out, pop, and context events
- Create metric extraction and trait inference logic as Django modules or Celery tasks
- Provide admin dashboard and user-facing game UIs using Django templates

## EXAMPLES:

In the `examples/` folder, you will find Django model, serializer, and API examples for behavioral event logging and trait inference.

- `examples/event_logging.py` - template for Django event logging model and API
- `examples/trait_inference.py` - template for metric extraction and trait inference logic

Use these as inspiration and for best practices. Do not copy directly; adapt to your game and trait requirements.

## DOCUMENTATION:

- Django documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- See django_pymetrics/Pymetrics Application Research.md for scientific context

## OTHER CONSIDERATIONS:

- Include a .env.example, README with instructions for Django setup and configuration
- Document project structure and event schema versioning
- Use pytest and scientific documentation standards
