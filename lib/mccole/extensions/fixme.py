"""Handle FIXME markers."""

import ivy
import shortcodes


@shortcodes.register("fixme")
def glossary_ref(pargs, kwargs, node):
    """Handle [% fixme ...args... %]."""
    return f'<span class="FIXME">FIXME</span>'
