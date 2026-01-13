# Gutenberg Release Notes Generator - Project Structure

```
gutenberg-release-notes/
│
├── gutenberg_release_notes.py   # Main script
├── config.py                     # Configuration file
├── test_parsing.py              # Test script with sample data
├── requirements.txt             # Python dependencies
│
├── README.md                    # Full documentation
├── QUICKSTART.md               # Quick start guide
└── PROJECT_STRUCTURE.md        # This file
```

## File Descriptions

### gutenberg_release_notes.py
The main Python script containing:
- `GutenbergReleaseProcessor` class
- GitHub API integration
- Enhancement parsing logic
- User-facing filter
- Claude API integration for note generation

**Key Methods:**
- `fetch_release()` - Fetches single release from GitHub
- `parse_enhancements()` - Extracts Enhancement section
- `is_user_facing()` - Filters developer-only items
- `fetch_multiple_releases()` - Batch processing
- `generate_consolidated_notes()` - Claude API call
- `main()` - Entry point

### config.py
Centralized configuration:
- Version list to process
- Output file path
- Developer keywords for filtering
- Claude API settings
- Prompt template

**Easily customizable** - just edit this file!

### test_parsing.py
Standalone test script that:
- Demonstrates parsing logic
- Shows filtering behavior
- Uses sample data (no API calls needed)

Run: `python test_parsing.py`

### requirements.txt
Python package dependencies:
- `requests` - HTTP library for GitHub API
- `anthropic` - Official Anthropic SDK

### README.md
Comprehensive documentation covering:
- Features
- Installation
- Usage
- How it works
- Customization
- Limitations

### QUICKSTART.md
Step-by-step guide for:
- First-time setup
- Running the script
- Viewing results
- Common troubleshooting

## Workflow

```
1. User runs script
   ↓
2. Script fetches releases from GitHub API
   ↓
3. Parses Enhancement sections
   ↓
4. Filters for user-facing changes
   ↓
5. Sends to Claude API
   ↓
6. Receives consolidated notes
   ↓
7. Saves to markdown file
```

## Extending the Project

### Add new sections (beyond Enhancements)
Modify `parse_enhancements()` to accept section name:
```python
def parse_section(self, release_body: str, section_name: str):
    pattern = rf'## {section_name}\s*(.*?)(?=\n##|\Z)'
    # ...
```

### Add GitHub authentication
Add to config:
```python
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
```

Update fetch_release():
```python
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
response = requests.get(url, headers=headers)
```

### Export to different formats
Add methods like:
- `export_to_html()`
- `export_to_pdf()`
- `export_to_json()`

### Add a web interface
Use Flask or FastAPI:
```python
@app.post("/generate")
async def generate_notes(versions: List[str]):
    processor = GutenbergReleaseProcessor()
    # ...
```

## Testing Strategy

1. **Unit tests**: Test individual methods
2. **Integration tests**: Test full workflow with mock API
3. **Manual testing**: Run `test_parsing.py`

## Environment Requirements

- Python 3.7+
- Internet access to:
  - api.github.com (GitHub API)
  - api.anthropic.com (Claude API)
- Anthropic API key

## Performance Considerations

- GitHub API: Rate limited to 60 requests/hour (unauthenticated)
- Claude API: Depends on your plan
- Each run makes N+1 API calls (N releases + 1 Claude call)
- Consider caching GitHub responses for repeated runs
