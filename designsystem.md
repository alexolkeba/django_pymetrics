# Professional Context Engineering for Django Pymetrics

This file is part of the context engineering discipline for one-pass implementation success in Django Pymetrics. It provides actionable, research-driven guidance for building robust, scalable, and scientifically valid behavioral analytics and agentic systems.

## Key Principles
- Modular, reusable design for all behavioral games and dashboards
- Mobile-friendly, accessible UIs from the start
- Use project-specific colors, fonts, and layouts that support neuroscience-based game interfaces
- Document all design choices and template structures for future developers
- Reference your own static files and CSS for consistent look and feel
- Adapt external inspiration (e.g., seogrove.ai) to fit the needs of behavioral data collection and analysis
- Ensure accessibility and usability for all users
- Use semantic HTML and ARIA roles for better screen reader support
- Provide clear visual feedback for user actions and game events

## Implementation Guidance
- Use Django template blocks and modular CSS/SCSS for all UIs. Structure templates in app-specific folders (e.g., `games/templates/games/`, `accounts/templates/accounts/`).
- Organize static assets (CSS, JS, images) in each app's `static/` directory. Use `{% static %}` in templates for asset references.
- Avoid hardcoding styles or variables; use a reusable system with design tokens and SCSS variables. Document all tokens in this file.
- Document design system decisions and template structures here for future context engineering and onboarding. Include rationale for major choices.
- Regularly review and update design patterns to align with evolving neuroscience and psychometric standards. Reference key research sources.
- Collaborate with UX/UI experts and behavioral scientists to validate design choices for analytics and game interfaces.
- Use design tokens and variables for consistent theming across all games and dashboards. Maintain a central palette and typography system.
- Test UI components for responsiveness (mobile, tablet, desktop) and cross-browser compatibility. List supported browsers and devices.
- Integrate user feedback loops (surveys, analytics) to continuously improve usability and engagement. Document feedback mechanisms.
- Ensure all visualizations and data displays are clear, interpretable, and scientifically valid. Use chart libraries that support accessibility.
- Provide accessibility checklists for each game and dashboard. Include ARIA roles, keyboard navigation, and color contrast validation.
- Maintain onboarding notes for new developers: how to extend templates, add new games, update design tokens, and validate UI changes.
- Future-proof the design system by tracking changes, versioning major updates, and documenting migration steps for legacy templates.