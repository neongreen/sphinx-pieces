# Sample Sphinx Project

This is a minimal Sphinx project demonstrating the usage of the `sphinx_pieces` extension from the parent directory.

## How to build

1. Install Sphinx if you haven't already:
   ```sh
   pip install sphinx
   ```
2. From this directory, run:
   ```sh
   sphinx-build -b html . _build/html
   ```
3. Open `_build/html/index.html` in your browser to view the documentation.

## Notes
- The extension is loaded from the parent directory (`..`).
- See `usage.rst` for an example of the custom directive.
