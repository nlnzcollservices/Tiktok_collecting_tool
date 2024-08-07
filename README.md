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
- `PySimpleGUI==4.60.5.0`
- `urllib3`

  additional for filtering:

- `fuzzywuzzy
- `python-Levenshtein
- `emoji


## Installation

1. **Clone the repository or download the script file.**

2. **Install the required Python packages:**

   Open a terminal or command prompt and navigate to the directory containing `requirements.txt`, then run:

   ```
   pip install -r requirements.txt
   ```
   
3. **Download geckodriver:**

   Download geckodriver for windows, uzip and place .exe file in the script folder or in other folder indicated in path.
   https://github.com/mozilla/geckodriver/releases
   (Windows releases contain "win" and ".zip")
   
## Usage

1. **Run the script:**

   ```
   python tiktok_gui_tool.py
   ```

2. When little window appears, input link to the TikTok video or profile URL and choose a folder to save the videos.

3. Click "Run!" to start the downloading process.
4. Let the app open a FireFox instance drived by "geckodriver.exe" and selenum. Refresh a page if asked. Complete a cute TikTok puzzle to prove that you are human. 

5. **Filter and Extract Playlist Videos:**
   
Unfortunately, the app cannot download from the playlists. If you would like limited content, use the tool and then filter downloaded video.

If you would like to copy certain playlist videos after collecting to separate folder, you can use `filter_output_by_playlist_tool.py`. Run the script, it will open small window, enter the playlist link, the folder with your videos, and the folder for playlist videos. The script will take all titles from the playlist, compare them with the .description file content, and copy them to the "playlist" folder changing names to titles.


## Maintenance

To ensure the script continues to function correctly:

1. **Keep `yt-dlp` up to date:**

   `yt-dlp` is frequently updated to handle changes in video download sites. Make sure you are using the latest version:

   ```
   pip install --upgrade yt-dlp

   ```


2. **Modify HTML parsing if TikTok changes their page structure:**

If the script stops recognizing video links, you may need to update the BeautifulSoup class selectors. Modify the following lines in the script:

```
lnks_soup = soup.find_all("div", attrs={"class": "css-at0k0c-DivWrapper e1cg0wnj1"})
```
Update the class attribute to match the new HTML structure of the TikTok page.



   
