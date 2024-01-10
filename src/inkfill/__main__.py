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
from typing import Any
from typing import cast
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

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
from . import day_month_year
from . import dollars
from . import month_day_year
from . import nth_of_month_year
from . import NumFormat
from . import plural
from . import Refs
from . import spell_number
from . import to_cardinal
from . import USD

T = TypeVar("T")
"""Generic type variable."""

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
        doc = doc_config(config, idx)
        title = doc.title or f"Untitled Document {(idx + 1)}"
        result += f"""<li><a href="/doc/{idx}">{title}</a></li>"""
    result += "</ul>"
    return result


@app.route("/doc/<idx:int>")
def doc_render(idx: int) -> str:
    """Render the nth document."""
    doc = doc_config(config, idx)
    tmpl = renderer.get_template(doc.template)
    return cast(str, tmpl.render(config=doc, xref=Refs(), Refs=Refs))


def doc_config(config: AttrDict, idx: int) -> AttrDict:
    """Return an interpolated document-specific config."""
    result = AttrDict() << config << config.document[idx]
    result.date = result.date or config.now.date()
    return convert_nested_str(result, result)


def convert_nested_str(item: T, config: AttrDict) -> T:
    """Render deeply-nested strings."""
    if isinstance(item, str):
        item = renderer.from_string(item).render(**config)
    if isinstance(item, dict):
        for key, val in item.items():
            item[key] = convert_nested_str(val, config)
    elif isinstance(item, list):
        for idx, val in enumerate(item):
            item[idx] = convert_nested_str(val, config)
    return item


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
    renderer.filters["plural"] = plural

    renderer.filters["day_of_month"] = nth_of_month_year
    renderer.filters["day_month_year"] = day_month_year
    renderer.filters["month_day_year"] = month_day_year

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

    config = convert_nested_dict(load_config(args.config))
    config.mtime = mtime or args.config.stat().st_mtime
    config.args = args
    config.now = datetime.now()
    config.document = [AttrDict(d) for d in config.document or []]
    print("[inkfill] configuration loaded")
    return config


def convert_nested_dict(obj: Union[Dict[str, Any], List[Any], Any]) -> AttrDict:
    """Return deeply-nested `dict` converted to `AttrDict`."""
    if isinstance(obj, dict):
        return AttrDict({k: convert_nested_dict(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [convert_nested_dict(v) for v in obj]
    return obj


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
