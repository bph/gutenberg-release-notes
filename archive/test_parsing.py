#!/usr/bin/env python3
"""
Test script to demonstrate parsing logic with sample release data
"""

from gutenberg_release_notes import GutenbergReleaseProcessor

# Sample release body (mimicking GitHub release format)
SAMPLE_RELEASE_BODY = """
# Gutenberg 22.3.0

## Changelog

### Features

Some new features here.

## Enhancements

- Add support for custom spacing in List block. ([68123](https://github.com/WordPress/gutenberg/pull/68123))
- Improve accessibility of the block toolbar. ([68045](https://github.com/WordPress/gutenberg/pull/68045))
- Add new API endpoint for block patterns. ([67890](https://github.com/WordPress/gutenberg/pull/67890))
- Enhance List View drag and drop behavior. ([68200](https://github.com/WordPress/gutenberg/pull/68200))
- Refactor internal block registration hooks. ([68150](https://github.com/WordPress/gutenberg/pull/68150))
- Add unit tests for block validation. ([68100](https://github.com/WordPress/gutenberg/pull/68100))

## Bug Fixes

Various bug fixes here.

## Documentation

Docs updates.
"""

def test_parsing():
    """Test the parsing and filtering logic"""
    processor = GutenbergReleaseProcessor()
    
    print("=" * 60)
    print("Testing Enhancement Extraction and Filtering")
    print("=" * 60)
    
    # Parse enhancements
    enhancements = processor.parse_enhancements(SAMPLE_RELEASE_BODY)
    
    print(f"\nTotal enhancements found: {len(enhancements)}")
    print("\nAll enhancements:")
    for i, enhancement in enumerate(enhancements, 1):
        print(f"{i}. {enhancement}")
    
    # Filter for user-facing
    user_facing = [e for e in enhancements if processor.is_user_facing(e)]
    developer_only = [e for e in enhancements if not processor.is_user_facing(e)]
    
    print(f"\n\nUser-facing enhancements: {len(user_facing)}")
    for i, enhancement in enumerate(user_facing, 1):
        print(f"{i}. {enhancement}")
    
    print(f"\n\nDeveloper-only (filtered out): {len(developer_only)}")
    for i, enhancement in enumerate(developer_only, 1):
        print(f"{i}. {enhancement}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_parsing()
