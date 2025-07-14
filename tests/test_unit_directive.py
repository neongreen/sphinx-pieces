"""
Test for the unit directive functionality.
"""

from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="unit-directive")
def test_pieces_directive_basic(app: SphinxTestApp, status, warning):
    """Test basic pieces directive functionality."""
    app.build()

    # Check that the build succeeded
    assert app.statuscode == 0

    # Read the generated HTML
    content = (app.outdir / "index.html").read_text(encoding="utf-8")

    # The header "Bar" should be modified to "Bar fafafa"
    assert "<h2>Bar fafafa" in content

    # The original header text should not appear alone
    assert "<h2>Bar</h2>" not in content or "<h2>Bar fafafa</h2>" in content


@pytest.mark.sphinx("html", testroot="unit-directive")
def test_pieces_directive_multiple_levels(app: SphinxTestApp, status, warning):
    """Test pieces directive with different header levels."""
    app.build()

    content = (app.outdir / "index.html").read_text(encoding="utf-8")

    # Test h1 level
    assert "<h2>Main Title test123" in content

    # Test h2 level
    assert "<h2>Subtitle xyz789" in content


@pytest.mark.sphinx("html", testroot="unit-directive")
def test_pieces_directive_no_following_header(app: SphinxTestApp, status, warning):
    """Test pieces directive behavior when no header follows."""
    app.build()

    # Should not crash and build successfully
    assert app.statuscode == 0


# Test data - create a temporary test directory structure
@pytest.fixture(scope="session")
def rootdir():
    return Path(__file__).parent.absolute() / "roots"


@pytest.fixture(autouse=True)
def setup_test_root(rootdir, monkeypatch):
    """Set up test root directory with test files."""
    test_root = rootdir / "test-unit-directive"
    test_root.mkdir(parents=True, exist_ok=True)

    # Create conf.py
    conf_py = test_root / "conf.py"
    conf_py.write_text(
        """
extensions = ['sphinx_pieces']
master_doc = 'index'
exclude_patterns = ['_build']
html_theme = 'basic'
""",
        encoding="utf-8",
    )

    # Create index.rst
    index_rst = test_root / "index.rst"
    index_rst.write_text(
        """
Test Document
=============

This is a test document for the unit directive.

.. pieces:test123:: Main Title

Some content under the main title.

.. pieces:fafafa:: Bar

Some content here under Bar.

.. pieces:xyz789:: Subtitle

Content under subtitle.

Regular Header
--------------

This header should not be affected.

.. pieces:orphan::

This unit directive has no following header.

The end.
""",
        encoding="utf-8",
    )


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

.. pieces:fafafa:: Bar

   content
""")
        # Create sphinx_pieces.yaml
        (srcdir / "sphinx_pieces.yaml").write_text("""
domains:
    pieces:
        - fafafa
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
                # Should contain the modified header
                assert "<h2>Bar fafafa" in content
                # Should contain the content
                assert "content" in content

        finally:
            app.cleanup()
