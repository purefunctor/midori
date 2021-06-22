"""Configuration for Sphinx."""
from datetime import datetime


project = "midori"
author = "PureFunctor"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
html_theme = "insegel"
