# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# The full version, including alpha/beta/rc tags
import os
import sys

import git
import hailin

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./_ext"))
sys.path.append(os.path.abspath("./src"))

project = "haiiliin.github.io"
copyright = "2022, WANG Hailin"
author = "WANG Hailin"

release = version = hailin.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "ablog",
    "bibliography",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinxcontrib.bibtex",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
]

# sphinxcontrib-bibtex configuration
bibtex_bibfiles = ["_static/bibs/references.bib"]

# bibliography configuration
bibliography_generate = False
bibliography_template = "_templates/paper.md"
bibliography_conf = "posts/papers.toml"
bibliography_outdir = "posts/papers"

# -- Ablog configuration ---------------------------------------------------
ablog_builder = "dirhtml"

# disqus configuration
disqus_shortname = "haiiliin-com"
disqus_pages = False

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl = "https://haiiliin.com/"

# A path relative to the configuration directory for posts archive pages.
blog_path = "posts"

# The "title" for the posts, used in active pages.  Default is ``'Blog'``.
blog_title = "WANG Hailin"

# The path that you store your content in, this will be used for the browsing path
# on your published website
# e.g. blog_post_pattern = "blog/*/*"
blog_post_pattern = "posts/*/*"

# -- Blog Post Related --------------------------------------------------------

# Format date for a post.
post_date_format = "%b %d, %Y"

# Number of paragraphs (default is ``1``) that will be displayed as an excerpt
# from the post. Setting this ``0`` will result in displaying no post excerpt
# in archive pages.  This option can be set on a per post basis using
post_auto_excerpt = 1

# Index of the image that will be displayed in the excerpt of the post.
# Default is ``0``, meaning no image.  Setting this to ``1`` will include
# the first image, when available, to the excerpt.  This option can be set
# on a per post basis using :rst:dir:`post` directive option ``image``.
post_auto_image = 0

# Number of seconds (default is ``5``) that a redirect page waits before
# refreshing the page to redirect to the post.
post_redirect_refresh = 1

# -- Blog Feed Options --------------------------------------------------------
# Turn feeds by setting :confval:`blog_baseurl` configuration variable.
# Choose to create feeds per author, location, tag, category, and year,
# default is ``False``.
blog_feed_archives = False

# Choose to display full text in posts feeds, default is ``False``.
blog_feed_fulltext = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = "WANG Hailin"
html_static_path = ["_static"]

# Get the sphinx theme from the branch name
default_theme = "sphinx_book_theme"
html_themes = {
    "main": default_theme,
    "sphinx-rtd-theme": "sphinx_rtd_theme",
    "sphinx-book-theme": "sphinx_book_theme",
    "pydata-sphinx-theme": "pydata_sphinx_theme",
}
try:
    current_branch = git.repo.Repo("../").active_branch.name
except Exception:
    current_branch = "main"
    if os.environ.get("READTHEDOCS_VERSION_TYPE", None) == "branch":
        current_branch = os.environ.get("READTHEDOCS_VERSION_NAME", "main")
        current_branch = "main" if current_branch == "latest" else current_branch

html_theme = os.environ.get("SPHINX_THEME", None) or html_themes.get(current_branch, default_theme)

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
if html_theme == "pydata_sphinx_theme":
    html_theme_options = {
        "github_url": "https://github.com/haiiliin/haiiliin.github.io",
        "twitter_url": "https://twitter.com/haiiliin",
        "header_links_before_dropdown": 3,
        "icon_links": [
            {
                # Label for this link
                "name": "email",
                # URL where the link will redirect
                "url": "mailto:hailin.wang@connect.polyu.hk",  # required
                # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
                "icon": "fa-solid fa-envelope",
                # The type of image to be used (see below for details)
                "type": "fontawesome",
            },
        ],
        "search_bar_text": "Search...",
        "show_prev_next": True,
        "navbar_end": ["search-field", "theme-switcher", "navbar-icon-links"],
        "navbar_persistent": [],
        "footer_start": ["copyright", "last-updated"],
        "footer_end": ["sphinx-version", "theme-version"],
    }
elif html_theme == "sphinx_book_theme":
    html_theme_options = {
        "repository_url": "https://github.com/haiiliin/haiiliin.github.io",
        "use_source_button": True,
        "repository_branch": current_branch,
        "use_edit_page_button": True,
        "use_repository_button": True,
        "use_issues_button": True,
    }
elif html_theme == "sphinx_rtd_theme":
    html_theme_options = {}

# HTML Sidebar configuration -- options available depend on ablog & the Sphinx theme you use.
# The following additional sidebars are provided by ablog:
# * postcard.html provides information regarding the current post
# * recentposts.html lists most recent five posts.
# * authors.html, languages.html, and locations.html sidebars link to author and location archive pages.
# * tagcloud.html provides a tag cloud for post tags
# * categories.html shows categories that you have created for posts
# You can create/include additional pages, by saving them in the _templates directory and including them
# below. See _templates/sidebar-nav.html for an example
if html_theme in ["pydata_sphinx_theme", "sphinx_book_theme"]:
    html_sidebars = {
        "*": ["breadcrumbs", "search-field", "sidebar-nav", "recentposts", "categories", "tagcloud", "archives"],
        "posts": ["breadcrumbs", "search-field", "sidebar-nav", "recentposts", "categories", "tagcloud", "archives"],
        "posts/**": ["breadcrumbs", "search-field", "sidebar-nav", "postcard"],
        "index": ["profile", "projects"],
        "about": ["profile", "projects"],
    }

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = "favicon.ico"

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = ["robots.txt"]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# A list of JavaScript filename. The entry must be a filename string or a tuple containing the filename string and the
# attributes dictionary. The filename must be relative to the html_static_path, or a full URI with scheme like
# https://example.org/script.js. The attributes is used for attributes of <script> tag. It defaults to an empty list.
html_js_files = ["js/rubyhammerhead.js"]

# A list of CSS files. The entry must be a filename string or a tuple containing the filename string and the attributes
# dictionary. The filename must be relative to the html_static_path, or a full URI with scheme like
# https://example.org/style.css. The attributes is used for attributes of <link> tag. It defaults to an empty list.
html_css_files = ["css/rubyhammerhead.css"]

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
html_search_language = "en"

# If true (and html_copy_source is true as well), links to the reST sources will be added to the sidebar.
# The default is True.
html_show_sourcelink = True
