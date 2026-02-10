#!/usr/bin/env python3
"""
Example script demonstrating how to use superdownloader as a module.
"""

from src.superdownloader import download_pdfs

# Example 1: Download from a single file
print("Example 1: Single file")
print("-" * 50)
success_count = download_pdfs("example_urls.txt")
print(f"Downloaded {success_count} PDFs\n")

# Example 2: Download from multiple files
# print("Example 2: Multiple files")
# print("-" * 50)
# success_count = download_pdfs(["urls1.txt", "urls2.txt", "urls3.txt"])
# print(f"Downloaded {success_count} PDFs\n")

# Example 3: Specify custom output directory
# print("Example 3: Custom output directory")
# print("-" * 50)
# success_count = download_pdfs("example_urls.txt", output_dir="./custom_pdfs")
# print(f"Downloaded {success_count} PDFs\n")
