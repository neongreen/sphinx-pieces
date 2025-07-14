from pathlib import Path
import yaml
from collections import defaultdict
from typing import Any
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.domains import Domain, ObjType, Index, IndexEntry
from sphinx.roles import XRefRole
from sphinx.locale import _
from sphinx.application import Sphinx

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version("sphinx_pieces")
except PackageNotFoundError:
    __version__ = "unknown"


# Index for unit:parameter objects
class UnitParameterIndex(Index):
    name = "unit-param-index"
    localname = "Unit Parameter Index"
    shortname = "unit param"

    def generate(self, docnames=None):
        content = defaultdict(list)
        for fullname, disp, typ, doc, anchor, _prio in self.domain.get_objects():
            if typ != "parameter" or (docnames and doc not in docnames):
                continue
            letter = disp[0].upper()
            content[letter].append(IndexEntry(disp, 0, doc, anchor, "", "", ""))
        return sorted(content.items()), False


# The directive for unit:parameter
class UnitParameterDirective(SphinxDirective):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        env = self.env
        domain = env.get_domain("unit")
        targetid = f"unit-parameter-{self.arguments[0]}"
        targetnode = nodes.target("", "", ids=[targetid])

        # Register object for index in domain data
        domain.data["parameters"].append(
            {
                "docname": env.docname,
                "name": self.arguments[0],
                "targetid": targetid,
            }
        )

        title = nodes.strong(text=self.arguments[0])
        para = nodes.paragraph()
        para += title
        if self.content:
            self.state.nested_parse(self.content, self.content_offset, para)

        return [targetnode, para]


def load_config(app: Sphinx) -> dict[str, list[str]]:
    """Load configuration from sphinx_pieces.yaml."""
    config_path = Path(app.confdir) / "sphinx_pieces.yaml"
    if not config_path.exists():
        return {}
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("domains", {})


# The domain for unit
class UnitDomain(Domain):
    indices = [UnitParameterIndex]
    name = "unit"
    label = "Unit"
    object_types = {
        "parameter": ObjType(_("parameter"), "parameter"),
    }
    directives = {
        "parameter": UnitParameterDirective,
    }
    roles = {
        "parameter": XRefRole(),
    }
    initial_data = {
        "parameters": [],
    }

    def clear_doc(self, docname):
        self.data["parameters"] = [
            obj for obj in self.data["parameters"] if obj["docname"] != docname
        ]

    def merge_domaindata(self, docnames, otherdata):
        for obj in otherdata["parameters"]:
            if obj["docname"] in docnames:
                self.data["parameters"].append(obj)

    def process_doc(self, env, docname, document):
        # No-op: all registration is done in the directive itself
        pass

    def get_objects(self):
        for obj in self.data["parameters"]:
            yield (
                obj["name"],
                obj["name"],
                "parameter",
                obj["docname"],
                obj["targetid"],
                1,
            )


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_domain(UnitDomain)
    return {"version": __version__, "parallel_read_safe": True}
