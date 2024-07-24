# TikTok Video Downloader

This Python script allows you to download videos from TikTok. It can handle both single video links and profile links, downloading all available videos from the specified profile. The script utilizes `selenium` with `Firefox` and `yt-dlp` for downloading the videos. A graphical user interface (GUI) is provided using `PySimpleGUI`.

## Features
- Download single TikTok videos or all videos from a profile.
- Handle invalid URLs and display appropriate error messages.
- User-friendly GUI for input and feedback.
- Automatically scrolls through the TikTok profile page to load all videos.

## Requirements
- Python 3.x
- `requests`
- `selenium`
- `beautifulsoup4`
- `yt-dlp`
- `PySimpleGUI==4.55.1`
- `urllib3`

## Installation

1. **Clone the repository or download the script files.**

2. **Install the required Python packages:**

   Open a terminal or command prompt and navigate to the directory containing `requirements.txt`, then run:

   ```sh
   pip install -r requirements.txt
