"""Create links table."""

from pathlib import Path

import ivy
import markdown
import shortcodes
import util
import yaml
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


@ivy.events.register(ivy.events.Event.INIT)
def links_append():
    """Add Markdown links table to Markdown files."""
    if "links" not in ivy.site.config:
        return

    links = _read_links()
    links = "\n".join([f"[{x['key']}]: {x['url']}" for x in links])

    def visitor(node):
        if node.ext == "md":
            node.text += "\n\n" + links

    ivy.nodes.root().walk(visitor)


@shortcodes.register("links")
def links_table(pargs, kwargs, node):
    """Create a table of links."""
    if "links" not in ivy.site.config:
        return "<p>NO LINKS</p>"

    links = _read_links()
    links = "\n".join(
        f'<tr><td>{x["title"]}</td><td><a href="{x["url"]}">'
        f'{x["url"]}</a></td></tr>'
        for x in links
    )
    title = "<thead><tr><th>Link</th><th>URL</th></tr></thead>"
    return f'<table class="links-table">\n{title}\n<tbody>\n{links}\n</tbody>\n</table>'


@ivy.events.register(ivy.events.Event.EXIT)
def check():
    """Check link usage."""
    used = set()
    ext = LinkCollectorExtension(used)
    ivy.nodes.root().walk(
        lambda node: markdown.markdown(
            node.text, extensions=[ext, "markdown.extensions.extra"]
        )
    )

    defined = {d["url"] for d in _read_links()}

    util.warn("unknown links", used - defined)
    util.warn("unused links", defined - used)


class LinkCollectorExtension(Extension):
    def __init__(self, used, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.used = used

    def extendMarkdown(self, md):
        md.treeprocessors.register(LinkCollector(md, self.used), "linkcollector", 15)


class LinkCollector(Treeprocessor):
    def __init__(self, md, used):
        super().__init__(md)
        self.used = used

    def run(self, root):
        for element in root.iter("a"):
            self.used.add(element.attrib["href"])
        return root


def _read_links():
    """Read links file."""
    filepath = Path(ivy.site.home(), ivy.site.config["links"])
    with open(filepath, "r") as reader:
        return yaml.safe_load(reader)
