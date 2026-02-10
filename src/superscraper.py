"""
Web scraper module for extracting PDF URLs from HTML pages.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def scrape_pdf_urls(url):
    """
    Scrape PDF URLs from a given web page.
    
    Args:
        url: The URL to scrape
        
    Returns:
        A list of full PDF URLs found on the page
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Error fetching URL {url}: {e}')
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_urls = []
    
    # Find all anchor tags
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Check if the link points to a PDF file
        if href.endswith('.pdf'):
            # Convert relative URLs to absolute URLs
            full_url = urljoin(url, href)
            pdf_urls.append(full_url)
    
    return pdf_urls


def save_urls_to_file(urls, filename='data/urls.txt'):
    """
    Save a list of URLs to a file, one URL per line.
    
    Args:
        urls: List of URLs to save
        filename: Output file path (default: 'data/urls.txt')
    """
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(f'{url}\n')
        print(f'Saved {len(urls)} URLs to {filename}')
    except IOError as e:
        print(f'Error writing to file {filename}: {e}')


def scrape_and_save(url, filename='data/urls.txt'):
    """
    Scrape PDF URLs from a webpage and save them to a file.
    
    Args:
        url: The URL to scrape
        filename: Output file path (default: 'data/urls.txt')
        
    Returns:
        List of PDF URLs found
    """
    print(f'Scraping {url}...')
    urls = scrape_pdf_urls(url)
    print(f'Found {len(urls)} PDF URLs')
    
    if urls:
        save_urls_to_file(urls, filename)
    
    return urls


def main():
    """Main function to demonstrate the scraper."""
    test_url = 'https://www.justice.gov/epstein/doj-disclosures/data-set-5-files'
    
    urls = scrape_and_save(test_url)
    
    if urls:
        print(f'\nFirst 5 URLs:')
        for url in urls[:5]:
            print(f'  {url}')
    

if __name__ == '__main__':
    main()
