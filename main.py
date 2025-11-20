import os
import requests
import yt_dlp
import glob

# ১. পেজের লিংক (যেখান থেকে ভিডিও নামবে)
TARGET_PAGE_URL = "https://www.facebook.com/watch/100063631665336" 

# ২. সিক্রেট কনফিগারেশন
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
PAGE_ID = os.environ.get("PAGE_ID")

def download_video():
    print("Bot started: Looking for latest video...")
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': False,
        'playlist_end': 1,
        'noplaylist': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([TARGET_PAGE_URL])
        return True
    except Exception as e:
        print(f"Download Failed: {e}")
        return False

def upload_to_facebook():
    files = glob.glob("downloaded_video.*")
    if not files:
        return
    
    video_filename = files[0]
    url = f"https://graph-video.facebook.com/v18.0/{PAGE_ID}/videos"
    
    params = {
        'access_token': ACCESS_TOKEN,
        'description': 'Video collected from internet #reels #fb'
    }
    
    with open(video_filename, 'rb') as f:
        files_data = {'source': f}
        requests.post(url, params=params, files=files_data)

if __name__ == "__main__":
    if download_video():
        upload_to_facebook()
