from pathlib import Path
import yaml

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore
from typing import Any
from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from sphinx.application import Sphinx

try:
    __version__ = version("sphinx_pieces")
except PackageNotFoundError:
    __version__ = "unknown"


class PiecesDirective(SphinxDirective):
    """
    A directive that applies a unit identifier to the following header.

    Usage:
        .. unit:parameter
        Header Text
        -----------
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        # Get the unit parameter from the directive name
        domain, _, subdomain = self.name.partition(":")

        # Create a new section node
        section = nodes.section()
        section["ids"].append(
            nodes.make_id(f"{domain}-{subdomain}-{self.arguments[0]}")
        )

        # Create a title node
        title_text = f"{self.arguments[0]} {subdomain}"
        title = nodes.title(text=title_text)

        # Add the title to the section
        section += title

        # Parse the content of the directive
        self.state.nested_parse(self.content, self.content_offset, section)

        return [section]


def load_config(app: Sphinx) -> dict[str, list[str]]:
    """Load configuration from sphinx_pieces.yaml."""
    config_path = Path(app.confdir) / "sphinx_pieces.yaml"
    if not config_path.exists():
        return {}
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("domains", {})


def setup(app: Sphinx) -> dict[str, Any]:
    domains = load_config(app)

    for domain, subdomains in domains.items():
        for subdomain in subdomains:
            name = f"{domain}:{subdomain}"
            app.add_directive(name, PiecesDirective)

    return {"version": __version__, "parallel_read_safe": True}
