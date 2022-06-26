from bs4 import BeautifulSoup

text = """<p id="nematode">C. elegans</p>
<p id="zebrafish">D. rerio</p>
<p id="fruitfly">D. melanogaster</p>
"""

doc = BeautifulSoup(text, "html.parser")
print(doc.find(id="zebrafish").string)
