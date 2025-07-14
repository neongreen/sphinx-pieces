"""
Test for the unit directive functionality.
"""

import pytest
from sphinx.testing.util import SphinxTestApp
from pathlib import Path


@pytest.mark.sphinx("html", testroot="unit-directive")
def test_unit_directive_basic(app, status, warning):
    """Test basic unit directive functionality."""
    app.build()

    # Check that the build succeeded
    assert app.statuscode == 0

    # Read the generated HTML
    content = (app.outdir / "index.html").read_text(encoding="utf-8")

    # The header "Bar" should be modified to "Bar fafafa"
    assert "Bar fafafa" in content

    # The original header text should not appear alone
    assert "Bar</h2>" not in content or "Bar fafafa</h2>" in content


@pytest.mark.sphinx("html", testroot="unit-directive")
def test_unit_directive_multiple_levels(app, status, warning):
    """Test unit directive with different header levels."""
    app.build()

    content = (app.outdir / "index.html").read_text(encoding="utf-8")

    # Test h1 level
    assert "Main Title test123" in content

    # Test h2 level
    assert "Subtitle xyz789" in content


@pytest.mark.sphinx("html", testroot="unit-directive")
def test_unit_directive_no_following_header(app, status, warning):
    """Test unit directive behavior when no header follows."""
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

.. unit:: test123

Main Title
==========

Some content under the main title.

.. unit:: fafafa

Bar
---

Some content here under Bar.

.. unit:: xyz789

Subtitle
~~~~~~~~

Content under subtitle.

Regular Header
--------------

This header should not be affected.

.. unit:: orphan

This unit directive has no following header.

The end.
""",
        encoding="utf-8",
    )


def test_unit_directive_integration():
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

.. unit:: fafafa

Bar
---

content
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
                assert "Bar fafafa" in content or "fafafa" in content

        finally:
            app.cleanup()
