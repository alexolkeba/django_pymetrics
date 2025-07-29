---

# Context Engineering for One-Pass Implementation Success

## Philosophy in Practice

To achieve one-pass implementation success, Context Engineering requires:

1. **Comprehensive Context**
   - Document all requirements, rules, and edge cases before coding.
   - Include examples, validation logic, and error handling patterns.
   - Reference all relevant documentation and APIs.

2. **Explicit Patterns and Conventions**
   - Use clear folder and module structures.
   - Follow project-wide coding standards (see CLAUDE.md).
   - Provide example files for every major pattern.

3. **Validation Gates**
   - Define tests and validation steps up front.
   - Ensure every implementation step has a corresponding test or check.
   - Use self-correcting loops: if a test fails, provide actionable feedback and iterate.

4. **Documentation Hooks**
   - Automatically update documentation as features are implemented.
   - Link code, tests, and docs for traceability.

5. **Self-Correcting Implementation**
   - If requirements or context are missing, halt and request clarification.
   - Use error messages and validation failures to improve context.

## Actionable Checklist for One-Pass Success

- [ ] Initial feature request is explicit and comprehensive (see INITIAL.md)
- [ ] PRP includes all context, validation, and examples
- [ ] Examples folder contains relevant code patterns
- [ ] CLAUDE.md defines project rules and standards
- [ ] Tests are defined before implementation begins
- [ ] Implementation follows documented patterns and validation gates
- [ ] Documentation is updated with every new feature
- [ ] All validation gates pass before feature is considered complete

By following this checklist, you maximize the chance of one-pass implementation success—where features are implemented correctly the first time, with minimal iteration.
Quick Start
For full setup with automatic documentation hooks: See SETUP.md

For basic template usage:

# 1. Set up your project rules (optional - template provided)
# Edit CLAUDE.md to add your project-specific guidelines

# 2. Add examples (highly recommended)
# Place relevant code examples in the examples/ folder

# 3. Create your initial feature request
# Edit INITIAL.md with your feature requirements

# 4. Generate a comprehensive PRP (Product Requirements Prompt)
# In Claude Code, run:
/generate-prp INITIAL.md

# 5. Execute the PRP to implement your feature
# In Claude Code, run:
/execute-prp PRPs/your-feature-name.md

📚 Table of Contents
- What is Context Engineering?
- Template Structure
- Step-by-Step Guide
- Writing Effective INITIAL.md Files
- The PRP Workflow
- Using Examples Effectively
- Best Practices

# What is Context Engineering?

Context Engineering represents a paradigm shift from traditional prompt engineering:

## Prompt Engineering vs Context Engineering

# Prompt Engineering:
Focuses on clever wording and specific phrasing
Limited to how you phrase a task
Like giving someone a sticky note

# Context Engineering:
A complete system for providing comprehensive context
Includes documentation, examples, rules, patterns, and validation
Like writing a full screenplay with all the details

# Why Context Engineering Matters
- Reduces AI Failures: Most agent failures aren't model failures - they're context failures
- Ensures Consistency: AI follows your project patterns and conventions
- Enables Complex Features: AI can handle multi-step implementations with proper context
- Self-Correcting: Validation loops allow AI to fix its own mistakes

# Template Structure
context-engineering-intro/
├── .claude/
│   ├── commands/
│   │   ├── generate-prp.md    # Generates comprehensive PRPs
│   │   └── execute-prp.md     # Executes PRPs to implement features
│   └── settings.local.json    # Claude Code permissions
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md       # Base template for PRPs
│   └── EXAMPLE_multi_agent_prp.md  # Example of a complete PRP
├── examples/                  # Your code examples (critical!)
├── CLAUDE.md                 # Global rules for AI assistant
├── INITIAL.md               # Template for feature requests
├── INITIAL_EXAMPLE.md       # Example feature request
└── README.md                # Readme file (This file)
This template doesn't focus on RAG and tools with context engineering because I have a LOT more in store for that soon. 

## Step-by-Step Guide
1. Set Up Global Rules (CLAUDE.md)
The CLAUDE.md file contains project-wide rules that the AI assistant will follow in every conversation. The template includes:

- Project awareness: Reading planning docs, checking tasks
- Code structure: File size limits, module organization
- Testing requirements: Unit test patterns, coverage expectations
- Style conventions: Language preferences, formatting rules
- Documentation standards: Docstring formats, commenting practices
You can use the provided template as-is or customize it for your project.

2. Create Your Initial Feature Request
Edit INITIAL.md to describe what you want to build:

## FEATURE:
[Describe what you want to build - be specific about functionality and requirements]

## EXAMPLES:
[List any example files in the examples/ folder and explain how they should be used]

## DOCUMENTATION:
[Include links to relevant documentation, APIs, or MCP server resources]

## OTHER CONSIDERATIONS:
[Mention any gotchas, specific requirements, or things AI assistants commonly miss]
See INITIAL_EXAMPLE.md for a complete example.

3. Generate the PRP
PRPs (Product Requirements Prompts) are comprehensive implementation blueprints that include:

- Complete context and documentation
- Implementation steps with validation
- Error handling patterns
- Test requirements
They are similar to PRDs (Product Requirements Documents) but are crafted more specifically to instruct an AI coding assistant.

Run in Claude Code:

/generate-prp INITIAL.md
Note: The slash commands are custom commands defined in .claude/commands/. You can view their implementation:

.claude/commands/generate-prp.md - See how it researches and creates PRPs
.claude/commands/execute-prp.md - See how it implements features from PRPs
The $ARGUMENTS variable in these commands receives whatever you pass after the command name (e.g., INITIAL.md or PRPs/your-feature.md).

This command will:

- Read your feature request
- Research the codebase for patterns
- Search for relevant documentation
- Create a comprehensive PRP in PRPs/your-feature-name.md

4. Execute the PRP
Once generated, execute the PRP to implement your feature:

/execute-prp PRPs/your-feature-name.md
The AI coding assistant will:

Read all context from the PRP
Create a detailed implementation plan
Execute each step with validation
Run tests and fix any issues
Ensure all success criteria are met
Writing Effective INITIAL.md Files
Key Sections Explained
FEATURE: Be specific and comprehensive

❌ "Build a web scraper"
✅ "Build an async web scraper using BeautifulSoup that extracts product data from e-commerce sites, handles rate limiting, and stores results in PostgreSQL"
EXAMPLES: Leverage the examples/ folder

Place relevant code patterns in examples/
Reference specific files and patterns to follow
Explain what aspects should be mimicked
DOCUMENTATION: Include all relevant resources

API documentation URLs
Library guides
MCP server documentation
Database schemas
OTHER CONSIDERATIONS: Capture important details

Authentication requirements
Rate limits or quotas
Common pitfalls
Performance requirements
The PRP Workflow
How /generate-prp Works
The command follows this process:

Research Phase

Analyzes your codebase for patterns
Searches for similar implementations
Identifies conventions to follow
Documentation Gathering

Fetches relevant API docs
Includes library documentation
Adds gotchas and quirks
Blueprint Creation

Creates step-by-step implementation plan
Includes validation gates
Adds test requirements
Quality Check

Scores confidence level (1-10)
Ensures all context is included
How /execute-prp Works
Load Context: Reads the entire PRP
Plan: Creates detailed task list using TodoWrite
Execute: Implements each component
Validate: Runs tests and linting
Iterate: Fixes any issues found
Complete: Ensures all requirements met
See PRPs/EXAMPLE_multi_agent_prp.md for a complete example of what gets generated.

Using Examples Effectively
The examples/ folder is critical for success. AI coding assistants perform much better when they can see patterns to follow.

What to Include in Examples
Code Structure Patterns

How you organize modules
Import conventions
Class/function patterns
Testing Patterns

Test file structure
Mocking approaches
Assertion styles
Integration Patterns

API client implementations
Database connections
Authentication flows
CLI Patterns

Argument parsing
Output formatting
Error handling
Example Structure
examples/
├── README.md           # Explains what each example demonstrates
├── cli.py             # CLI implementation pattern
├── agent/             # Agent architecture patterns
│   ├── agent.py      # Agent creation pattern
│   ├── tools.py      # Tool implementation pattern
│   └── providers.py  # Multi-provider pattern
└── tests/            # Testing patterns
    ├── test_agent.py # Unit test patterns
    └── conftest.py   # Pytest configuration
Best Practices
1. Be Explicit in INITIAL.md
Don't assume the AI knows your preferences
Include specific requirements and constraints
Reference examples liberally
2. Provide Comprehensive Examples
More examples = better implementations
Show both what to do AND what not to do
Include error handling patterns
3. Use Validation Gates
PRPs include test commands that must pass
AI will iterate until all validations succeed
This ensures working code on first try
4. Leverage Documentation
Include official API docs
Add MCP server resources
Reference specific documentation sections
5. Customize CLAUDE.md
Add your conventions
Include project-specific rules
Define coding standards
🎯 Advanced PRP Method - Multi-Agent Research Approach
This template demonstrates an advanced PRP creation method using multiple parallel research agents for comprehensive documentation gathering.

See Advanced AI Automation Examples
SEO Grove: https://seogrove.ai/ - Example of advanced AI automation (built with different methods)
YouTube Channel: https://www.youtube.com/c/incomestreamsurfers - Learn more about AI automation methodologies
AI Automation School: https://www.skool.com/iss-ai-automation-school-6342/about - Join our community
Advanced PRP Creation Process
Prompt 1: Initialize Research Framework
read my incredibly specific instructions about how to create a prp document then summarise them, also store how to do a jina scrapein order to create a llm.txt in your memory

If a page 404s or does not scrape properly, scrape it again

Do not use Jina to scrape CSS of the design site.

All SEPARATE pages must be stored in /research/[technology]/ directories with individual .md files.

curl
  "https://r.jina.ai/https://platform.openai.com/docs/" \
    -H "Authorization: Bearer jina_033257e7cdf14fd3b948578e2d34986bNtfCCkjHt7_j1Bkp5Kx521rDs2Eb"
Prompt 2: Generate PRP with Parallel Research
/generate-prp initial.md
Wait until it gets to the research phase, then press escape and say:

can you spin up multiple research agents and do this all at the same time
This approach enables:

Parallel Documentation Scraping: 6+ agents simultaneously research different technologies
Comprehensive Coverage: 30-100+ pages of official documentation scraped and organized
Technology-Specific Organization: Each technology gets its own /research/[tech]/ directory
Production-Ready PRPs: Complete implementation blueprints with real-world examples
Research Directory Structure
research/
├── pydantic-ai/      # 22+ documentation pages
├── openai/           # 20+ API documentation pages  
├── anthropic/        # 18+ Claude documentation pages
├── jina/             # 12+ scraping API pages
├── shopify/          # 18+ GraphQL/REST API pages
└── seo-apis/         # 24+ Search Console/Ahrefs pages
This multi-agent research approach results in PRPs with 9/10 confidence scores for one-pass implementation success.

