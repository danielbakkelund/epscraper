
# Instructions

You are a helpful code assistant, that is creating a program
for downlading PDF documents.

The process is as follows:

1. You generate a list of URLs on the following form:
   `https://www.justice.gov/epstein/doj-disclosures/data-set-5-files`.
   In particular, the number in the data set is a running number.
   The start end end numbers for the URLs are given you on the command line.
2. Pass the URLs to the module located at `src/superscraper.py`.
   This module will prodvide you with a list of URLs pointing to PDFs.
3. Pass the PDF URLs to the module `src/superdownloader.py`.
   This module will download the PDFs.
   See `README_DOWNLOADER.md` for details on this module.

It is important to gather all the PDF URLs first, since, as soon as the download
starts, the user has to click a "I am not a robot" button once. If you do this in
several passes, the user must click several times, which is unfortunate.

The resulting module should be called `src/supermain.py`
