from pathlib import Path

from sphinx.application import Sphinx
from sphinx.config import Config

from jinja2 import Template

try:
    import tomllib as toml
except ImportError:
    import tomli as toml


class Dict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class PaperConfig(Dict):
    blogpost: bool = True
    date: str
    author: str
    category: str = "Paper"
    tags: str
    language: str = "English"

    title: str
    doi: str
    abstract: str
    pdf: str

    google_scholar_link: str
    scopus_link: str


def generate(app: Sphinx, config: Config):
    if not config.bibliography_generate:
        return

    # Read the configuration file
    bibtmp = Path(config.bibliography_template)
    bibconf = Path(config.bibliography_conf)
    biboutdir = Path(config.bibliography_outdir)

    # Read the template
    with bibtmp.open("r") as f:
        template = Template(str(f.read()))

    # Read the configuration file
    biboutdir.mkdir(parents=True, exist_ok=True)
    with bibconf.open("rb") as f:
        conf = toml.load(f)

    # Generate the blog posts
    for key, paper in conf["papers"].items():
        conf = PaperConfig(paper)
        title = conf.title.replace(" ", "+")
        conf.google_scholar_link = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={title}"
        conf.scopus_link = f"https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1={title}&" \
                           f"sot=b&sdt=b&sl=107&s=TITLE-ABS-KEY%28{title}%29&origin=searchbasic&editSaveSearch=&" \
                           f"yearFrom=Before+1960&yearTo=Present"
        with (biboutdir / f"{key}.md").open("w") as f:
            f.write(template.render(**conf))


def setup(app: Sphinx):
    app.add_config_value("bibliography_generate", True, "env")
    app.add_config_value("bibliography_template", "_templates/paper.md", "env")
    app.add_config_value("bibliography_conf", "papers.toml", "env")
    app.add_config_value("bibliography_outdir", "posts/papers", "env")
    app.connect("config-inited", generate)
