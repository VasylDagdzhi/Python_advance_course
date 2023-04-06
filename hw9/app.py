# from functools import lru_cache
import json

from flask import Blueprint, render_template

import inspect

import psutil
from flask import Flask, abort, request, Response

from statapi import methods
from statapi.methods import formatters

app = Flask(__name__)

# (!) Warning: normally static files *MUST* be served by
#     web server (e.g. Nginx), NOT Flask
#     But Flask provides a way to serve statics (if needed)
#     for simple projects, development and testing purposes
# (!) Flask adds default /static route to serve files from 'static' dir
# Custom folder for assets (also normally must be served by web server)
assets = Blueprint('assets', __name__, static_folder='assets')
app.register_blueprint(assets, url_prefix='/')


@app.route('/memory')
def memory():
    mem = json.loads(str(methods['virtual_memory']()[0]).replace("\n", ""))
    app.logger.debug('Got memory data:\n\t %r', mem)
    return render_template('memory.html.jinja',
                           pagetitle='Memory statistics',
                           statname='memory',
                           mem=mem
                           )


@app.route('/memory-client')
def memory_client():
    mem = json.loads(str(methods['virtual_memory']()[0]).replace("\n", ""))
    app.logger.debug('Got memory data:\n\t %r', mem)
    return render_template('memory-client.html',
                           pagetitle='Memory statistics',
                           statname='memory',
                           mem=mem
                           )


@app.route('/stats/')
# disabled the caching as it affects the values given to the functions and the way they are parsed
# @lru_cache(maxsize=1)
def stats_root():
    """List all methods."""
    format = request.args.get('format')
    # check if there is a given format value, and it is valid, else raise an error
    if (format is not None) and (format not in formatters):
        abort(400, f'Format {format} is not a valid format. Supported:{[f for f in formatters]}')

    ret = {}
    # if the format is json, toml, yaml or repr
    if format is not None:
        for method in methods:
            # we get each original method from the psutil library
            func = getattr(psutil, method)
            # and its arguments
            argspec = inspect.getfullargspec(func)
            args = argspec.args
            # also the default values if any present
            defaults = argspec.defaults or []
            # and compose an arguments list with their values if any specified
            arg_list = []
            for arg, default in zip(args[::-1], defaults[::-1]):
                arg_list.append(f"{arg}={default!r}")
            arg_str = ", ".join(arg_list[::-1])
            # assign the formatted dict with info and arguments for each method
            ret[method] = {"Info:": func.__doc__, 'Arguments': arg_str}
        # call the correct formatting function in order to have our dict named 'ret' shown in the needed format
        mime, func = formatters.get(format, (None, None))
        # if func is None:
        #     raise ValueError(400, f'Format {format} not supported')
        res = func(ret)
        # return the output in the converted format
        return Response(res, mimetype=mime)
    else:
        # if no format is specified, we return a human-readable output
        i = 0  # row number
        ret = []
        for method in methods:
            i += 1
            # get the original callable function from psutil library to parse its arguments and info
            func = getattr(psutil, method)
            argspec = inspect.getfullargspec(func)
            args = argspec.args
            defaults = argspec.defaults or []
            arg_list = []
            for arg, default in zip(args[::-1], defaults[::-1]):
                arg_list.append(f"{arg}={default!r}")
            arg_str = ", ".join(arg_list[::-1])
            # if the function doesn't take arguments we set them as "None" string
            if len(arg_str) == 0:
                arg_str = "None"
                example = f"http://localhost:5000/stats/{method}"
            # otherwise, parse each argument name and its default value if any
            else:
                arguments = ""  # string of arguments we will use to create a clickable example URL
                j = 0
                for j in range(0, len(arg_list)):
                    arg, val = arg_list[j].split("=")
                    arguments += f"{arg}={val}&"
                # remove the excessive & symbol from the arguments list in the URLs
                if arguments[-1] == "&":
                    arguments = arguments[:-1]
                example = f"http://localhost:5000/stats/{method}?{arguments}"
            ret.append(
                f'<h3>[{i}] [{func.__name__}]</h3><br>Arguments: {arg_str}</br><br>Description: {func.__doc__}</br>'
                f'<br>Example: <a href="{example}">{example}</a></br>')
        return Response(ret, mimetype="text/html")


@app.route('/stats/<string:method>')
def stats(method):
    format = request.args.get('format', 'json')  # automatically assign the default format to 'json' if not specified

    # in case an invalid format is specified:
    if (format is not None) and (format not in formatters):
        abort(400, f'Format {format} is not a valid format. Supported:{[f for f in formatters]}')

    try:
        func = methods[method]
    except KeyError:
        abort(404, f'Method {method} not found')

    try:
        if format is None:
            # call method with no arguments
            res, mime = func()
        else:
            # get arguments from query parameters
            args = {}
            for arg_name in request.args:
                value = request.args.get(arg_name)
                # during tests found that boolean values aren't correctly parsed, so done it manually
                if value == "False":
                    args[arg_name] = False
                elif value == "True":
                    args[arg_name] = True
            # call method with arguments, including the format if specified
            res, mime = func(**args)
    except Exception as exc:
        abort(400, exc)  # in case something is not right, catch and print the error

    app.logger.debug('Got memory data:\n\t %r', res)

    return Response(res, mimetype=mime)


if __name__ == '__main__':
    # We need to set logging to be able to see everything
    import logging

    app.logger.setLevel(logging.DEBUG)

    # (!) Never run your app on '0.0.0.0 unless you're deploying
    #     to production, in which case a proper WSGI application
    #     server and a reverse-proxy is needed
    #     0.0.0.0 means "run on all interfaces" -- insecure
    app.run(host='127.0.0.1', port=5000, debug=True)
