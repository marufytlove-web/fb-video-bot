import os
import requests
import yt_dlp
import glob

# ==========================================
# ১. টার্গেট পেজের লিংক (যেখান থেকে ভিডিও নামবে)
# ==========================================
TARGET_PAGE_URL = "https://www.facebook.com/profile.php?id=61560510194649" 
# (উপরের লিংকটি পরিবর্তন করে আপনি যে পেজ থেকে ভিডিও নিতে চান তার লিংক দিন)

# ২. সিক্রেট কনফিগারেশন (GitHub থেকে আসবে)
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
PAGE_ID = os.environ.get("PAGE_ID")

def download_video():
    print("Bot started: Looking for latest video...")
    
    # ভিডিও ডাউনলোড করার অপশন
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': False,
        'playlist_end': 1, # শুধু লেটেস্ট ১টি ভিডিও নামবে
        'noplaylist': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([TARGET_PAGE_URL])
        print("Download Success!")
        return True
    except Exception as e:
        print(f"Download Failed: {e}")
        return False

def upload_to_facebook():
    # ডাউনলোড করা ফাইলটি খুঁজে বের করা
    files = glob.glob("downloaded_video.*")
    if not files:
        print("No video file found to upload.")
        return
    
    video_filename = files[0]
    print(f"Uploading file: {video_filename}")
    
    url = f"https://graph-video.facebook.com/v18.0/{PAGE_ID}/videos"
    
    params = {
        'access_token': ACCESS_TOKEN,
        'description': 'Latest video update! #viral #video' # ক্যাপশন এখানে বদলাতে পারেন
    }
    
    with open(video_filename, 'rb') as f:
        files_data = {'source': f}
        response = requests.post(url, params=params, files=files_data)
    
    print("Facebook Upload Response:", response.json())

if __name__ == "__main__":
    if download_video():
        upload_to_facebook()
    else:
        print("Skipping upload due to download error.")
