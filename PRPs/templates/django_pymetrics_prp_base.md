name: "Django Pymetrics PRP Base Template v2"
description: |

## Purpose
Template optimized for Django Pymetrics AI agents to implement features with sufficient context and self-validation capabilities for behavioral data collection, metric extraction, and trait inference. Follows context engineering principles for one-pass implementation success.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md
6. **One-Pass Implementation**: Ensure all context and validation steps are present for first-try success

---

## Goal
[Describe the Django behavioral analytics feature to be built]

## Why
- [Business value and user impact for neuroscience-based talent assessment]
- [Integration with existing Django models, APIs, and trait inference logic]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements for Django event logging, metric extraction, and trait inference]

### Success Criteria
- [ ] [Specific measurable outcomes for Django behavioral analytics]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- file: django_pymetrics/Pymetrics Application Research.md
  why: Scientific and architectural context
- file: django_pymetrics/games/md_files/balloon_risk_behavioral_data.md
  why: Game-specific behavioral data schema
- url: https://docs.djangoproject.com/
  why: Django ORM and API patterns
- url: https://www.django-rest-framework.org/
  why: REST API implementation
```
