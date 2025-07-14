try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore
from typing import Any
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.transforms import SphinxTransform
from sphinx.util.docutils import SphinxDirective

from sphinx.application import Sphinx

try:
    __version__ = version("sphinx_pieces")
except PackageNotFoundError:
    __version__ = "unknown"


class UnitDirective(SphinxDirective):
    """
    A directive that applies a unit identifier to the following header.

    Usage:
        .. unit:parameter
        Header Text
        -----------
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        # Get the unit parameter from the directive name
        unit_param = self.name.split(":", 1)[1] if ":" in self.name else ""

        # Create a pending node that will be processed by the transform
        pending = nodes.pending(
            UnitTransform, {"unit_param": unit_param, "lineno": self.lineno}
        )
        pending.source = self.state.document.current_source
        pending.line = self.lineno

        return [pending]


class UnitTransform(SphinxTransform):
    """
    Transform that modifies headers following unit directives.
    """

    default_priority = 210  # Run after most other transforms

    def apply(self):
        for pending in self.document.findall(nodes.pending):
            if pending.transform is UnitTransform:
                self.handle_pending(pending)

    def handle_pending(self, pending):
        unit_param = pending.details["unit_param"]

        # Find the next section/header after this pending node
        parent = pending.parent
        pending_index = parent.index(pending)

        # Look for the next section node
        for i in range(pending_index + 1, len(parent)):
            node = parent[i]
            if isinstance(node, nodes.section):
                # Found a section, modify its title
                title = node[0]  # First child should be the title
                if isinstance(title, nodes.title):
                    # Append the unit parameter to the title text
                    if title.children and isinstance(title.children[0], nodes.Text):
                        original_text = title.children[0].astext()
                        title.children[0] = nodes.Text(f"{original_text} {unit_param}")
                break

        # Remove the pending node
        pending.parent.remove(pending)


def setup(app: Sphinx) -> dict[str, Any]:
    # Register the transform
    app.add_transform(UnitTransform)

    # Custom directive class that accepts arguments
    class UnitParameterDirective(SphinxDirective):
        """Unit directive that takes the parameter as an argument."""

        has_content = False
        required_arguments = 1
        optional_arguments = 0
        final_argument_whitespace = True

        def run(self):
            unit_param = self.arguments[0] if self.arguments else ""

            # Create a pending node that will be processed by the transform
            pending = nodes.pending(
                UnitTransform, {"unit_param": unit_param, "lineno": self.lineno}
            )
            pending.source = self.state.document.current_source
            pending.line = self.lineno

            return [pending]

    # Register the unit directive
    app.add_directive("unit", UnitParameterDirective)

    return {"version": __version__, "parallel_read_safe": True}
