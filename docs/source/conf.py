# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from importlib.metadata import version as importlib_version
from pathlib import Path

sys.path.insert(0, str(Path.cwd().parents[1]))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'nbsphinx',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
    'sphinx_prompt',
    'sphinx_math_dollar',
    'sphinx_mdinclude',
    'sphinx_design',
    'myst_nb',
    'sphinx.ext.napoleon',
    'IPython.sphinxext.ipython_console_highlighting']


# docstrings
autodoc_typehints = "none"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# always execute notebooks
env_skip_execute = os.getenv("SKIP_EXECUTE")


if not env_skip_execute:
    nb_execution_mode = "force"
else:
    nb_execution_mode = "off"

nbsphinx_allow_errors = True
nbsphinx_timeout = 1000

# myst-nb control of notebooks
nb_execution_timeout = 500
nb_execution_allow_errors = True
myst_enable_extensions = ["dollarmath"]


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The main toctree document.
main_doc = 'index'

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CASSI-2026'
copyright = '2026, Sunny Wong'
author = 'Sunny Wong'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Enable linking references to other projects' documentation.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
    "networkx": ('https://networkx.org/documentation/stable', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'sympy': ('https://docs.sympy.org/latest/', None),
    'yt': ('https://yt-project.org/doc', None),
    'unyt': ('https://unyt.readthedocs.io/en/stable', None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
}

# Don't include the extra CSS from sphinx-prompt when using the copy button
copybutton_exclude = 'style'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "repository_url": "https://github.com/sunnywong314/CASSI2026-Sunny",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "use_source_button": True,
    "repository_branch": "main",
    "launch_buttons": {
        "colab_url": "https://colab.research.google.com",
    },
    "path_to_docs": "docs/source",
    "logo": {
        "text": f"CASSI 2026",
    }
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
