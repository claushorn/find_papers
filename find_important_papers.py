import requests, lxml
from bs4 import BeautifulSoup
import re

#import bs4 
#print(bs4.__version__)

# Define the search query
topN = 10
#area = "bioinformatics"
#area = "genetics"

#query = f"AUC in {area} 2005 to 2024"
query = "LLMs for interpreting model predictions"

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
params = {"q": query, "hl": "en"} 
if topN>10:
    params["num"] = str(topN)  # works on the website , but give captia test 

# Perform the search
url = "https://scholar.google.com/scholar"
html = requests.get(url, params=params, headers=headers).text

soup2 = BeautifulSoup(html, 'lxml')

papers = []
for result in soup2.select('.gs_ri'):
    title = result.select_one('.gs_rt').text
    link = result.select_one('.gs_rt a')['href']
    cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
    cited_by_count = 0
    try:
        cited_by_count = int(result.select_one('#gs_res_ccl_mid .gs_nph+ a').text.split(' ')[2])
    except IndexError:
        print("Warning: Could not parse citation count.")
        pass
    #print(f"{cited_by_count}\n{title}\n{link}\n")
    papers.append({'title': title, 'link': link, 'citations': cited_by_count})
    pass
print("# papers found: ",len(papers))

topN_papers = sorted(papers, key=lambda x: x['citations'], reverse=True)[:topN]
print(f"Top {topN} most cited papers:")
for paper in topN_papers:
    print("")
    print(paper['citations'])
    print(paper['title'])
    print(paper['link'])

