
# Instructions

**Note**: Please read `general_instructions.md` for coding standards and project setup guidelines.

You are a helpful code assistant that is going to assist
in creating a web scraper.

The scraper module shall be implemented in Python, and shall
be called `src/superscraper.py`

The workflow is as follows:

1. The scraper receives a URL to inspect
2. The scraper reads the URL and extracts a number of links that point to PDF files.
   The format of the PDF files is given below.
3. The scraper passes the list of URLs to a PDF_Downlader

## Additional information

An example of a typical HTML file that will be encountered can be found
in `html/example.html`.

The PDF URLs to download are typically looking like the link in the anchor tag below:

<li><div class="views-field views-field-title"><span class="field-content"><a href="/epstein/files/DataSet%202/EFTA00003159.pdf">EFTA00003159.pdf</a></span></div></li>

Sometimes the entire URL is provided, such as here:
<li><div class="views-field views-field-title"><span class="field-content"><a href="https://www.justice.gov/epstein/files/DataSet%205/EFTA00008410.pdf">EFTA00008410.pdf</a></span></div></li>

If only the partial URL is provided, it is important that the full URL is offered in the returned list.

In the first edition, store the URLs to a file `data/urls.txt`, one URL per line.

# General notes

Use ' for strings, and """ for docstrings, as a main rule.

# TESTING

Test the code as you go, making sure you are able to download the URLs.

Testsing can be done as follows:

Try to scrape the page at `https://www.justice.gov/epstein/doj-disclosures/data-set-5-files`
The URLs should be the same as can be found in `html/example2.html`
