from bs4 import BeautifulSoup

text = """<p><strong>RNA</strong> (n.):
<a href="https://en.wikipedia.org/wiki/RNA">ribonucleic acid</a>."""

doc = BeautifulSoup(text, "html.parser")
print(f"type(doc) {type(doc)}")
print("--------")
print(doc.contents[0])
print("--------")
for (i, child) in enumerate(doc.contents[0].contents):
    print(f"{i}:[{child}]")
