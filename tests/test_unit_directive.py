"""
Test for the unit directive functionality.
"""

from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp




def test_pieces_directive_integration():
    """Integration test that creates a real Sphinx app and tests the directive."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create source directory
        srcdir = tmpdir / "source"
        srcdir.mkdir()

        # Create conf.py
        (srcdir / "conf.py").write_text("""
extensions = ['sphinx_pieces']
master_doc = 'index'
""")

        # Create index.rst
        (srcdir / "index.rst").write_text("""
Test
====

.. unit:parameter:: MyParam

   Some content.

.. other:thing:: MyThing

   Some other content.
""")
        # Create sphinx_pieces.yaml
        (srcdir / "sphinx_pieces.yaml").write_text("""
domains:
    unit:
        - parameter
    other:
        - thing
""")

        # Create output directory
        outdir = tmpdir / "build"

        # Build with Sphinx
        app = SphinxTestApp(
            srcdir=srcdir,
            builddir=outdir,
            confdir=srcdir,
            status=None,
            warning=None,
        )

        try:
            app.build()

            # Check the result
            html_file = outdir / "html" / "index.html"
            if html_file.exists():
                content = html_file.read_text()
                assert "MyParam parameter" in content
                assert "MyThing thing" in content

        finally:
            app.cleanup()
