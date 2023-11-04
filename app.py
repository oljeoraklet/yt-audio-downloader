import threading
from flask import Flask, request, send_file, jsonify, render_template, g, session
import os
from pytube import YouTube
from moviepy.editor import *
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

def cleanup():
    now = datetime.now()
    for filename in os.listdir('.'):
        print(filename)
        if filename.endswith('.mp3'):
            file_time = datetime.fromtimestamp(os.path.getctime(filename))
            print(file_time)
            if now - file_time > timedelta(minutes=2):
                os.remove(filename)
    # Schedule the cleanup function to run again in 15 minutes
    threading.Timer(15 * 60, cleanup).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['url']
    video = YouTube(url)
    video_title = video.title

    audio_only = video.streams.get_audio_only().download(filename=f"{video_title}.mp4")
    audio = AudioFileClip(f"{video_title}.mp4")
    audio.write_audiofile(f"{video_title}.mp3")
    os.remove(f"{video_title}.mp4")

    # Delete the previous file for this session, if any
    old_filename = session.get('last_file')
    if old_filename:
        try:
            os.remove(old_filename)
        except FileNotFoundError:
            pass  # File was already deleted, nothing to do
    # Store the name of the new file in the session
    session['last_file'] = f"{video_title}.mp3"

    return jsonify(fileName=f"{video_title}.mp3")

@app.route('/download')
def download():
    video_title = request.args.get('fileName')
    return send_file(video_title, as_attachment=True)

if __name__ == '__main__':
    cleanup()  # Start the first cleanup
    app.run(debug=True)
