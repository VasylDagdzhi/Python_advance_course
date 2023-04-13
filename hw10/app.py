import os

from logic import Application
from utils.textcut import cutter
import logging
import utils
from flask import Flask, abort, send_file, render_template, url_for, send_from_directory, request
import requests
import PIL.Image

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/')
def home():
    return render_template('ultracat.html', title=Application.page_title, mimetype='text/html')


@app.route('/cats/')
def list_cats():
    return render_template('cats.html', title=Application.page_title, cat_count=Application.get_cat_count(),
                           mimetype='text/html', cats=Application.get_cats())


@app.route('/cats/<path:filename>')
def get_cat_image(filename):
    return send_from_directory('static/cats', filename)


@app.route('/cats/create')
def cat_create():
    return render_template('create.html', title=Application.page_title, cat_count=Application.get_cat_count(),
                           mimetype='text/html', cats=Application.get_cat_urls())


@app.route('/cats/cat<int:num>.<string:ext>')
def cat_original(num, ext):
    file, base, ext = Application.get_cat(f'{num}.{ext}', try_random=False)
    name = f'cat{base}{ext}'  # the filename passed to browser
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
    return send_file(file, as_attachment=False, download_name=name)


@app.route('/cats/catoftheday<name>')
def cat_modified(name):
    file, base, ext = Application.get_cat(name, try_random=True)
    date = utils.DateTriple()  # try UADateTriple() here
    date_suffix = date.tostr(fmt='{day}_{month:.3}').lower()
    text = date.tostr(fmt='{weekday:.3},\n{day}\n{month:.3}')
    try:
        img = PIL.Image.open(file)
        bgcolor = (255, 255, 255, int(255 * 0.4))
        cut = cutter.text_cutout(img, text, bgcolor=bgcolor)
        if ext in ['.jpg', '.jpeg', '.jfif']:
            # eliminate alpha-channel as JPEG has no alpha
            cut = cut.convert('RGB')
        file = utils.ImageIO(cut, ext=ext)
    except utils.ImageIOError as err:
        abort(400, str(err))

    # passed to browser
    name = f'catoftheday{base}-{date_suffix}{ext}'
    return send_file(file, as_attachment=False, download_name=name)


@app.route('/cats/upload_cat', methods=['POST'])
def cat_upload():
    image = request.files['image']
    top_text = request.form['top-text']
    bottom_text = request.form['bottom-text']

    date_suffix = utils.DateTriple().tostr(fmt='{day}_{month:.3}').lower()
    ext = f'.{image.filename.split(".")[-1]}'
    base = image.filename.split(".")[:-1][0]
    # generate a name for the image to be saved with
    name = f'{base}-{date_suffix}{ext}'

    image.save(os.path.join(app.static_folder, 'cats', name))
    text = f"{top_text}\n{bottom_text}"
    try:
        file = Application.find_cat_file_by_name(name)
        img = PIL.Image.open(file)
        bgcolor = (255, 255, 255, int(255 * 0.4))
        cut = cutter.text_cutout(img, text, bgcolor=bgcolor)
        if ext in ['.jpg', '.jpeg', '.jfif']:
            # eliminate alpha-channel as JPEG has no alpha
            cut = cut.convert('RGB')
        file = utils.ImageIO(cut, ext=ext)
    except utils.ImageIOError as err:
        abort(400, str(err))
    # passed to browser
    name = f'catoftheday{base}-{date_suffix}{ext}'
    return send_file(file, as_attachment=True, download_name=name)


@app.route('/cats/create_cat/<string:name>/<string:top_text>/<string:bottom_text>', methods=['GET'])
def create_cat(name: str, top_text: str, bottom_text: str):
    logger.debug(f'Debug message: {name} | {top_text} | {bottom_text}')
    image = Application.find_cat_file_by_name(name)
    text = f"{top_text}\n{bottom_text}"
    try:
        file = Application.find_cat_file_by_name(name)
        img = PIL.Image.open(file)
        bgcolor = (255, 255, 255, int(255 * 0.4))
        cut = cutter.text_cutout(img, text, bgcolor=bgcolor)
        if image.suffix in ['.jpg', '.jpeg', '.jfif']:
            # eliminate alpha-channel as JPEG has no alpha
            cut = cut.convert('RGB')
        file = utils.ImageIO(cut, ext=image.suffix)
    except utils.ImageIOError as err:
        abort(400, str(err))
    # passed to browser
    return send_file(file, as_attachment=True, download_name=name)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
