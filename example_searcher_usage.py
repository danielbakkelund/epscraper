#!/usr/bin/env python3
"""
Example usage of the supersearcher module.

This demonstrates how to use supersearcher programmatically.
"""

import sys
import os

# Add src to path if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from supersearcher import search_pdfs, PDFSearcher


def example_basic_search():
    """Basic search example."""
    print('=' * 60)
    print('Example 1: Basic search')
    print('=' * 60)
    
    # Search and save to default location: data/<search>_urls.txt
    urls = search_pdfs('epstein')
    
    print(f'\nFound {len(urls)} URLs')
    if urls:
        print('First 3 URLs:')
        for url in urls[:3]:
            print(f'  {url}')


def example_custom_output():
    """Search with custom output file."""
    print('\n' + '=' * 60)
    print('Example 2: Search with custom output file')
    print('=' * 60)
    
    # Search and save to custom location
    urls = search_pdfs('maxwell', 'data/maxwell_search.txt')
    
    print(f'\nFound {len(urls)} URLs saved to data/maxwell_search.txt')


def example_advanced_usage():
    """Advanced usage with PDFSearcher context manager."""
    print('\n' + '=' * 60)
    print('Example 3: Advanced usage with context manager')
    print('=' * 60)
    
    with PDFSearcher() as searcher:
        # You can perform multiple searches with the same browser instance
        urls1 = searcher.search_and_extract('documents')
        print(f'Search 1 found {len(urls1)} URLs')
        
        # Could do another search here if needed
        # urls2 = searcher.search_and_extract('another term')


if __name__ == '__main__':
    print('Supersearcher Module Examples')
    print('Note: These examples will open a browser window')
    print()
    
    # Run only one example to avoid opening multiple browsers
    # Uncomment the one you want to test
    
    example_basic_search()
    # example_custom_output()
    # example_advanced_usage()
