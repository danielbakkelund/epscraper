#!/usr/bin/env python3
"""
Main orchestration module for downloading Epstein PDF files from justice.gov.

See instrs/director_instructions.md for detailed requirements.

This module coordinates the entire process:
1. Generate URLs for data sets based on start/end range
2. Scrape all data set pages to extract PDF URLs
3. Download all PDFs in a single session (CAPTCHA only needed once)

Usage:
    python src/supermain.py <start> <end>

Example:
    python src/supermain.py 1 10

This will:
- Generate URLs for data sets 1 through 10
- Scrape each page to find PDF URLs
- Download all PDFs to ./pdfs directory
"""

import sys
import os
from pathlib import Path

from epscrape.superscraper import scrape_pdf_urls
from epscrape.superdownloader import download_pdfs


def load_downloaded_datasets(filename='data/downloaded.txt'):
    """
    Load the list of already downloaded data set numbers.

    Args:
        filename: Path to the downloaded tracking file

    Returns:
        Set of data set numbers that have been downloaded
    """
    downloaded = set()
    
    if not os.path.exists(filename):
        return downloaded
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                downloaded.add(int(line))
    
    return downloaded


def save_downloaded_dataset(dataset_num, filename='data/downloaded.txt'):
    """
    Register a data set number as downloaded.

    Args:
        dataset_num: The data set number that was downloaded
        filename: Path to the downloaded tracking file
    """
    # Ensure directory exists
    Path(filename).parent.mkdir(exist_ok=True)
    
    with open(filename, 'a') as f:
        f.write(f'{dataset_num}\n')


def generate_dataset_urls(start, end, skip_downloaded=True):
    """
    Generate URLs for data sets in the specified range.

    Args:
        start: Starting data set number (inclusive)
        end: Ending data set number (inclusive)
        skip_downloaded: Whether to skip already downloaded data sets

    Returns:
        Tuple of (list of URLs to data set pages, list of dataset numbers)
    """
    base_url = "https://www.justice.gov/epstein/doj-disclosures/data-set-{}-files"
    urls = []
    dataset_numbers = []
    
    downloaded = load_downloaded_datasets() if skip_downloaded else set()
    
    for i in range(start, end + 1):
        if i in downloaded:
            print(f"  Skipping data set {i} (already downloaded)")
            continue
        urls.append(base_url.format(i))
        dataset_numbers.append(i)

    return urls, dataset_numbers


def scrape_all_pdfs(dataset_urls, dataset_numbers):
    """
    Scrape all data set pages to extract PDF URLs.

    Args:
        dataset_urls: List of data set page URLs to scrape
        dataset_numbers: List of corresponding data set numbers

    Returns:
        Dict mapping dataset number to list of PDF URLs
    """
    pdfs_by_dataset = {}

    print(f"Scraping {len(dataset_urls)} data set pages...\n")

    for i, (url, dataset_num) in enumerate(zip(dataset_urls, dataset_numbers), 1):
        print(f"[{i}/{len(dataset_urls)}] Scraping data set {dataset_num}: {url}")
        pdf_urls = scrape_pdf_urls(url)
        print(f"  Found {len(pdf_urls)} PDF URLs")
        pdfs_by_dataset[dataset_num] = pdf_urls
        print()

    return pdfs_by_dataset


def save_urls_to_file(urls, filename='data/all_pdfs.txt'):
    """
    Save PDF URLs to a file.

    Args:
        urls: List of PDF URLs
        filename: Output file path
    """
    # Ensure directory exists
    Path(filename).parent.mkdir(exist_ok=True)

    with open(filename, 'w') as f:
        for url in urls:
            f.write(f'{url}\n')

    print(f"Saved {len(urls)} PDF URLs to {filename}\n")


def main():
    """Main function to orchestrate the download process."""
    if len(sys.argv) != 3:
        print("Usage: python src/supermain.py <start> <end>")
        print()
        print("Example:")
        print("  python src/supermain.py 1 10")
        print()
        print("This will scrape data sets 1 through 10 and download all PDFs.")
        sys.exit(1)

    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except ValueError:
        print("Error: start and end must be integers")
        sys.exit(1)

    if start > end:
        print("Error: start must be less than or equal to end")
        sys.exit(1)

    print(f"=== Epstein PDF Downloader ===")
    print(f"Data sets: {start} to {end}\n")

    # Step 1: Generate data set URLs
    print("Step 1: Generating data set URLs...")
    dataset_urls, dataset_numbers = generate_dataset_urls(start, end)
    print(f"Generated {len(dataset_urls)} data set URLs to process\n")

    if not dataset_urls:
        print("All data sets in this range have already been downloaded. Exiting.")
        sys.exit(0)

    # Step 2: Scrape all pages to get PDF URLs
    print("Step 2: Scraping all data set pages for PDF URLs...")
    pdfs_by_dataset = scrape_all_pdfs(dataset_urls, dataset_numbers)
    
    total_pdfs = sum(len(urls) for urls in pdfs_by_dataset.values())
    print(f"Total PDF URLs found: {total_pdfs}\n")

    if total_pdfs == 0:
        print("No PDF URLs found. Exiting.")
        sys.exit(0)

    # Save all URLs to file for reference
    all_pdf_urls = []
    for dataset_num in dataset_numbers:
        all_pdf_urls.extend(pdfs_by_dataset[dataset_num])
    
    urls_file = 'data/all_pdfs.txt'
    save_urls_to_file(all_pdf_urls, urls_file)

    # Step 3: Download all PDFs in single session
    print("Step 3: Downloading all PDFs...")
    print("Note: You will need to click 'I am not a robot' once when prompted.\n")

    try:
        success_count = download_pdfs(urls_file, output_dir="./pdfs")

        # Register all data sets as downloaded after successful download
        print("\nRegistering downloaded data sets...")
        for dataset_num in dataset_numbers:
            save_downloaded_dataset(dataset_num)
        print(f"Registered {len(dataset_numbers)} data sets as downloaded")

        print(f"\n=== Complete ===")
        print(f"Successfully downloaded: {success_count}/{total_pdfs} PDFs")

        sys.exit(0 if success_count > 0 else 1)

    except Exception as e:
        print(f"\nError during download: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
