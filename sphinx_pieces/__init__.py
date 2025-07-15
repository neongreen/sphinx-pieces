from pathlib import Path
import yaml
from collections import defaultdict
from typing import Any
from docutils import nodes
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective
from sphinx.domains import Domain, ObjType, Index, IndexEntry
from sphinx.roles import XRefRole
from sphinx.locale import _
from sphinx.application import Sphinx
from sphinx.transforms import SphinxTransform

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version("sphinx_pieces")
except PackageNotFoundError:
    __version__ = "unknown"


def create_domain(domain_name: str, species_list: list[str]) -> type[Domain]:
    """Create a new Domain subclass."""

    class PieceDirective(SphinxDirective):
        has_content = True
        required_arguments = 1
        optional_arguments = 0
        final_argument_whitespace = True

        def run(self):
            env = self.env
            domain = env.get_domain(domain_name)
            piece_type = self.name.split(":")[1]
            piece_name = self.arguments[0]
            targetid = f"{domain_name}-{piece_type}-{piece_name}"
            targetnode = nodes.target("", "", ids=[targetid])

            # Register object for index in domain data
            domain.data[f"{piece_type}s"].append(
                {
                    "docname": env.docname,
                    "name": piece_name,
                    "targetid": targetid,
                }
            )

            # Create a placeholder node
            placeholder = nodes.pending(
                PieceTransform,
                {"piece_type": piece_type, "piece_name": piece_name},
            )
            string_list = StringList([f"**{piece_name}**"])
            self.content.insert(0, string_list)
            self.state.nested_parse(self.content, self.content_offset, placeholder)

            return [targetnode, placeholder]

    class PieceIndex(Index):
        name = f"{domain_name}-gen-index"
        localname = f"{domain_name.capitalize()} Index"
        shortname = f"{domain_name.capitalize()} Index"

        def generate(self, docnames=None):
            content = defaultdict(list)
            for fullname, disp, typ, doc, anchor, _prio in self.domain.get_objects():
                if docnames and doc not in docnames:
                    continue
                letter = disp[0].upper()
                content[letter].append(IndexEntry(disp, 0, doc, anchor, "", "", ""))
            return sorted(content.items()), False

    class PieceDomain(Domain):
        name = domain_name
        label = domain_name.capitalize()
        object_types = {s: ObjType(_(s), s) for s in species_list}
        directives = {s: PieceDirective for s in species_list}
        roles = {s: XRefRole() for s in species_list}
        indices = [PieceIndex]
        initial_data = {f"{s}s": [] for s in species_list}

        def get_objects(self):
            for s in species_list:
                for obj in self.data[f"{s}s"]:
                    yield (
                        obj["name"],
                        obj["name"],
                        s,
                        obj["docname"],
                        obj["targetid"],
                        1,
                    )

    return PieceDomain


def load_config(app: Sphinx) -> dict[str, list[str]]:
    """Load configuration from sphinx_pieces.yaml."""
    config_path = Path(app.confdir) / "sphinx_pieces.yaml"
    if not config_path.exists():
        return {}
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("domains", {})


from sphinx.transforms import SphinxTransform


class PieceTransform(SphinxTransform):
    default_priority = 700

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.findall(nodes.pending):
            if node.details["piece_name"]:
                # This is our placeholder node.
                # The content of the directive is now in the placeholder node.
                # We can now modify the content of the node.
                # For example, let's add the piece_type to the title.
                new_paragraph = nodes.paragraph()
                for child in node.children:
                    if isinstance(child, nodes.paragraph) and child.children and isinstance(child.children[0], nodes.strong):
                        strong_node = child.children[0]
                        original_text = strong_node.astext()
                        strong_node.children = [nodes.Text(f"{original_text} {node.details['piece_type']}")]
                    new_paragraph.append(child.deepcopy())
                node.replace_self(new_paragraph)


def setup(app: Sphinx) -> dict[str, Any]:
    config = load_config(app)
    for domain_name, species in config.items():
        app.add_domain(create_domain(domain_name, species))
    app.add_transform(PieceTransform)

    return {"version": __version__, "parallel_read_safe": True}
