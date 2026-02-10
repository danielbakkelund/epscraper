
# Instructions

You are a helpful code assistant that helps in
creating an OCR program for extracting text from
PDFs.

The resulting program shall be in python, and placed
in the module `src/superocr.py`.

The module should be executable both from the command line (for testing),
and as an imported python module.

Workflow:

1. The program reads PDF files from the directory `pdfs`.
2. The program uses the module `src/ocr.py` to perform the actual OCR.
3. The resulting texts are placed in a the folder `texts`, with filenames
   as for the PDFs, just extensions changed to `.txt`.

Tesseract is already installed, and the files can be expected to contain
english text.

The program first checks to see if the file is already converted, so that it does
not convert the same file twice.

Some of the files are images, so not everything ends up as text. If there is no
meaningful text output, the conversion should result in a text file with the text
"empty file".

The generated source should have a reference to this instruction at the start of
the file, for future reference.
