from flask import Flask, request, send_file, jsonify, render_template

import os
from pytube import YouTube
from moviepy.editor import *

app = Flask(__name__)

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

    return jsonify(fileName=f"{video_title}.mp3")

@app.route('/download')
def download():
    video_title = request.args.get('fileName')
    return send_file(video_title, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
