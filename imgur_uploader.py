import os

import sys
from flask import Flask, render_template, url_for, redirect, request, jsonify
from imgurpython import ImgurClient

from werkzeug.utils import secure_filename

import requests

import logging

logging.basicConfig(level=logging.DEBUG)

# Disable annoying InsecurePlatformWarning
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

ACCEPTED_EXTENSIONS = ['.jpg', '.jpeg', '.png']

# Build the uploads folder
current_folder = os.path.dirname(os.path.realpath(__file__))
uploads_folder = os.path.join(current_folder, 'uploads')

@app.route('/', methods=['GET', 'POST'])
def index():
    links = []

    if request.method == 'POST':
        imgur_client_id = os.environ['imgur_client_id']
        imgur_client_secret = os.environ['imgur_client_secret']
        imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

        file_list = request.files.getlist('file')

        if not file_list:
            return jsonify({'ok': False})

        file = file_list[0]
        filename = file.filename

        # If it's an accepted file
        if any(filename.lower().endswith(x) for x in ACCEPTED_EXTENSIONS):
            # Generate the path and save the file
            path = os.path.join(uploads_folder, secure_filename(filename))
            file.save(path)

            # Upload the file to imgur
            res = imgur_client.upload_from_path(path)

            # Delete the local file
            os.remove(path)

            # Return the IMGUR link
            return jsonify({'ok': True, 'link': res['link']})
        else:
            return jsonify({'ok': False})

    return render_template('index.html', links=links)

if __name__ == '__main__':
    app.run()
