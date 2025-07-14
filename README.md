# sphinx_pieces

## Idea

> The idea is to let people mark any section of a Sphinx document—or any header—with a domain and subdomain.
> It should be easy to define your own domains and subdomains, because the goal is to support internal documentation across teams.
>
> For example, one team might have a system where content can be labeled as an explanation, a tutorial, a reference, etc.
> They should be able to define something like team-a:tutorial as a directive, and apply that to relevant sections of their documentation.
>
> This would work like domains with namespaces, but without needing to write code to define a new one.
> Ideally, there would be a YAML file—or several, like team-a.yaml, team-b.yaml, and so on—where each team can define their own typology or hierarchy of content types.
> They’d then use those types to mark up their docs.

## Dev notes

Don't use pip. This project uses uv.

### If using uv

Typecheck: `uv run mypy sphinx_pieces tests`.

Test: `uv run pytest`.

### If you have Mise

Typecheck: `mise mypy`.

Test: `mise test`.

