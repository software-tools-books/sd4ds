#!/usr/bin/env python

"""Create single-page HTML version of book."""

import argparse
import sys
import os
from bs4 import BeautifulSoup


def main():
    options = parse_args()

    with open(os.path.join(options.root, "index.html"), "r") as reader:
        soup = BeautifulSoup(reader.read(), "html.parser")
    body = soup.find("body")

    content = open(options.head, "r").read()
    content += part(options.root, body, "ol.toc-chapter", "Chapter")
    content += part(options.root, body, "ol.toc-appendix", "Appendix")
    content += open(options.foot, "r").read()

    print(content)


def part(root, body, key, kind):
    toc = body.select_one(key)
    content = []
    for ref in toc.find_all("a"):
        slug = ref.attrs["href"].rstrip("/")
        path = os.path.join(root, slug, "index.html")
        content.append(get(path, slug, kind))
    return "\n".join(content)


def get(path, slug, kind):
    with open(path, "r") as reader:
        soup = BeautifulSoup(reader.read(), "html.parser")

    main = soup.find("main")
    main.name = "section"
    main["class"] = "new-chapter"
    patch_chapter_refs(main)
    patch_glossary(main)
    patch_images(main, slug)
    patch_bib_refs(main)

    title = soup.find("h1")
    title["id"] = slug
    title.string = f"{kind}: {title.text}"
    main.insert(0, title)

    return str(main)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", required=True, help="HTML head")
    parser.add_argument("--foot", required=True, help="HTML foot")
    parser.add_argument("--root", required=True, help="root directory")
    return parser.parse_args()


def patch_bib_refs(main):
    b = "../bibliography/"
    for node in main.select("a.bibref"):
        if node.attrs["href"].startswith(b):
            node.attrs["href"] = node.attrs["href"].replace(b, "")


def patch_chapter_refs(main):
    for node in main.select("a"):
        if ("href" in node.attrs) and (node.attrs["href"].startswith("../") and (node.attrs["href"].endswith("/"))):
            node.attrs["href"] = node.attrs["href"].replace("../", "#", 1)[:-1]


def patch_glossary(content):
    g = "../glossary/"
    for node in content.select("a.glossref"):
        if node.attrs["href"].startswith(g):
            node.attrs["href"] = node.attrs["href"].replace(g, "")
    for node in content.select("span.glosskey"):
        if "break-before" in node.attrs["class"]:
            node.attrs["class"] = [c for c in node.attrs["class"] if c != "break-before"]
            if "class" in node.parent.attrs:
                node.parent.attrs["class"].append("break-before")
            else:
                node.parent.attrs["class"] = ["break-before"]


def patch_images(content, slug):
    for node in content.find_all("img"):
        if node.attrs["src"].startswith("./"):
            relative = node.attrs["src"][2:]
            node.attrs["src"] = f"./{slug}/{relative}"


if __name__ == "__main__":
    main()
