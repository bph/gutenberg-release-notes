# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Your API Key

```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

Get your API key from: https://console.anthropic.com/

## Step 3: Run the Script

### Default Usage (processes v22.0.0 to v22.3.0):
```bash
python gutenberg_release_notes.py
```

### Custom Versions:

Edit `config.py` and change the VERSIONS list:
```python
VERSIONS = [
    "v21.0.0",
    "v21.1.0", 
    "v21.2.0",
]
```

Then run:
```bash
python gutenberg_release_notes.py
```

## Step 4: View Results

The script generates two files:
1. `releases_data.json` - Raw extracted data
2. `release_notes_22.0-22.3.md` - Your consolidated release notes!

## Example Output

The release notes will look something like:

```markdown
# Gutenberg 22.x Release Notes

## Editor Experience Improvements

The block editor received significant performance enhancements across 
versions 22.0-22.2, with page load times reduced by up to 30%...

## List View Enhancements

Starting in version 22.1 and continuing through 22.3, the List View 
gained new drag-and-drop capabilities...
```

## Troubleshooting

**"ANTHROPIC_API_KEY not set"**
- Make sure you've exported the environment variable
- Check that you're in the same terminal session

**"Error fetching vX.X.X"**
- Verify the version exists on GitHub
- Check your internet connection
- GitHub API has rate limits (60/hour without auth)

**Network issues in restricted environments**
- The script requires access to:
  - api.github.com
  - api.anthropic.com

## Customization Tips

### Change the output style:
Edit the `PROMPT_TEMPLATE` in `config.py`

### Filter different types of changes:
Modify `DEVELOPER_KEYWORDS` in `config.py` to adjust what gets filtered

### Process different version ranges:
Update the `VERSIONS` list in `config.py`
