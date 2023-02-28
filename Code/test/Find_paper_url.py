import pdf2doi
import doi

pdf2doi.config.set('verbose', False)


# the function can analyse all PDFs under the path
def extract_real_url(pdf_file_path):
    results = pdf2doi.pdf2doi(pdf_file_path)
    for result in results:
        # the routine below is to print the doi of each pdf
        # print(result['identifier'], result['path'])
        url = doi.get_real_url_from_doi(result["identifier"])
        print(url)


# remember to change the path
extract_real_url('/Users/anton/Documents/HPCDS/PSD/Patrick__Barrera_and_Collins/papers/Papers')
