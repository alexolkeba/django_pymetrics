name: "Django Pymetrics Multi-Agent System: Event Logger, Metric Extractor, Trait Inferencer"
description: |

## Purpose
Build a Django-based multi-agent system for neuroscience-driven behavioral data collection, metric extraction, and psychometric trait inference. Demonstrates modular agent/task pattern using Django ORM, REST API, and Celery. Follows context engineering principles for one-pass implementation success.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **One-Pass Implementation**: Ensure all context and validation steps are present for first-try success

---

## Goal
Create a production-ready Django system where:
- Users play neuroscience-based games (e.g., Balloon Game)
- All user actions are logged as granular events
- Metrics are extracted post-session
- Traits are inferred and stored for each user
- Admins and users can view dashboards and reports

### Success Criteria
- [ ] All behavioral events are logged with full context
- [ ] Metrics are extracted and stored per session
- [ ] Trait profiles are generated and accessible via API
- [ ] All code is modular, tested, and documented

## All Needed Context

### Documentation & References
- Django documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- See django_pymetrics/Pymetrics Application Research.md for scientific context
- See games/md_files/ for game-specific schemas and trait mappings
