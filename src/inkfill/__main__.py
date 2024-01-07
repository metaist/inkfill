#!/usr/bin/env python
# type: ignore
"""Generate documents using configurable templates.

Usage: inkfill [--help | --version] [--debug] <config>

Options:
  -h, --help                    show this message and exit
  --version                     show program version and exit
  --debug                       show debug messages
  <config>                      configuration file
"""
# std
from datetime import datetime
from datetime import timedelta
from os import environ as ENV
from pathlib import Path
from typing import cast
from typing import List
from typing import Optional

# lib
from attrbox import AttrDict
from attrbox import load_config
from attrbox import parse_docopt
from bottle import Bottle
from bottle import static_file
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined
from timeloop import Timeloop
import bottle

# pkg
from . import __version__
from . import commafy
from . import compound
from . import nth_of_month_year
from . import dollars
from . import NumFormat
from . import Refs
from . import spell_number
from . import to_cardinal
from . import USD

PATH_VIEWS = Path(__file__).parent.resolve() / "views"
"""Path to views."""

bottle.debug(True)
app = Bottle()
"""`bottle` web server."""

args = None
"""`docopt` arguments."""

config = None
"""`toml` configuration."""

renderer = None
"""`jinja2` environment."""

tl = Timeloop()
"""`timeloop` periodic scheduler."""


@app.route("/static/<path>")
def static(path: str):
    """Serve a static file."""
    return static_file(path, root=PATH_VIEWS / "static")


@app.route("/")
def doc_list() -> str:
    """List of possible documents."""
    result = "<ul>"
    for idx, doc in enumerate(config.document):
        title = doc.title or "Untitled Document " + (idx + 1)
        title = title.format(**config)
        result += f"""<li><a href="/doc/{idx}">{title}</a></li>"""
    result += "</ul>"
    return result


@app.route("/doc/<idx:int>")
def doc_render(idx: int) -> str:
    """Render the nth document."""
    doc = config.document[idx]
    path = (doc.template or "").format(**config)
    tmpl = renderer.get_template(path)
    config_doc = AttrDict() << config << doc
    for key, val in config_doc.items():
        if isinstance(val, str):
            config_doc[key] = val.format(**config)
    return cast(str, tmpl.render(config=config_doc, xref=Refs(), Refs=Refs))


def setup_jinja() -> Environment:
    """Set up the jinja environment."""
    global renderer

    user_path = ENV.get("INKFILL_PATH", "~/.config/inkwell")
    paths = [
        Path(".").resolve(),  # current working directory
        args and args.config.parent,  # directory that the configuration file is in
        Path(user_path).expanduser(),  # user directory
        PATH_VIEWS,  # base templates
    ]

    renderer = Environment(loader=FileSystemLoader(paths), undefined=StrictUndefined)
    renderer.filters["compound"] = compound
    renderer.filters["day_of_month"] = nth_of_month_year

    renderer.filters["dollars"] = dollars
    renderer.filters["USD"] = USD

    renderer.filters["commafy"] = commafy
    renderer.filters["num_format"] = lambda num, format: NumFormat.get(format)(num)
    renderer.filters["say_number"] = to_cardinal
    renderer.filters["spell_number"] = spell_number
    return renderer


def setup_config(mtime: int = 0) -> AttrDict:
    """Setup the config."""
    global config

    config = AttrDict(load_config(args.config))
    config.mtime = mtime or args.config.stat().st_mtime
    config.args = args
    config.now = datetime.now()
    config.document = [AttrDict(d) for d in config.document or []]
    print("[inkfill] configuration loaded")
    print(config)
    return config


@tl.job(timedelta(seconds=1.5))
def check_config() -> None:  # pragma: no cover
    """Periodically reload config, if needed."""
    mtime = args.config.stat().st_mtime
    if config and config.mtime == mtime:  # no change
        return
    elif config:  # changed
        print("[inkfill] reloading configuration")
        setup_config(mtime)


def main(argv: Optional[List[str]] = None) -> None:  # pragma: no cover
    """Parse args."""
    global args
    args = parse_docopt(__doc__, argv=argv, version=__version__, read_config=False)
    args.config = Path(cast(str, args.config)).resolve()

    setup_config()
    setup_jinja()

    tl.start()
    app.run(reloader=True)


if __name__ == "__main__":  # pragma: no cover
    main()
