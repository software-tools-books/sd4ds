from bs4 import BeautifulSoup

text = """<p>Genes:</p>
<ul>
<li class="gene">Indy</li>
<li class="gene">Tinman</li>
<li class="category">Halloween genes:
  <ul>
  <li class="gene">Mummy</li>
  <li class="gene">Phantom</li>
  </ul>
</li>
</ul>
"""

doc = BeautifulSoup(text, "html.parser")
for node in doc.find_all("li"):
    print(node)
print("----")
for node in doc.find_all("li", attrs={"class": "gene"}):
    print(node.string)
