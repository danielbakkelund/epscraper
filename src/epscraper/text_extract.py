'''

Requires:

brew install tesseract tesseract-lang

'''


def _get_logger(x):
    import logging
    return logging.getLogger(__name__ + '.' + x.__name__)


def get_text_from_pdf(pdf_path,language):
    '''
    Converts a (non-extractable) pdf to text via optical
    image to text transformation. Also supports scanned documents.
    pdf_path - the file path to the PDF to analyse.
    language - The language in the pdf to extract from.
               Use, for example, one of
               'eng' - English
               'nor' - Norwegian
               'deu' - German

               For more languages, check out
               https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html

    '''
    import pytesseract
    import pdf2image

    log = _get_logger(get_text_from_pdf)
    log.info('Converting the file "%s" to text.', pdf_path)

    # Convert pdf to a sequence of jpeg images
    pdfImgs=pdf2image.convert_from_path(pdf_path)

    # Extract the text from each image
    extracted_text=[]
    for im in pdfImgs:
        text=pytesseract.image_to_string(im,lang=language)
        extracted_text.append(text)

    # Join into one long string
    result = ' '.join(extracted_text)
    log.debug('Extracted text:\n%s', result)

    return result
