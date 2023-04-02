from functools import lru_cache

from flask import Flask, abort, request, Response

from statapi import methods
from statapi.methods import formatters

app = Flask(__name__)


@app.route('/stats/')
@lru_cache(maxsize=1)  # can use cuz no flask proxies referred
def stats_root():
    """List all methods."""
    ret = {'methods': list(methods)}
    return ret  # auto-converted to json by flask


@app.route('/stats/<string:method>')
def stats(method):
    format = request.args.get('format')

    if format not in formatters:
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
                args[arg_name] = request.args.get(arg_name)
            # call method with arguments, including the format if specified
            res, mime = func(**args)
    except Exception as exc:
        abort(400, exc)

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
