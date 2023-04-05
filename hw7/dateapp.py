import inspect
import logging
from datetime import datetime, timedelta
from typing import Any

from flask import Flask, abort, request

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


def generate_docstring(function: Any) -> str:
    """
    Generate docstring for the given function by separating the processing logic into a separate function.

    :param function: The function to generate docstring for.
    :return: The docstring for the given function.
    """
    arg_spec = inspect.getfullargspec(function)
    args = arg_spec.args
    defaults = arg_spec.defaults

    signature = f"{function.__name__}("
    for i, arg in enumerate(args):
        signature += arg
        if defaults and i >= len(args) - len(defaults):
            default_index = len(args) - len(defaults) + i
            signature += f"={defaults[default_index]}"
        if i < len(args) - 1:
            signature += ", "
    signature += ")"

    processing_function = inspect.getsource(function).split("\n")[1:]
    processing_function = "\n".join([f"    {line}" for line in processing_function])

    docstring = f"{function.__doc__}\n\n" if function.__doc__ else ""
    docstring += f"{signature}\n\n"
    docstring += f"{processing_function}\n\n"

    return docstring


@app.route('/')
@app.route('/<name>')
def basic(name: str = "Flask") -> str:
    """
    Returns an HTML greeting with the given name.

    :param name: The name to include in the greeting.
    :return: An HTML greeting.
    """

    route = request.path
    app.logger.info(f'Reached route "{route}". Param: {name}')
    return f'<h1>Wazzup, {name}?</h1>'


@app.route('/datetime')
def datetime_info() -> str:
    """
    Returns an HTML page with instructions for using the datetime route.

    :return: An HTML page with instructions for using the datetime route.
    """
    route = request.path
    app.logger.info(f'Reached route "{route}"')
    return '<html><head><h2>This page returns the date and time in the specified time zone.<h2></head>' \
           '<body><p>Usage:</p>' \
           '<a href="http://127.0.0.1:5000/datetime/+2">http://127.0.0.1:5000/datetime/+2</a>' \
           '<p>Will return the current date and time in +2 time zone.</p></body></html>'


@app.route('/datetime/')
@app.route('/datetime/<time>')
def datetime_default(time: str = "0") -> str:
    """
    Returns an HTML page with the current date and time in the specified time zone.

    :param time: The time zone offset in hours.
    :return: An HTML page with the current date and time in the specified time zone.
    """
    try:
        offset = int(time)
        if offset < -12 or offset > 14:
            raise ValueError
    except ValueError:
        return abort(406, f'Invalid timezone: "{time}".')

    if offset == 0:
        now = datetime.utcnow()
    else:
        now = datetime.now()
    tzoffset = timedelta(hours=offset)
    route = request.path
    app.logger.info(f'Reached route "{route}". Param: {time}')
    return f'<html><head><h2>Current time in UTC{time} is:<h2></head>' \
           f'<body><p>{(now + tzoffset).strftime("%Y-%m-%d %H:%M:%S")}</p>' \
           '</body></html>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
