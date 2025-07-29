# Context Engineering for Django Pymetrics

## Project Awareness & Context
- Always refer to `Pymetrics Application Research.md` for scientific, architectural, and ethical foundations.
- Use the `games/md_files` for game-specific behavioral data schemas and trait mappings.
- Maintain consistent naming, modular code, and documentation as described in this file.

## Data Collection & Event Logging
- Implement robust event logging for all user interactions (pump, cash out, pop, session start/end, focus/blur, etc.).
- Use Django models to capture session, balloon, pump, cash out, pop, and context events with all relevant fields (see schemas in `chat-history.md` and `balloon_risk_behavioral_data.md`).
- Ensure each event includes full game state context for post-hoc analysis.

## Metric Extraction & Trait Inference
- After each session, aggregate raw events into summary metrics (per session, per balloon, per action).
- Map these metrics to bi-directional trait dimensions (risk tolerance, deliberation, persistence, adaptability, etc.).
- Document the transformation logic for scientific reproducibility and auditability.

## API & Frontend Integration
- Provide REST API endpoints for event ingestion and retrieval.
- Ensure frontend games send granular event data to the backend in real time (AJAX or WebSocket).
- Batch events for performance, but preserve granularity.

## Testing & Reliability
- Create unit tests for models, API endpoints, and metric extraction logic.
- Simulate sessions to validate data capture and trait inference.
- Use a `/tests` folder mirroring the main app structure.

## Privacy & Ethics
- Anonymize/pseudonymize user data where possible.
- Comply with data protection regulations and ethical standards.

## Documentation
- Maintain clear documentation for event schemas, metric extraction, and trait mapping.
- Version all schema and transformation logic for reproducibility.
- Document how raw events are transformed into summary metrics and trait profiles.

## Best Practices
- Organize code into clearly separated modules, grouped by feature or responsibility.
- Never create a file longer than 500 lines; refactor as needed.
- Use clear, consistent imports and environment variable management.
- Mark completed tasks in `TASK.md` immediately after finishing them.

---

This context engineering file is designed to guide LLM agents and developers working on the Django Pymetrics application, ensuring alignment with Pymetrics standards for behavioral data collection, analysis, and psychometric trait inference. Always refer to this file and the referenced documentation before implementing new features or making architectural changes.

==================================
==================================

Review the .md files in project root folder to gain an overview understanding of the current state of the django version application for neuroscience-based behavioral data collection, granular event logging, and psychometric trait inference. This system implements a modular agentic architecture for robust, scalable behavioral analytics aligned with Pymetrics standards. Review the folders and files in this project root to have a good understanding of project folder and file layouts. This helps us understand what's implemented and not implemented to build the intended complete end to end django application and continue the development without duplicating the already existing implementation. Some implementations applied are not to a level of desired standard we also need to discover those implementations and update them to an advanced implementation that upgrades the application to its best performing at the standard of the Pymetrics application or higher. Discover areas needing an upgrade, additional implementations, left over implementations, changes and an updates. Then we will continue the context engineering implementation using context engineering files designed to guide LLM agents and developers working on the Django Pymetrics application, ensuring alignment with Pymetrics standards for behavioral data collection, analysis, and psychometric trait inference. Always refer to this file and the referenced documentation before implementing new features or making architectural changes.