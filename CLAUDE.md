# Professional Context Engineering for Django Pymetrics

## Project Awareness & Context
- Modular Django apps: `accounts` (user management), `ai_model` (trait profiles), `games` (game sessions/results), `pymetric` (core settings), and `django_backend/static/emotional_faces` (game assets).
- Models for users (`User`, `RecruiterProfile`, `CandidateProfile`), game sessions/results (`GameSession`, `GameResult`), and trait profiles (`TraitProfile`).
- Designed for neuroscience-based behavioral data collection, granular event logging, and psychometric trait inference, aligned with Pymetrics standards.

## Data Collection & Event Logging
- Implement robust event logging for all user interactions in each game (e.g., Balloon Risk, Memory Cards, Reaction Timer, etc.).
- Use Django models to capture session, trial, action, and meta-events, ensuring all relevant fields are present (see `games/models.py` and `ai_model/models.py`).
- Store raw behavioral data in JSON fields for flexibility and future-proofing.

## Metric Extraction & Trait Inference
- After each session, aggregate raw events into summary metrics (per session, per game, per action).
- Map these metrics to bi-directional trait dimensions (risk tolerance, working memory, attention control, etc.) using documented logic in `ai_model/models.py` and game-specific schemas.
- Document the transformation logic for scientific reproducibility and auditability.

## API & Frontend Integration
- Provide REST API endpoints for event ingestion, retrieval, and trait profile access.
- Ensure frontend games send granular event data to the backend in real time (AJAX/WebSocket).
- Batch events for performance, but preserve granularity and context.

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
- Review and refactor existing models in `accounts/models.py`, `ai_model/models.py`, and `games/models.py` to ensure all necessary fields and relationships are present for behavioral analytics.
- Expand event logging to cover all granular behavioral data points for each game.
- Implement metric extraction and trait inference logic as modular, testable Django/Celery tasks.
- Build REST APIs for all core data flows and ensure frontend integration for real-time event capture.
- Document every schema, transformation, and trait mapping for future developers and scientific validation.

---

This context engineering guide is designed to enable AI coding assistants and developers to update, extend, and implement all necessary features for a fully functional Django Pymetrics application, ensuring one-pass implementation success and alignment with the highest standards of behavioral data science.

### 🌀 Project Awareness & Context & Research
- Always read `Pymetrics Application Research.md` at the start of a new conversation to understand the scientific, architectural, and ethical foundations of the Django Pymetrics project.
- Check `TASK.md` before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- Use consistent naming conventions, file structure, and architecture patterns as described in this context engineering template.
- Use Django ORM for all models and Django REST Framework for APIs.
- Use Docker for local development and testing if possible.
- Stick to OFFICIAL DOCUMENTATION PAGES ONLY for Django, DRF, and scientific references.
- Refer to the `/research/` directory and `games/md_files/` for behavioral data schemas and trait mappings before implementing any feature.
- Always version event schemas and metric extraction logic for scientific reproducibility.

### 🧩 Code Structure & Modularity
- Never create a file longer than 500 lines of code. Refactor by splitting into modules or helper files.
- Organize code into clearly separated Django apps and modules, grouped by feature or responsibility.
- Use clear, consistent imports and environment variable management.
- Use pytest for unit tests and scientific documentation standards.
- All behavioral event logging and trait inference logic must be modular and well-documented.

### 🧪 Testing & Reliability
- Always create Pytest unit tests for new features (models, APIs, metric extraction, trait inference).
- Simulate sessions to validate data capture and trait inference.
- Tests should live in a `/tests` folder mirroring the main app structure.
- Include at least: 1 test for expected use, 1 edge case, 1 failure case.

### ✅ Task Completion
- Mark completed tasks in `TASK.md` immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 🏷️ Style & Conventions
- Use Python as the primary language.
- Follow PEP8, use type hints, and format with `black`.
- Use Django ORM for data validation and DRF for APIs.
- Write docstrings for every function using the Google style.

### 📚 Documentation & Explainability
- Update `README.md` when new features are added, dependencies change, or setup steps are modified.
- Comment non-obvious code and ensure everything is understandable to a mid-level developer.
- When writing complex logic, add an inline `# Reason:` comment explaining the why, not just the what.
- Document all event schemas, metric extraction, and trait mapping logic for scientific reproducibility.

### 🤖 AI Behavior Rules
- Never assume missing context. Ask questions if uncertain.
- Never hallucinate libraries or functions – only use known, verified Python packages.
- Always confirm file paths and module names exist before referencing them in code or tests.
- Never delete or overwrite existing code unless explicitly instructed to or if part of a task from `TASK.md`.

### 🔒 Privacy & Ethics
- Anonymize/pseudonymize user data where possible.
- Comply with data protection regulations and ethical standards.
- Ensure all behavioral data handling is scientifically valid and reproducible.

### 🎨 Design
- Stick to the design system inside designsystem.md for building any new features and game UIs.

