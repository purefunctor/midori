"""Configuration for Sphinx."""
from datetime import datetime


project = "midori"
author = "PureFunctor"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "insegel"
