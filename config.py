"""
Configuration file for Gutenberg Release Notes Generator
Customize this file to change the behavior of the generator
"""

# Versions to process
# Format: Can be either:
#   - Version string with 'v' prefix (e.g., "v22.0.0") - fetches from GitHub API
#   - Dictionary with 'file' key (e.g., {"file": "~/path/to/changelog.md", "version": "v22.4.0"})
VERSIONS = [
    "v22.0.0",
    "v22.1.0",
    "v22.2.0",
    "v22.3.0",
    {"file": "~/GBMain/gutenberg/gb224.md", "version": "v22.4.0"}
]

# Output file path
OUTPUT_FILE = "./release_notes_wp7.0.md"

# Developer-only keywords (case-insensitive)
# Enhancements containing these words will be filtered out
DEVELOPER_KEYWORDS = [
    'api',
    'hook', 
    'filter',
    'deprecat',
    'refactor',
    'internal',
    'unit test',
    'e2e test',
    'test coverage',
    'code quality',
    'technical debt',
    'types',
    'typescript'
]

# Claude API configuration
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 16000

# Prompt template for generating release notes
PROMPT_TEMPLATE = """You are writing release notes for WordPress Gutenberg plugin updates.

Here are the Enhancement sections from multiple Gutenberg releases:

{context}

Create a single, consolidated release notes document that:
1. Groups related improvements across versions (e.g., "List View improvements continued across 22.1-22.3")
2. Shows feature evolution and refinements
3. Highlights major themes
4. Uses clear, non-technical language suitable for WordPress users and editors
5. Avoids repetition - if similar features appear in multiple versions, combine them
6. Organizes by feature area rather than by version

For each feature, include:
- Feature name with GitHub PR link(s) in markdown format (e.g., [#72305](https://github.com/WordPress/gutenberg/pull/72305))
- Brief explanation of what it is and why it matters for users
- Practical benefits and use cases

Write in a friendly, clear tone that helps users understand the value of each improvement."""
