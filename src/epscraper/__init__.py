"""
Epstein Files - Search, Download & OCR Package

Main functions:
- search_and_download: Search for PDFs and download them
- process_all_pdfs: Extract text from PDFs using OCR
"""

from epscraper.search_and_download import search_and_download
from epscraper.superocr import process_all_pdfs

__all__ = ['search_and_download', 'process_all_pdfs']
