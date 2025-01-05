# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "isisaka.com"
copyright = "2024, Tadahiro Ishisaka"
author = "Tadahiro Ishisaka"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "ja"

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# html_theme_options = {
#     "source_repository": "https://github.com/ishisaka/isisaka_com/",
#     "source_branch": "main",
#     "source_directory": "source",
# }
html_static_path = ["_static"]
html_title = "isisaka.com"
html_logo = "_static/images/isisaka.com.png"
html_favicon = "_static/images/favicon.ico"

# -- Options for myst-parser -------------------------------------------------
myst_fence_as_directive = ["mermaid"]
