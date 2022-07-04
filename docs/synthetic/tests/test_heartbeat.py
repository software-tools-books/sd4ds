"""Check that the project has a heartbeat."""

import dnadoh


def test_module_can_be_imported():
    assert hasattr(dnadoh, "__author__")
    assert hasattr(dnadoh, "__version__")
