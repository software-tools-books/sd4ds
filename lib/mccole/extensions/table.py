"""Handle tables and table references."""

import shortcodes
import util


@shortcodes.register("t")
def table_ref(pargs, kwargs, node):
    """Handle [% t slug %] table reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), "Bad 't' shortcode")
    slug = pargs[0]
    return f'<a class="tbl-ref" href="FIXME">Table&nbsp;{slug}</a>'
