
#!/usr/bin/env python3
"""
Epstein Files Downloader
Crawls provided URLs and downloads PDF files from court document listings.
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path


def _get_logger(x):
    import logging
    return logging.getLogger(__name__ + '.' + x.__name__)


class EpsteinFilesDownloader:
    def __init__(self, output_dir='data', delay=0.1):
        """
        Initialize the downloader.

        Args:
            output_dir: Directory to save downloaded PDFs
            delay: Delay between requests in seconds (be respectful to servers)
        """
        self.log = _get_logger(EpsteinFilesDownloader)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        self.extractor = re.compile(
            r'^.*<a href="(.*/epstein/files/DataSet[% \d]+/(EFTA[\d]+.pdf))">\2</a>.*$',
            re.IGNORECASE
        )

    def extract_pdf_links(self, url):
        """
        Extract PDF links from a given URL.

        Args:
            url: URL to scrape

        Returns:
            List of PDF URLs found on the page
        """
        print(f"Fetching: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            self.log.error(f"Error fetching {url}: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        link_tags = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
        print(f'Found {len(link_tags)} <a> tags.')

        # Find all links within the specific HTML structure
        pdf_links = []
        for li in link_tags:
            self.log.debug(f"Processing link tag: {li}")
            m = self.extractor.match(str(li))
            if m:
                href = m.group(1)
                self.log.info(f"Extracted link: {href}")
                pdf_links.append(href)

        self.log.info(f"Found {len(pdf_links)} PDF links")
        return pdf_links

    def download_pdf(self, pdf_url):
        """
        Download a single PDF file.

        Args:
            pdf_url: URL of the PDF to download

        Returns:
            Path to downloaded file or None if failed
        """
        # Extract filename from URL
        filename = os.path.basename(urlparse(pdf_url).path)
        filepath = self.output_dir / filename

        # Skip if already downloaded
        if filepath.exists():
            self.log.info(f"Already exists: {filename}")
            return filepath

        self.log.info(f"Downloading: {filename}")

        try:
            response = self.session.get(pdf_url, timeout=60, stream=True)
            response.raise_for_status()

            # Write file in chunks
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.log.debug(f"Saved: {filename}")
            return filepath

        except requests.RequestException as e:
            self.log.error(f"Error downloading {filename}: {e}")
            # Clean up partial download
            if filepath.exists():
                filepath.unlink()
            return None

    def download_from_urls(self, url_list):
        """
        Download all PDFs from a list of URLs.

        Args:
            url_list: List of URLs to crawl

        Returns:
            Dictionary with statistics
        """
        stats = {
            'urls_processed': 0,
            'pdfs_found': 0,
            'pdfs_downloaded': 0,
            'pdfs_failed': 0,
            'pdfs_skipped': 0
        }

        for url in url_list:
            stats['urls_processed'] += 1

            # Extract PDF links from the page
            pdf_links = self.extract_pdf_links(url)
            stats['pdfs_found'] += len(pdf_links)

            # Download each PDF
            for pdf_url in pdf_links:
                time.sleep(self.delay)  # Be respectful to the server

                result = self.download_pdf(pdf_url)
                if result and result.exists():
                    if result.stat().st_size > 0:
                        stats['pdfs_downloaded'] += 1
                    else:
                        stats['pdfs_skipped'] += 1
                else:
                    stats['pdfs_failed'] += 1

            # Delay between pages
            time.sleep(self.delay)

        return stats


def main():
    """
    Example usage of the downloader.
    """
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    # Example URLs - replace with your actual list
    urls = [
        'https://www.justice.gov/epstein/doj-disclosures/data-set-1-files',
    ]

    # Create downloader instance
    downloader = EpsteinFilesDownloader(
        output_dir='data',
        delay=1.0  # 1 second delay between requests
    )

    print('Starting download process...')
    print(f'Output directory: {downloader.output_dir.absolute()}')
    print('-' * 60)

    #downloader.extract_pdf_links(urls[0])  # Test extraction on the first URL
    #exit(0)


    # Download from all URLs
    stats = downloader.download_from_urls(urls)

    # Print summary
    print('-' * 60)
    print('Download Summary:')
    print(f'  URLs processed: {stats['urls_processed']}')
    print(f'  PDFs found: {stats['pdfs_found']}')
    print(f'  PDFs downloaded: {stats['pdfs_downloaded']}')
    print(f'  PDFs skipped (already exist): {stats['pdfs_skipped']}')
    print(f'  PDFs failed: {stats['pdfs_failed']}')
    print(f'\nFiles saved to: {downloader.output_dir.absolute()}')


if __name__ == '__main__':
    main()
