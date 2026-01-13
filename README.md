# Gutenberg Release Notes Generator

Automatically generate user-friendly release notes from multiple Gutenberg plugin releases by extracting and consolidating Enhancement sections using AI.

## Overview

This tool:
1. **Fetches** release data from GitHub for specified Gutenberg versions
2. **Extracts** Enhancement sections from each release
3. **Filters** out developer-only features to focus on user-facing changes
4. **Consolidates** changes across multiple versions
5. **Generates** narrative release notes using Claude API

## Features

- ✅ Automatic filtering of developer-focused enhancements
- ✅ Smart grouping of related features across versions
- ✅ Natural language narrative output (not bullet points)
- ✅ Customizable version ranges
- ✅ Intermediate file outputs for review

## Installation

### Requirements

- Python 3.7+
- `requests` library

### Setup

```bash
# Install dependencies
pip install requests

# Clone or download this repository
# No additional setup required!
```

## Usage

### Basic Usage

```bash
python gutenberg_release_notes.py
```

### Configuration

Edit the script to customize:

```python
# Specify which versions to process
VERSIONS = ["v22.0.0", "v22.1.0", "v22.2.0", "v22.3.0"]

# Optional: Set your Anthropic API key
ANTHROPIC_API_KEY = "your-api-key-here"
```

### With API Key

If you provide an Anthropic API key, the tool will automatically generate the final release notes:

```bash
# Set environment variable
export ANTHROPIC_API_KEY="your-key"
python gutenberg_release_notes.py

# Or edit the script directly
# ANTHROPIC_API_KEY = "your-key"
```

### Without API Key

If no API key is provided, the tool will:
1. Extract and filter enhancements
2. Save a formatted prompt to `claude_prompt.txt`
3. You can then manually paste this into claude.ai

## Output Files

The tool generates several files:

| File | Description |
|------|-------------|
| `enhancements_filtered.txt` | All user-facing enhancements organized by version and section |
| `claude_prompt.txt` | Ready-to-use prompt for Claude API |
| `release_notes_X_Y.md` | Final consolidated release notes (if API key provided) |

## How It Works

### 1. Fetching Releases

The tool fetches release pages from GitHub:
```
https://github.com/WordPress/gutenberg/releases/tag/v22.3.0
```

### 2. Parsing Enhancements

Extracts the `### Enhancements` section and identifies:
- Subsection headers (e.g., `#### Block Editor`)
- Individual enhancement items (lines starting with `*`)

### 3. Filtering

Removes developer-only enhancements based on:

**Developer-only sections:**
- Data Layer
- Code Quality  
- Build Tooling
- Testing
- Documentation
- Tools & Packages

**Developer-only keywords:**
- API, hooks, refactor
- TypeScript migrations
- Test improvements
- Type annotations

**User-facing indicators:**
- UI, editor, toolbar
- Panel, modal, button
- Menu, dialog

### 4. Consolidation

Groups related features across versions to show evolution.

### 5. Generation

Uses Claude to transform technical bullet points into clear narrative prose.

## Troubleshooting

### No enhancements found
- Verify the version tags exist on GitHub
- Check if the release format changed
- The regex pattern may need updating

### API errors
- Verify your API key is valid
- Check you have API credits
- Ensure internet connectivity

## License

MIT License - feel free to use and modify for your needs.
