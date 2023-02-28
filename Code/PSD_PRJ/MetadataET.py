import pdf2doi
from habanero import Crossref
import requests
import re

class MyDict(dict):
    def __init__(self, *args, **kwargs):
        super(MyDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        """
        Override __getitem__ to return None instead of raising a KeyError
        when a non-existent key is accessed.
        """
        return super(MyDict, self).get(key, None)

def pdf2doi_wraper(pdf_file_path):
    return pdf2doi.pdf2doi(pdf_file_path)["identifier"]

def doi2meta(doi):
    cr = Crossref()
    try:
        results = cr.works(ids=doi)
        metadata = results['message']
        return metadata
    except:
        return None

def title2doi(title):
    cr = Crossref()
    results = cr.works(query=title)
    dois = [item['DOI'] for item in results['message']['items']]
    return dois

def name2ORCID(*query):
    # parameter can be:
    # first name, second name, location
    # first name, second name
    if len(query)==3:
        url = "https://pub.orcid.org/v3.0/search/?q=given-names:%s+AND+family-name:%s+AND+affiliation-org-name:%s&rows=10"%query
    elif len(query)==2:
        url = "https://pub.orcid.org/v3.0/search/?q=given-names:%s+AND+family-name:%s&rows=10"%query
    else:
        raise Exception("number of parameters ERROR")
    # Set the headers to accept JSON responses
    headers = {"Accept": "application/json"}
    # Send the GET request to the API endpoint
    response = requests.get(url, headers=headers)
    # Parse the JSON response and extract the ORCID identifiers
    results = response.json()
    if results["result"]!=None:
        orcid = [i["orcid-identifier"]["path"] for i in results["result"]]
        return orcid
    else:
        return None


def extract_information(pdf_file_path):
    doi = pdf2doi_wraper(pdf_file_path)
    if doi==None:
        raise Exception("Can't fint doi from this pdf file")
    else:
        metadata = doi2meta(doi)
        if metadata==None:
            raise Exception("can't fetch metaddata, %s"%doi)
    url = metadata["resource"]["primary"]["URL"]
    title = preprocess(metadata["title"][0])
    date = metadata["created"]["timestamp"]
    authors = [{"name": {"given": i["given"], "family":i["family"]}, "sequence": i["sequence"], \
                "location": [j["name"] for j in i["affiliation"]], "ORCID":MyDict(i)["ORCID"], \
                "ORCID_trust": True} for i in metadata["author"]]
    for i in authors:
        if i["ORCID"]!=None:
            i["ORCID"] = i["ORCID"].lstrip("http://orcid.org/")
        if i["ORCID"]==None:#try to fill orcid by name and location(more exact)
            if len(i["location"])!=0:
                for location in i["location"]:
                    orcid = name2ORCID(i["name"]["given"], i["name"]["family"], location)
                    if orcid!=None:
                        i["ORCID"] = orcid
                        i["ORCID_trust"] = False
                        break;
        if i["ORCID"]==None:#try to fill orcid only by name(may return multiple orcids)
            orcid = name2ORCID(i["name"]["given"], i["name"]["family"])
            if orcid!=None:
                i["ORCID"] = orcid
                i["ORCID_trust"] = False
    if "reference" in metadata:
        row_references = metadata["reference"]
        references = []
        for i in row_references:
            ref_data = {}
            if "article-title" in i:
                ref_data["title"] = i["article-title"]
                ref_data["type"] = "paper"
                ref_data["key"] = doi+"%&%"+i["key"]
            elif "DOI" in i:
                ref_meta = doi2meta(i["DOI"])
                if ref_meta!=None:
                    if len(ref_meta["title"])==0:
                        ref_data["title"] = preprocess(ref_meta["resource"]["primary"]["URL"])
                        ref_data["type"] = "website"
                    else:
                        ref_data["title"] = preprocess(ref_meta["title"][0])
                        ref_data["type"] = "paper"
                else:
                    ref_data["title"] = preprocess(i["DOI"])
                    ref_data["type"] = "paper"
                ref_data["key"] = doi+"%&%"+i["key"]
            elif "volume-title" in i:
                ref_data["title"] = preprocess(i["volume-title"])
                ref_data["type"] = "book"
                ref_data["key"] = doi+"%&%"+i["key"]
            elif "series-title" in i:
                ref_data["title"] = preprocess(i["series-title"])
                ref_data["type"] = "book"
                ref_data["key"] = doi+"%&%"+i["key"]
            elif "unstructured" in i:
                ref_data["title"] = preprocess(i["unstructured"])
                ref_data["type"] = "website"
                ref_data["key"] = doi+"%&%"+i["key"]
            else:
                ref_data["title"] = None
                ref_data["type"] = "website"
                ref_data["key"] = doi+"%&%"+i["key"]
                ref_data["raw"] = i
            references.append(ref_data)
    else:
        references = []

    res = {"title": title, "date":date, "doi": doi, "url": url, "authors": authors, "references": references}
    return res

def preprocess(str):
    str = re.sub('"', "\\\"", str)
    str = re.sub("'", "\\\'", str)
    return str

if __name__=="__main__":
    extract_information("../Paper/Papers/3547334.pdf")