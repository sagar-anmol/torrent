# torrent_downloader.py

import libtorrent as lt
import time
from flask import Flask, render_template_string, request
from flask_ngrok import run_with_ngrok

# Initialize the torrent session
ses = lt.session()
downloads = []

# Function to add a torrent from a magnet link
def add_torrent(magnet_link):
    params = {
        'save_path': './downloads/',
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True}
    handle = lt.add_magnet_uri(ses, magnet_link, params)
    downloads.append(handle)

# Function to get the status of all torrents
def download_status():
    statuses = []
    for handle in downloads:
        s = handle.status()
        statuses.append(f"Name: {s.name}, State: {s.state}, Progress: {s.progress * 100:.2f}%")
    return "<br>".join(statuses)

# Initialize the Flask app
app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

# Define the home route with the user panel
@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Torrent Downloader</title>
    </head>
    <body>
        <h1>Enter Torrent Magnet Link</h1>
        <form action="/add" method="post">
            <input type="text" name="magnet" placeholder="Paste Magnet Link Here">
            <button type="submit">Add Torrent</button>
        </form>
        <h2>Download Status</h2>
        <iframe src="/status" width="600" height="400"></iframe>
    </body>
    </html>
    ''')

# Route to handle adding a torrent
@app.route('/add', methods=['POST'])
def add():
    magnet_link = request.form['magnet']
    add_torrent(magnet_link)
    return "Torrent added successfully! <a href='/'>Go back</a>"

# Route to display the download status
@app.route('/status')
def status():
    return download_status()

# Run the Flask app
if __name__ == "__main__":
    app.run()
