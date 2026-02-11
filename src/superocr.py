#!/usr/bin/env python3
"""
OCR Program for extracting text from PDFs

This module is created according to instructions in:
instrs/ocr_instructions.md

Workflow:
1. Reads PDF files from the directory `pdfs`
2. Uses the module `src.ocr` to perform OCR
3. Outputs text files to `texts` directory with .txt extension
4. Skips already converted files
5. Marks empty/image-only files as "empty file"
"""

import os
import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from ocr import get_text_from_pdf

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_pdf(pdf_path, output_dir, language='eng'):
    """
    Process a single PDF file and extract text using OCR.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the text output
        language: Language code for Tesseract (default: 'eng')

    Returns:
        True if processed successfully, False if skipped
    """
    pdf_file = Path(pdf_path)
    output_file = Path(output_dir) / (pdf_file.stem + '.txt')

    # Check if already converted
    if output_file.exists():
        logger.info(f'Skipping {pdf_file.name} - already converted')
        return False

    logger.info(f'Processing {pdf_file.name}...')

    try:
        # Log before starting conversion to identify hangs
        logger.info(f'Starting OCR conversion for {pdf_file.name}')
        # Extract text using OCR
        text = get_text_from_pdf(str(pdf_path), language)

        # Check if meaningful text was extracted
        # Strip whitespace and check if there's actual content
        clean_text = text.strip()
        if not clean_text or len(clean_text) < 10:
            logger.warning(f'{pdf_file.name} appears to be empty or image-only')
            text = 'empty file'

        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

        logger.info(f'Successfully converted {pdf_file.name} to {output_file.name}')
        return True

    except Exception as e:
        logger.error(f'Error processing {pdf_file.name}: {e}')
        # Write error marker
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('empty file')
        return False


def process_all_pdfs(pdf_dir='pdfs', output_dir='texts', language='eng', num_cores=5):
    """
    Process all PDF files in the specified directory.

    Args:
        pdf_dir: Directory containing PDF files (default: 'pdfs')
        output_dir: Directory to save text outputs (default: 'texts')
        language: Language code for Tesseract (default: 'eng')
        num_cores: Number of parallel processes (default: 5)

    Returns:
        Dictionary with processing statistics
    """
    pdf_path = Path(pdf_dir)
    output_path = Path(output_dir)

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Get all PDF files
    pdf_files = list(pdf_path.glob('*.pdf'))

    if not pdf_files:
        logger.warning(f'No PDF files found in {pdf_dir}')
        return {'total': 0, 'processed': 0, 'skipped': 0}

    logger.info(f'Found {len(pdf_files)} PDF files in {pdf_dir}')
    logger.info(f'Processing with {num_cores} parallel cores')

    processed = 0
    skipped = 0

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Submit all tasks
        future_to_pdf = {
            executor.submit(process_pdf, pdf_file, output_path, language): pdf_file
            for pdf_file in sorted(pdf_files)
        }

        # Process results as they complete
        for future in as_completed(future_to_pdf):
            if future.result():
                processed += 1
            else:
                skipped += 1

    stats = {
        'total': len(pdf_files),
        'processed': processed,
        'skipped': skipped
    }

    logger.info(f'Processing complete: {processed} processed, {skipped} skipped')
    return stats


def main():
    """
    Command line entry point.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='OCR processing for PDF files'
    )
    parser.add_argument(
        '--pdf-dir',
        default='pdfs',
        help='Directory containing PDF files (default: pdfs)'
    )
    parser.add_argument(
        '--output-dir',
        default='texts',
        help='Directory for text output (default: texts)'
    )
    parser.add_argument(
        '--language',
        default='eng',
        help='Language code for OCR (default: eng)'
    )
    parser.add_argument(
        '--cores',
        type=int,
        default=5,
        help='Number of parallel cores to use (default: 5)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    stats = process_all_pdfs(args.pdf_dir, args.output_dir, args.language, args.cores)

    print(f'\nSummary:')
    print(f'  Total PDFs: {stats["total"]}')
    print(f'  Processed: {stats["processed"]}')
    print(f'  Skipped: {stats["skipped"]}')


if __name__ == '__main__':
    main()
