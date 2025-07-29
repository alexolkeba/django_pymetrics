# Professional Context Engineering Quick Start for Django Pymetrics

This guide provides a clear, actionable foundation for one-pass implementation success in Django Pymetrics. Follow these steps to ensure your project is robust, scalable, and scientifically valid.

## What You Have
- Modular context engineering system for Django Pymetrics
- Templates for global rules, feature requests, code examples, and implementation blueprints

## How to Use This Template

### Step 1: Customize CLAUDE.md
- Add Django-specific rules: ORM, DRF, event logging, privacy, scientific documentation
- Require event logging for all behavioral games
- Ensure privacy and reproducibility

### Step 2: Add Examples
- Place Django code examples in the `examples/` folder:
  - Event logging models
  - API endpoints for behavioral data
  - Metric extraction and trait inference scripts
  - Unit tests for reliability

### Step 3: Create Your Feature Request
- Edit `INITIAL.md` with your feature:
```markdown
## FEATURE:
Build a REST API for granular behavioral event logging and trait inference for Balloon Game

## EXAMPLES:
See examples/event_logging.py for our standard Django model and API structure

## DOCUMENTATION:
- Django docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- See django_pymetrics/Pymetrics Application Research.md for scientific context
```

### Step 4: Generate the PRP
In Claude Code, run:
```
/generate-prp INITIAL.md
```

This creates a comprehensive implementation blueprint in `PRPs/`

### Step 5: Execute the PRP
```
/execute-prp PRPs/your-feature.md
```

The AI will implement your feature following all the context you provided.

## Tips for Success

1. **More Examples = Better Results**: The AI performs best when it has patterns to follow
2. **Be Specific in INITIAL.md**: Don't assume the AI knows your preferences
3. **Use the Validation**: PRPs include test commands that ensure working code
4. **Iterate**: You can generate multiple PRPs and refine them before execution

## Common Use Cases

- **New Features**: Describe what you want, provide examples, get implementation
- **Refactoring**: Show current code patterns, describe desired state
- **Bug Fixes**: Include error logs, expected behavior, relevant code
- **Integration**: Provide API docs, show existing integration patterns

## Next Steps

1. Start with a simple feature to test the workflow
2. Build up your examples folder over time
3. Refine CLAUDE.md as you discover patterns
4. Use PRPs for all major features to ensure consistency