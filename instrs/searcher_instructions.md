
# Instructions

You are a helpful coding assistant helping in implementing a
scraping module for downlading PDFs from a designated site.

The site is accessed through `https://www.justice.gov/epstein/search`,
and at the bottom of the page, there is a search field in which one
can search for PDFs. For your convenience, the source of the above URL can
also be found in the file `html/search_page.html`.
Notice that if you try to curl the address (try that), then you may be met
by a button requiring you to state that you are not a robot, and also one
where you have to state that you are above 18 years old.

(A similar scraper is implemented in `src/superscraper.py` and `src/superdownloader.py`.
Have a look there to understand the necessary workarounds, or at least to get some
inspiration).

The module shall be implemented in python and located in `src/supersearcher.py`.
The module should be usable both from the command line (for testing) and as a proper
python module, as part of a larger program.

## Workflow

1. The module receives a search string.
2. The module simulates a user, entering the search string in the search and "clicking" search.
3. At this point, a list of search matches are presented at the bottom of the page.
   (I presume this is done through some javascript, since I can't see any trace of the
    search matches in the HTML when I choose "view source" in the browser).
4. Go through the list of search matches and extract the PDF links (similar to the job
   done by the `src/superscraper.py`).
5. Append the URLs to a file named `data/<search string>_urls.txt`, substituting blanks
   with underscores in the filename.
6. There is a "next" button for showing more PDF links -- click that link,
   scrape the new PDF links, append to the file, and repeat.

Before you start coding: read the general instructions found in `instrs/general_instructions.md`.
