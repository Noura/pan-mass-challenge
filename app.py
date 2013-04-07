#!/usr/bin/env python
import os
import sys
from flask import Flask, render_template, request
from werkzeug import secure_filename
import jinja2
import json

import database
from secret_constants import PASSWORD, ADMIN_PASSWORD

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = 'static/uploads/photos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
db = database.get_database()

def file_ext(filename):
    return filename.rsplit('.', 1)[1]

def allowed_file(filename):
    return '.' in filename and \
        file_ext(filename) in ALLOWED_EXTENSIONS

def next_counter():
    filenames = os.listdir(os.path.join(THIS_DIR, PHOTOS_DIR))
    biggest = max([int(x.split('.')[0]) for x in filenames])
    return biggest + 1

@app.route('/')
def home():
    ctx = {'tab': 'home'}
    return render_template('index.html', **ctx)

@app.route('/photos/', methods=['GET', 'POST'])
def photos(admin=False):
    ctx = {
        'errors': {},
        'tab': 'photos',
        'values': {},
        'admin': admin,
    }
    # adding a photo
    if request.method == 'POST' and not admin:
        password = request.form.get('password', None)
        f = request.files.get('file', None)
        user = request.values.get('user', None)
        caption = request.values.get('caption', None)
        desc = request.values.get('desc', None)
        ctx['values'] = dict(user=user, caption=caption, desc=desc, password=password)
        if not password:
            ctx['errors']['password'] = True
        if password != PASSWORD:
            ctx['errors']['password'] = True
        if not f:
            ctx['errors']['file'] = True
        if not allowed_file(f.filename):
            ctx['errors']['file'] = True
        if not user:
            ctx['errors']['user'] = True
        if not caption:
            ctx['errors']['caption'] = True
        if not desc:
            ctx['errors']['desc'] = True
        if ctx['errors'] == {}:
            ctx['values'] = {}
            filename = secure_filename(f.filename)
            f.save(os.path.join(THIS_DIR, PHOTOS_DIR, filename))
            db.add_photo(filename, caption, user, desc)

    # showing the page of photos
    ctx['photos'] = db.get_photos()
    ctx['prefix'] = PHOTOS_DIR
    ctx['values_json'] = json.dumps(ctx['values'])
    return render_template('photos.html', **ctx)

@app.route('/admin/', methods=['GET', 'POST'])
def photos_admin():
    # deleting a photo
    if request.method == 'POST':
        password = request.form.get('admin_password', None)
        pid = request.form.get('pid', None)
        if password == ADMIN_PASSWORD and pid:
            db.delete_photo(pid)
            #TODO delete photo file

    # showing admin page of photos
    return photos(True)
   

if __name__ == '__main__':
    app.run()
