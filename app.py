from flask import Flask, request, jsonify
import yt_dlp
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = Flask(__name__)

# Function to download YouTube video
def download_video(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Google Drive Authentication
def upload_to_drive(file_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    file_drive = drive.CreateFile({'title': os.path.basename(file_path)})
    file_drive.Upload()

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/download', methods=['POST'])
def download_and_upload():
    url = request.json.get('url')
    if not url:
        return jsonify({"status": "error", "message": "URL is required"})
    
    # Download the video
    download_video(url)
    
    # Assuming video is downloaded and saved in 'downloads/video.mp4'
    upload_to_drive('downloads/video.mp4')  # Adjust filename if needed
    return jsonify({"status": "success", "message": "Video downloaded and uploaded to Google Drive"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
