#!/usr/bin/env python3
"""
Gutenberg Release Notes Generator
Fetches multiple Gutenberg releases and generates consolidated user-facing release notes
"""

import re
import json
import requests
from typing import List, Dict, Optional
from anthropic import Anthropic

# Try to import config, fall back to defaults
try:
    from config import (
        VERSIONS, OUTPUT_FILE, DEVELOPER_KEYWORDS,
        CLAUDE_MODEL, CLAUDE_MAX_TOKENS, PROMPT_TEMPLATE
    )
except ImportError:
    # Default configuration
    VERSIONS = ["v22.0.0", "v22.1.0", "v22.2.0", "v22.3.0", "v22.4.0"]
    OUTPUT_FILE = "./release_notes.md"
    DEVELOPER_KEYWORDS = [
        'api', 'hook', 'filter', 'deprecat', 'refactor',
        'internal', 'unit test', 'e2e test', 'test coverage',
        'code quality', 'technical debt', 'types', 'typescript'
    ]
    CLAUDE_MODEL = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS = 4000
    PROMPT_TEMPLATE = """Create consolidated release notes..."""

# Configuration
GITHUB_API_BASE = "https://api.github.com/repos/WordPress/gutenberg"
ANTHROPIC_API_KEY = None  # Set via environment variable or parameter


class GutenbergReleaseProcessor:
    def __init__(self, anthropic_api_key: Optional[str] = None):
        """Initialize the processor with optional Anthropic API key"""
        self.anthropic_api_key = anthropic_api_key
        if anthropic_api_key:
            self.client = Anthropic(api_key=anthropic_api_key)
    
    def fetch_release(self, version: str) -> Dict:
        """
        Fetch a single release from GitHub API
        
        Args:
            version: Release version (e.g., "v22.3.0")
            
        Returns:
            Release data dictionary
        """
        url = f"{GITHUB_API_BASE}/releases/tags/{version}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def parse_enhancements(self, release_body: str) -> List[str]:
        """
        Extract enhancement items from release markdown body

        Args:
            release_body: The markdown body of the release

        Returns:
            List of enhancement items with their subsection context
        """
        enhancements = []

        # Normalize line endings to \n only
        release_body = release_body.replace('\r\n', '\n').replace('\r', '\n')

        # Developer-only subsection headers to filter out
        developer_subsections = [
            'data layer', 'code quality', 'build tooling', 'testing',
            'documentation', 'tools', 'packages', 'tooling'
        ]

        # Try to find Enhancements section (could be ## or ### level)
        # Pattern: ### Enhancements ... until next ### or ## section
        # Use negative lookahead (?!#) to match exactly 2 or 3 hashes, not more
        pattern = r'###\s*Enhancements\s*(.*?)(?=\n###(?!#)|\n##(?!#)|\Z)'
        match = re.search(pattern, release_body, re.DOTALL | re.IGNORECASE)

        if not match:
            # Fallback to ## Enhancements if ### not found
            pattern = r'##\s*Enhancements\s*(.*?)(?=\n##(?!#)|\Z)'
            match = re.search(pattern, release_body, re.DOTALL | re.IGNORECASE)

        if not match:
            return enhancements

        enhancements_section = match.group(1)

        # Parse line by line, tracking current subsection
        current_subsection = None
        lines = enhancements_section.split('\n')

        for line in lines:
            # Check for subsection header (#### SubsectionName)
            subsection_match = re.match(r'^\s*####\s+(.+)$', line)
            if subsection_match:
                current_subsection = subsection_match.group(1).strip()
                continue

            # Extract bullet points (lines starting with - or *)
            bullet_match = re.match(r'^[\s]*[-*]\s+(.+)$', line)
            if bullet_match:
                item = bullet_match.group(1).strip()

                # Skip items from developer-only subsections
                if current_subsection:
                    subsection_lower = current_subsection.lower()
                    if any(dev_section in subsection_lower for dev_section in developer_subsections):
                        continue

                enhancements.append(item)

        return enhancements
    
    def is_user_facing(self, enhancement: str) -> bool:
        """
        Determine if an enhancement is user-facing
        
        Args:
            enhancement: Enhancement text
            
        Returns:
            True if user-facing, False if developer-only
        """
        enhancement_lower = enhancement.lower()
        
        # Check for developer keywords from config
        for keyword in DEVELOPER_KEYWORDS:
            if keyword in enhancement_lower:
                return False
        
        return True
    
    def fetch_multiple_releases(self, versions: List) -> List[Dict]:
        """
        Fetch multiple releases and extract enhancements

        Args:
            versions: List of version strings or dicts with file paths
                     e.g., ["v22.0.0", {"file": "path/to/file.md", "version": "v22.4.0"}]

        Returns:
            List of dictionaries with version and enhancements
        """
        all_data = []

        for version_entry in versions:
            # Check if it's a local file or API version
            if isinstance(version_entry, dict) and 'file' in version_entry:
                # Load from local file
                version = version_entry['version']
                file_path = version_entry['file']
                print(f"Loading {version} from local file: {file_path}...")
                try:
                    all_data.append(self._load_from_local_file(file_path, version))
                    print(f"  Found {len(all_data[-1]['enhancements'])} user-facing enhancements")
                except Exception as e:
                    print(f"  Error loading {version} from file: {e}")
            else:
                # Fetch from GitHub API
                version = version_entry
                print(f"Fetching {version}...")
                try:
                    release = self.fetch_release(version)
                    enhancements = self.parse_enhancements(release['body'])

                    # Filter for user-facing enhancements
                    user_enhancements = [
                        e for e in enhancements
                        if self.is_user_facing(e)
                    ]

                    all_data.append({
                        'version': version,
                        'name': release.get('name', version),
                        'published_at': release.get('published_at', ''),
                        'enhancements': user_enhancements
                    })

                    print(f"  Found {len(user_enhancements)} user-facing enhancements")

                except Exception as e:
                    print(f"  Error fetching {version}: {e}")

        return all_data

    def _load_from_local_file(self, file_path: str, version: str) -> Dict:
        """
        Load changelog from a local markdown file

        Args:
            file_path: Path to the local changelog file
            version: Version string (e.g., "v22.4.0")

        Returns:
            Dictionary with version and enhancements
        """
        import os

        # Expand user home directory
        expanded_path = os.path.expanduser(file_path)

        # Read the file
        with open(expanded_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse enhancements from the file
        enhancements = self.parse_enhancements(content)

        # Filter for user-facing enhancements
        user_enhancements = [
            e for e in enhancements
            if self.is_user_facing(e)
        ]

        return {
            'version': version,
            'name': version,
            'published_at': '',
            'enhancements': user_enhancements
        }

    def generate_consolidated_notes(self, releases_data: List[Dict]) -> str:
        """
        Use Claude API to generate consolidated release notes
        
        Args:
            releases_data: List of release data with enhancements
            
        Returns:
            Consolidated release notes as a string
        """
        if not self.anthropic_api_key:
            raise ValueError("Anthropic API key required for generating notes")
        
        # Prepare the context for Claude
        context = self._format_context_for_claude(releases_data)
        
        # Use prompt from config
        prompt = PROMPT_TEMPLATE.format(context=context)

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def _format_context_for_claude(self, releases_data: List[Dict]) -> str:
        """Format releases data into a readable context for Claude"""
        context_parts = []
        
        for release in releases_data:
            version = release['version']
            enhancements = release['enhancements']
            
            context_parts.append(f"### {version}")
            if enhancements:
                for enhancement in enhancements:
                    context_parts.append(f"- {enhancement}")
            else:
                context_parts.append("(No user-facing enhancements)")
            context_parts.append("")  # Blank line
        
        return "\n".join(context_parts)
    
    def save_notes(self, notes: str, output_file: str):
        """Save release notes to a file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(notes)
        print(f"\nRelease notes saved to: {output_file}")


def main():
    """Main execution function"""
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set. Will fetch data but cannot generate notes.")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
    
    # Initialize processor
    processor = GutenbergReleaseProcessor(anthropic_api_key=api_key)
    
    print("=" * 60)
    print("Gutenberg Release Notes Generator")
    print("=" * 60)

    # Format version list for display
    version_list = [
        v if isinstance(v, str) else v['version']
        for v in VERSIONS
    ]
    print(f"Processing versions: {', '.join(version_list)}\n")
    
    # Fetch releases
    releases_data = processor.fetch_multiple_releases(VERSIONS)
    
    # Save raw data for inspection
    with open('./releases_data.json', 'w') as f:
        json.dump(releases_data, f, indent=2)
    print("\nRaw data saved to: releases_data.json")
    
    # Generate consolidated notes if API key is available
    if api_key:
        print("\nGenerating consolidated release notes with Claude...")
        try:
            consolidated_notes = processor.generate_consolidated_notes(releases_data)
            processor.save_notes(consolidated_notes, OUTPUT_FILE)
            
            # Print a preview
            print("\n" + "=" * 60)
            print("PREVIEW OF GENERATED NOTES:")
            print("=" * 60)
            print(consolidated_notes[:500] + "..." if len(consolidated_notes) > 500 else consolidated_notes)
            
        except Exception as e:
            print(f"Error generating notes: {e}")
    else:
        print("\nSkipping note generation (no API key). Raw data available in releases_data.json")


if __name__ == "__main__":
    main()
