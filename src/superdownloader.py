#!/usr/bin/env python3
"""
PDF Downloader for justice.gov Epstein files.

This module provides functionality to download PDFs from justice.gov that require
age verification and CAPTCHA handling. It uses undetected Chrome to bypass bot
detection and maintains session cookies across multiple downloads.

Public API:
    download_pdfs(url_files, output_dir="./pdfs", headless=False)
        Main function to download PDFs from one or more URL files.
    
    PDFDownloader(output_dir="./pdfs", headless=False)
        Context manager class for advanced usage.

Example:
    >>> from src.superdownloader import download_pdfs
    >>> count = download_pdfs("urls.txt")
    >>> count = download_pdfs(["urls1.txt", "urls2.txt"])

Command-line usage:
    python src/superdownloader.py urls1.txt urls2.txt
"""

import os
import sys
import time
import ssl
from urllib.parse import urlparse, unquote
from pathlib import Path

# Workaround for SSL certificate issues on macOS
ssl._create_default_https_context = ssl._create_unverified_context

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


__all__ = ['download_pdfs', 'PDFDownloader']


class PDFDownloader:
    def __init__(self, output_dir="./pdfs", headless=False):
        """
        Initialize PDF downloader.
        
        Args:
            output_dir: Directory to save downloaded PDFs
            headless: Run browser in headless mode (currently not supported due to Chrome limitations)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.headless = headless
        self.driver = None
        
    def __enter__(self):
        """Context manager entry."""
        options = uc.ChromeOptions()
        if self.headless:
            # Use old headless mode as new one has issues
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
        
    def extract_filename(self, url):
        """Extract the PDF filename from the URL."""
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]
        # Decode URL encoding (e.g., %20 -> space)
        filename = unquote(filename)
        return filename
    
    def download_pdf(self, url):
        """Download a single PDF, handling age verification."""
        filename = self.extract_filename(url)
        output_path = self.output_dir / filename
        
        print(f"Downloading: {url}")
        print(f"  -> {output_path}")
        
        try:
            # Navigate to the URL
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Check if we're on the age verification page by looking for the button
            try:
                yes_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "age-button-yes"))
                )
                print(f"  Age verification required, clicking 'Yes' button...")
                yes_button.click()
                
                # Wait for the page to process the click and set cookies
                time.sleep(5)
                
                # Navigate to the PDF again
                print(f"  Accessing PDF...")
                self.driver.get(url)
                time.sleep(3)
                
            except Exception as e:
                print(f"  No age verification required (or button not found)")
            
            # Get the page source to check if it's PDF or HTML
            page_source = self.driver.page_source
            
            # If we still have HTML, try getting the content via requests with the cookies
            if '<html' in page_source.lower():
                print(f"  Getting PDF with session cookies...")
                import requests
                
                # Get cookies from Selenium
                cookies = self.driver.get_cookies()
                session = requests.Session()
                for cookie in cookies:
                    session.cookies.set(cookie['name'], cookie['value'])
                
                # Download the PDF
                response = session.get(url)
                
                if response.status_code == 200 and response.content.startswith(b'%PDF'):
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Downloaded successfully ({len(response.content)} bytes)")
                    return True
                else:
                    print(f"  ✗ Error: Not a valid PDF (status: {response.status_code}, size: {len(response.content)})")
                    return False
            else:
                # We might have gotten the PDF directly in the page_source (unlikely)
                print(f"  ✗ Error: Unexpected content type")
                return False
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def download_from_file(self, url_file):
        """Download all PDFs from a file containing URLs (one per line)."""
        urls = []
        with open(url_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        
        print(f"Found {len(urls)} URLs to download\n")
        
        success_count = 0
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}]")
            if self.download_pdf(url):
                success_count += 1
            print()
        
        print(f"Complete: {success_count}/{len(urls)} downloaded successfully")
        return success_count
    
    def download_from_multiple_files(self, url_files):
        """Download all PDFs from multiple files, reusing browser session."""
        all_urls = []
        
        # Collect all URLs from all files
        for url_file in url_files:
            print(f"Reading URLs from: {url_file}")
            with open(url_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        all_urls.append(line)
        
        print(f"\nFound {len(all_urls)} total URLs to download\n")
        
        success_count = 0
        for i, url in enumerate(all_urls, 1):
            print(f"[{i}/{len(all_urls)}]")
            if self.download_pdf(url):
                success_count += 1
            print()
        
        print(f"Complete: {success_count}/{len(all_urls)} downloaded successfully")
        return success_count


def download_pdfs(url_files, output_dir="./pdfs", headless=False):
    """
    Download PDFs from one or more URL files.
    
    Args:
        url_files: String path to a single file, or list of file paths
        output_dir: Directory to save downloaded PDFs (default: "./pdfs")
        headless: Run browser in headless mode (default: False, experimental)
    
    Returns:
        int: Number of successfully downloaded PDFs
    
    Example:
        >>> from src.superdownloader import download_pdfs
        >>> download_pdfs("urls.txt")
        >>> download_pdfs(["urls1.txt", "urls2.txt", "urls3.txt"])
        >>> download_pdfs(["urls.txt"], output_dir="./my_pdfs")
    """
    # Normalize input to list
    if isinstance(url_files, str):
        url_files = [url_files]
    
    # Validate all files exist
    for url_file in url_files:
        if not os.path.exists(url_file):
            raise FileNotFoundError(f"URL file not found: {url_file}")
    
    # Download using context manager
    with PDFDownloader(output_dir=output_dir, headless=headless) as downloader:
        if len(url_files) == 1:
            return downloader.download_from_file(url_files[0])
        else:
            return downloader.download_from_multiple_files(url_files)


def main():
    if len(sys.argv) < 2:
        print("Usage: python superdownloader.py <url_file> [url_file2 ...] [--headless]")
        print("  url_file: Text file(s) containing URLs, one per line")
        print("  --headless: Optional flag to run in headless mode (experimental, may not work)")
        print("\nExamples:")
        print("  python superdownloader.py urls.txt")
        print("  python superdownloader.py urls1.txt urls2.txt urls3.txt")
        print("\nNote: By default, the browser runs in visible mode due to Chrome/Selenium limitations.")
        print("When processing multiple files, you only need to pass the CAPTCHA once at the start.")
        sys.exit(1)
    
    # Separate file arguments from flags
    headless = "--headless" in sys.argv
    url_files = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    if not url_files:
        print("Error: No URL files specified")
        sys.exit(1)
    
    # Check all files exist
    for url_file in url_files:
        if not os.path.exists(url_file):
            print(f"Error: File '{url_file}' not found")
            sys.exit(1)
    
    # Use the public API function
    try:
        success_count = download_pdfs(url_files, headless=headless)
        sys.exit(0 if success_count > 0 else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
