from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download_video', methods=['POST'])
def download_video():
    video_url = request.form['url']
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        temp_folder = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_folder, yt.title + '.mp4')
        stream.download(output_path=temp_folder, filename=yt.title + '.mp4')

        return send_file(temp_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error downloading {video_url}: {str(e)}'})


@app.route('/download_audio', methods=['POST'])
def download_audio():
    audio_url = request.form['audio-url']
    try:
        yt = YouTube(audio_url)
        stream = yt.streams.get_audio_only()

        temp_folder = tempfile.mkdtemp()
        print(temp_folder)
        temp_file_path = os.path.join(temp_folder, yt.title + '.mp3')
        print(temp_file_path)
        os.chdir(temp_folder)
        stream.download(output_path=temp_folder, filename=yt.title + '.mp3')

        return send_file(temp_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error downloading {audio_url}: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
