#!/usr/bin/env python3
"""
PDF Search Module for justice.gov Epstein files.

See instrs/searcher_instructions.md for detailed requirements.

This module provides functionality to search for PDFs on the justice.gov/epstein
site and extract PDF URLs from the search results. It uses undetected Chrome to
handle JavaScript-based search functionality and age verification.

Public API:
    search_pdfs(search_string, output_file=None)
        Main function to search and extract PDF URLs.
    
    PDFSearcher()
        Context manager class for advanced usage.

Example:
    >>> from supersearcher import search_pdfs
    >>> urls = search_pdfs('flight logs')
    >>> urls = search_pdfs('black book', 'data/custom_urls.txt')

Command-line usage:
    python src/supersearcher.py "search terms"
    python src/supersearcher.py "search terms" --output data/custom.txt
"""

import os
import sys
import time
import ssl
from pathlib import Path

# Workaround for SSL certificate issues on macOS
ssl._create_default_https_context = ssl._create_unverified_context

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


__all__ = ['search_pdfs', 'PDFSearcher']


class PDFSearcher:
    """
    Context manager for searching and extracting PDF URLs from justice.gov/epstein.
    
    Handles browser automation, age verification, search execution, and pagination.
    """
    
    def __init__(self, headless=False):
        """
        Initialize PDF searcher.
        
        Args:
            headless: Run browser in headless mode (currently not fully supported)
        """
        self.headless = headless
        self.driver = None
        self.search_url = 'https://www.justice.gov/epstein/search'
        
    def __enter__(self):
        """Context manager entry."""
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        
        # Use version 144 to match current Chrome
        self.driver = uc.Chrome(options=options, version_main=144)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        if self.driver:
            self.driver.quit()
    
    def handle_age_verification(self):
        """Handle age verification if present."""
        try:
            yes_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, 'age-button-yes'))
            )
            print('Age verification required, clicking "Yes" button...')
            yes_button.click()
            time.sleep(1)
            return True
        except TimeoutException:
            print('No age verification required')
            return False
    
    def perform_search(self, search_string):
        """
        Enter search string and click search button.
        
        Args:
            search_string: The search query to execute
        """
        print(f'Performing search for: "{search_string}"')
        
        # Find search input field
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'searchInput'))
            )
            search_input.clear()
            search_input.send_keys(search_string)
            
            # Click search button
            search_button = self.driver.find_element(By.ID, 'searchButton')
            search_button.click()
            
            # Wait for results to load
            print('Waiting for search results to load...')
            time.sleep(3)
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f'Error performing search: {e}')
            raise
    
    def extract_pdf_urls(self):
        """
        Extract PDF URLs from the current results page.
        
        Returns:
            List of PDF URLs found on the page
        """
        pdf_urls = []
        
        try:
            # Wait for results container
            results_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'results'))
            )
            
            # Find all links in the results
            links = results_container.find_elements(By.TAG_NAME, 'a')
            
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and href.endswith('.pdf'):
                        pdf_urls.append(href)
                except Exception as e:
                    continue
            
            print(f'Found {len(pdf_urls)} PDF URLs on this page')
            
        except TimeoutException:
            print('No results found or results did not load')
        
        return pdf_urls
    
    def has_next_page(self):
        """
        Check if there is a next page button available.
        
        Returns:
            True if next page exists, False otherwise
        """
        try:
            # Look for pagination container
            pagination = self.driver.find_element(By.ID, 'pagination')
            
            # Look for a "next" button or link that's not disabled
            # Common patterns: button with text "Next", ">" or arrow
            next_buttons = pagination.find_elements(By.TAG_NAME, 'button')
            
            for button in next_buttons:
                text = button.text.lower()
                if 'next' in text or '>' in text or '›' in text or '»' in text:
                    # Check if button is enabled
                    if button.is_enabled() and button.get_attribute('disabled') is None:
                        return True
            
            # Also check for links
            next_links = pagination.find_elements(By.TAG_NAME, 'a')
            for link in next_links:
                text = link.text.lower()
                if 'next' in text or '>' in text or '›' in text or '»' in text:
                    return True
            
            return False
            
        except NoSuchElementException:
            return False
    
    def click_next_page(self):
        """Click the next page button."""
        try:
            pagination = self.driver.find_element(By.ID, 'pagination')
            
            # Try buttons first
            next_buttons = pagination.find_elements(By.TAG_NAME, 'button')
            for button in next_buttons:
                text = button.text.lower()
                if 'next' in text or '>' in text or '›' in text or '»' in text:
                    if button.is_enabled() and button.get_attribute('disabled') is None:
                        print('Clicking next page...')
                        # Scroll to button and use JavaScript click to avoid interception
                        self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', button)
                        time.sleep(0.5)
                        try:
                            button.click()
                        except Exception:
                            # Fallback to JavaScript click
                            self.driver.execute_script('arguments[0].click();', button)
                        time.sleep(3)
                        return True
            
            # Try links
            next_links = pagination.find_elements(By.TAG_NAME, 'a')
            for link in next_links:
                text = link.text.lower()
                if 'next' in text or '>' in text or '›' in text or '»' in text:
                    print('Clicking next page...')
                    # Scroll to link and use JavaScript click
                    self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', link)
                    time.sleep(0.5)
                    try:
                        link.click()
                    except Exception:
                        # Fallback to JavaScript click
                        self.driver.execute_script('arguments[0].click();', link)
                    time.sleep(3)
                    return True
            
            return False
            
        except Exception as e:
            print(f'Error clicking next page: {e}')
            return False
    
    def search_and_extract(self, search_string):
        """
        Perform search and extract all PDF URLs across all pages.
        
        Args:
            search_string: The search query
            
        Returns:
            List of all PDF URLs found
        """
        all_urls = []
        
        # Navigate to search page
        print(f'Navigating to {self.search_url}...')
        self.driver.get(self.search_url)
        time.sleep(2)
        
        # Handle age verification
        self.handle_age_verification()
        
        # Perform the search
        self.perform_search(search_string)
        
        # Extract URLs from first page
        page_num = 1
        urls = self.extract_pdf_urls()
        all_urls.extend(urls)
        
        # Check for additional pages
        while self.has_next_page():
            page_num += 1
            print(f'\nMoving to page {page_num}...')
            
            if not self.click_next_page():
                break
            
            urls = self.extract_pdf_urls()
            all_urls.extend(urls)
        
        print(f'\nTotal PDF URLs found: {len(all_urls)}')
        return all_urls


def save_urls_to_file(urls, filename):
    """
    Save URLs to a file, one per line.
    
    Args:
        urls: List of URLs to save
        filename: Output file path
    """
    # Ensure the data directory exists
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(filename, 'a') as f:
            for url in urls:
                f.write(f'{url}\n')
        print(f'Appended {len(urls)} URLs to {filename}')
    except IOError as e:
        print(f'Error writing to file {filename}: {e}')


def search_pdfs(search_string, output_file=None, headless=False):
    """
    Search for PDFs and extract URLs.
    
    Args:
        search_string: The search query
        output_file: Optional output file path. If not provided, uses
                    'data/<search_string>_urls.txt' with spaces replaced by underscores
        headless: Run browser in headless mode (default: False)
    
    Returns:
        List of PDF URLs found
    
    Example:
        >>> from supersearcher import search_pdfs
        >>> urls = search_pdfs('flight logs')
        >>> urls = search_pdfs('black book', 'data/custom_urls.txt')
    """
    # Generate default output filename if not provided
    if output_file is None:
        safe_search_string = search_string.replace(' ', '_')
        output_file = f'data/{safe_search_string}_urls.txt'
    
    print(f'Search query: "{search_string}"')
    print(f'Output file: {output_file}\n')
    
    with PDFSearcher(headless=headless) as searcher:
        urls = searcher.search_and_extract(search_string)
        
        if urls:
            save_urls_to_file(urls, output_file)
        else:
            print('No PDF URLs found')
        
        return urls


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        print('Usage: python supersearcher.py <search_string> [--output <file>] [--headless]')
        print('  search_string: The search query (use quotes for multi-word queries)')
        print('  --output: Optional output file path (default: data/<search_string>_urls.txt)')
        print('  --headless: Optional flag to run in headless mode')
        print('\nExamples:')
        print('  python supersearcher.py "flight logs"')
        print('  python supersearcher.py "black book" --output data/blackbook.txt')
        sys.exit(0 if len(sys.argv) > 1 else 1)
    
    # Parse arguments
    search_string = sys.argv[1]
    output_file = None
    headless = '--headless' in sys.argv
    
    # Check for custom output file
    if '--output' in sys.argv:
        try:
            output_index = sys.argv.index('--output')
            output_file = sys.argv[output_index + 1]
        except (ValueError, IndexError):
            print('Error: --output flag requires a filename')
            sys.exit(1)
    
    try:
        urls = search_pdfs(search_string, output_file, headless)
        sys.exit(0 if urls else 1)
    except Exception as e:
        print(f'Fatal error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
