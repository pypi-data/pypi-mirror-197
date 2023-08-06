from bs4 import BeautifulSoup
import requests

class __bibtex__:
    def __init__(self):
        self.url = ""
        self.HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"}

    def check(self, url):
        self.url = url
        result = ""
        if "doi.org" in url:
            result = "DOI"
        if "scholar.google" in url:
            result = "Scholar"
        else:
            result = "DOI"
        return result

    def bibtex_doi(self):
        try:
            if "doi.org" not in self.url:
                url = 'http://dx.doi.org/' + self.url
            else:
                url = self.url
            headers = {"accept": "application/x-bibtex"}
            r = requests.get(url, headers = headers)
            if r.status_code == 200:
                return r.text
            else:
                raise LookupError
        except LookupError:
            print("Cannot read this link DOI")

    def bibtex_scholar(self):
        url = self.url
        content = requests.get(url, headers=self.HEADERS).content
        html = BeautifulSoup(content, "html.parser")
        block = html.find("div", {"class": "gs_ri"})
        title = block.find("h3")
        link = title.find("a")
        id = link["id"]
        cite_url = "https://scholar.google.de/scholar?hl=de&q=info:" + id + ":scholar.google.com/&output=cite&scirp=0"
        findLatex = requests.get(cite_url)
        citation_view = BeautifulSoup(findLatex.content, "html.parser")
        latex_link = citation_view.find("div", {"id": "gs_citi"})
        latex_mf = latex_link.findChildren("a")[0]["href"]
        result = BeautifulSoup(requests.request("GET", url=latex_mf).content, "html.parser")
        return result.text