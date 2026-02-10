
# Instructions

**Note**: Please read `general_instructions.md` for coding standards and project setup guidelines.

You are a helpful code assistant that is going to assist
in creating a PDF downloader.

The downloader module shall be implemented in Python, and shall
be called `src/superdownloader.py`

The workflow is as follows:

1. The PDF_Downloader receives a filename consisting a list of URLs pointing to PDFs
2. The PDF_Downloader downloads the PDFs to the directory `./pdfs`
3. The PDF file names shall be the same as the short name of the PDF as in the URL.

### Important Notice

An example URL is https://www.justice.gov/epstein/files/DataSet%205/EFTA00008418.pdf

The PDF is not directly accessible for download through the URL, but requires a browsing user to click an
"I am above 18" confirmation before downloading. The downloader must take care of this,
rigging the necessary code and infrastructure to get this done.

I advice by starting easy, trying to run the downloader, and then add complexity in the solution as you
see needed. For example, try to just curl the above URL (which should result in an image), and inspect
the result, which is probably a redirect or something.

If you need python libraries or otherwise, you can add the dependencies to `requirements.txt`
and run `pip --install -r requirements.txt`. You already run in a venv, so this should be OK.
