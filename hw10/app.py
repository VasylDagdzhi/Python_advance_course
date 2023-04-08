import os

import catday
import utils
from flask import Flask, Response, abort, send_file, render_template, url_for, send_from_directory
import PIL.Image
import io
import logging
import random

from time import perf_counter

app = Flask(__name__)
page_title = "Cat of the day!"


@app.route('/')
def home():
    return render_template('ultracat.html', title=page_title, mimetype='text/html')


# Note:
#   If a rule ends with a slash and is requested without a slash by the user,
#   the user is automatically redirected to the same page with a trailing 
#   slash attached.
#   If a rule does not end with a trailing slash and the user requests
#   the page with a trailing slash, a 404 not found is raised.
# So we try to always define rules with trailing slashes '/'

@app.route('/cats/')
def list_cats():
    cat_count = len(catday.CATS)
    return render_template('cats.html', title=page_title, cat_count=cat_count, mimetype='text/html', cats=catday.CATS)


@app.route('/cats/<path:filename>')
def get_cat_image(filename):
    return send_from_directory('cats', filename)


@app.route('/cats/create')
def cat_create():
    cat_count = len(catday.CATS)
    image_urls = [url_for('get_cat_image', filename=os.path.basename(path)) for path in catday.CATS]
    return render_template('create.html', title=page_title, cat_count=cat_count, mimetype='text/html', cats=image_urls)


def get_cat(numext, try_random=False):
    try:
        ret = catday.find_cat_file(numext=numext,
                                   try_random=try_random)
    except ValueError:  # integer unconvertable or wrong range
        abort(404, 'Wrong image number')
    else:
        app.logger.debug('Retrieve image "%s" for '
                         'base %s with ext "%s"',
                         *ret)
        return ret


@app.route('/cats/cat<int:num>.<string:ext>')
def cat_original(num, ext):
    t_start = perf_counter()  # measure request time

    file, base, ext = get_cat(f'{num}.{ext}', try_random=False)

    name = f'cat{base}{ext}'  # the filename passed to browser

    app.logger.debug('Original extension is %s', file.suffix)

    # if the extension is different, perform conversion with PIL
    if ext.lower() != file.suffix.lower():

        try:
            img = PIL.Image.open(file)
            # Save to buffer in memory and serve with Flask
            buf = utils.ImageIO(img, ext=ext)
        except utils.ImageIOError as err:
            abort(400, str(err))
        else:
            # now our file gets mocked by conversion result
            file = buf

    # if the file has the same extension,
    # don't convert at all and return directly

    took = perf_counter() - t_start

    if app.logger.isEnabledFor(logging.DEBUG):
        msg = f'Request took {took * 1000:.2f} ms'
        app.logger.debug(msg)

    return send_file(file, as_attachment=False, download_name=name)


@app.route('/cats/catoftheday<name>')
def cat_modified(name):
    file, base, ext = get_cat(name, try_random=True)

    date = utils.DateTriple()  # try UADateTriple() here
    date_suffix = date.tostr(fmt='{day}_{month:.3}').lower()

    text = date.tostr(fmt='{weekday:.3},\n{day}\n{month:.3}')

    try:
        img = PIL.Image.open(file)
        bgcolor = (255, 255, 255, int(255 * 0.4))
        cut = catday.cutter.text_cutout(img, text, bgcolor=bgcolor)
        if ext in ['.jpg', '.jpeg', '.jfif']:
            # eliminate alpha-channel as JPEG has no alpha
            cut = cut.convert('RGB')
        file = utils.ImageIO(cut, ext=ext)
    except utils.ImageIOError as err:
        abort(400, str(err))

    # passed to browser
    name = f'catoftheday{base}-{date_suffix}{ext}'
    return send_file(file, as_attachment=False, download_name=name)


if __name__ == '__main__':
    import logging

    app.logger.setLevel(logging.DEBUG)
    app.run(host='127.0.0.1', port=5000, debug=True)
