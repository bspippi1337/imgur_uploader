import os
from flask import Flask, render_template, url_for, redirect, request
from imgurpython import ImgurClient

from werkzeug.utils import secure_filename

import requests

# Disable annoying InsecurePlatformWarning
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

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

        # For each uploaded file
        for file in request.files.getlist('files'):

            # If it's a JPEG
            if file.filename.endswith(".jpg") or file.filename.endswith(".jpeg"):
                # Generate the path and save the file
                path = os.path.join(uploads_folder, secure_filename(file.filename))
                file.save(path)

                # Upload the file to imgur
                res = imgur_client.upload_from_path(path)

                # Save the imgur link
                links.append(res['link'])

                # Delete the local file
                os.remove(path)

    return render_template('index.html', links=links)

if __name__ == '__main__':
    app.run()
