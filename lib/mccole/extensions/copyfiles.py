"""Copy files verbatim from source directory to destination."""

from glob import iglob
from pathlib import Path
from shutil import copyfile

import ivy


@ivy.events.register(ivy.events.Event.INIT)
def copy_files():
    """Copy files."""
    if (patterns := ivy.site.config.get("copy", None)) is None:
        return
    for pat in patterns:
        src_dir = ivy.site.src()
        out_dir = ivy.site.out()
        pat = Path(src_dir, "**", pat)
        for src_file in iglob(str(pat), recursive=True):
            out_file = src_file.replace(src_dir, out_dir)
            Path(out_file).parent.mkdir(exist_ok=True, parents=True)
            copyfile(src_file, out_file)
