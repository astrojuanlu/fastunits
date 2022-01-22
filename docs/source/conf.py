from importlib.metadata import metadata

# -- Project information

_metadata = metadata("fastunits")

project = _metadata["Name"]
author = _metadata["Author-email"].split("<", 1)[0].strip()
copyright = f"2022, {author}"

version = _metadata["Version"]
release = ".".join(version.split(".")[:2])


# -- General configuration

extensions = [
    "myst_parser",
]

templates_path = ["_templates"]


# -- Options for HTML output

html_theme = "furo"
html_static_path = ["_static"]
