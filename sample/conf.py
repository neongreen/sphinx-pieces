# Configuration file for the Sphinx documentation builder.
import os
import sys


sys.path.insert(0, os.path.abspath(".."))

project = "Sample Sphinx Pieces Project"
extensions = ["sphinx_pieces"]
master_doc = "index"

# -- Options for HTML output --
html_theme = "alabaster"
