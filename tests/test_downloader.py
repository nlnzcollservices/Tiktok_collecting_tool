import os
import pytest
from unittest.mock import patch, MagicMock
import yt_dlp

# Import the function to be tested
def download_video(link, video_path, video_folder):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'ignoreerrors': True,
        'writedescription': True,
        'nocheckcertificate': True,
        'writecomments': True,
        'writedescription': True,
        'writeinfojson': True,
        'mergeoutputformat': 'mp4',
    }
    print("here!!!")
    print(link)
    print(video_path)
    print(video_folder)
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    try:
        print("here")
        ydl_opts['outtmpl'] = video_path
        print(ydl_opts)
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download([link])
        flag = True
    except Exception as e:
        print(str(e))
        flag = False
    return flag

# Test case
@pytest.mark.parametrize("link, video_path, video_folder, expected", [
    ("your_link_to_video", "7266307715595586818", "TIKTOK", True),
])
def test_download_video(link, video_path, video_folder, expected):
    with patch("os.makedirs") as mock_makedirs, \
         patch("os.path.exists", return_value=False), \
         patch("yt_dlp.YoutubeDL") as mock_yt_dlp:
        
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value = mock_ydl_instance
        mock_ydl_instance.download.return_value = None  # Simulate successful download
        
        result = download_video(link, video_path, video_folder)
        
        mock_makedirs.assert_called_once_with(video_folder)
        mock_yt_dlp.assert_called_once()
        mock_ydl_instance.download.assert_called_once_with([link])
        
        assert result == expected

if __name__ == "__main__":
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change the working directory to the test directory (assuming 'tests' folder is in the current directory)
    test_dir = os.path.join(current_dir)
    
    # Run the tests in the 'tests' directory
    pytest.main([test_dir])
