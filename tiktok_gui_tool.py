
import subprocess
import configparser
import os
import sys
import json
import csv
import requests
from time import sleep
from datetime import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import yt_dlp
import PySimpleGUI as sg
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()

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
def is_valid_url(url):
    """Check if the provided URL is valid."""
    try:
        result = requests.get(url, verify=False)
        return result.status_code == 200
    except:
        return False

def my_gui():
    scheme = "LightGreen2"
    sg.theme(scheme)
    layout = [
        [sg.Text('Insert link to tiktok web page', font=('Helvetica', 13, 'bold italic'))],
        [sg.Text('Full path with tag or username', font=('Helvetica', 11, 'italic'))],
        [sg.Text('Tiktok link', size=(10, 1)), sg.InputText("", key='url', size=(100, 1))],
        [sg.Text('', size=(100, 1)), sg.FolderBrowse('FolderBrowse', key='foldername')],
        [sg.Button("Run!"), sg.Button("Quit")]
    ]
    window = sg.Window('TikTok downloader', layout, default_element_size=(35, 2))
    return window

def is_single_video(url):
    """Check if the provided URL is a single video link."""
    return "/video/" in url

def get_tiktok_videos(url, storage_folder):
    """
    Gets a single video from a given tiktok page URL or collects videos from a profile.
    Updates the item() data object.
    """
    flag_collected = False
    print(url)

    if is_single_video(url):
        # If it's a single video link, download that video
        print("Single url")
        video_link = str(url)
        video_id = url.split("/")[-1]
        author = url.split("/")[-3].lstrip("@")
        video_title = author +"_" +video_id
        flag_collected = download_video(video_link, video_title, storage_folder)
    else:
        # If it's a profile link, collect and download all videos
        items = []
        driver = webdriver.Firefox()
        print("Driver activated")
        if not os.path.exists(storage_folder):
            os.makedirs(storage_folder)
        downloaded_files = os.listdir(storage_folder)
        print("Already downloaded")
        print(downloaded_files)
        driver.set_window_size(768, 1024)
        driver.get(url)
        driver.maximize_window()
        sleep(2)
        driver.get(url)
        sleep(15)

        scroll_down(driver)
        my_links = []
        my_links_dict = {}
        soup = bs(driver.page_source, 'html.parser')
        print(soup.text)
        items = []
        itms_titles = {}
        lnks_soup = soup.find_all("div", attrs={"class": "css-at0k0c-DivWrapper e1cg0wnj1"})
        if not lnks_soup:
            sg.Print("Failed. Either No URLs found in the TikTok profile or run again and do not forget to 'refresh' or/and solve cute Tiktok puzzle in your FireFox instance.")
            flag_collected=False
        else:
            for lnk_soup in lnks_soup:
                lnk = lnk_soup.find("a").attrs["href"]
                items.append(lnk)
                title = lnk_soup.find("img").attrs["alt"]
                itms_titles[lnk] = title

            video_collector(items, storage_folder, itms_titles, downloaded_files)
            flag_collected = True

    return flag_collected

def scroll_down(driver):
    """
    A method for scrolling the page.
    Origin: #https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    sg.Print("Scrolling...")
    print("Scrol_down")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(6)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def download_video(link, video_path, video_folder):
    print("Downloading")
    print(link)
    print(video_path)
    print(video_folder)
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    try:
        ydl_opts['outtmpl'] = video_path
        print(ydl_opts)
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download([link])
        flag = True
    except:
        flag = False
    return flag

def parse_link(storage_folder, video_id):
    video_path = os.path.join(storage_folder, video_id, video_id + ".mp4")
    video_folder = os.path.join(storage_folder, video_id)
    return video_path, video_folder

def video_collector(items, storage_folder, itms_titles, downloaded_files):
    """Gets list of video links and then downloads each video. Set item.flag = True if complete."""
    print("Videos")
    #print(os.getcwd())

    if not os.path.exists(storage_folder):
        os.makedirs(storage_folder)
    downloaded_files = os.listdir(storage_folder)
    print(items)
    for itm in items:
        print(itm)
        sg.Print("Collecting " + itm)
        video_id = itm.split("/")[-3].lstrip("@") + "_" + itm.split("/")[-1]
        if not video_id in downloaded_files:
            download_path, download_folder = parse_link(storage_folder, video_id)
            flag = download_video(itm, download_path, download_folder)
            if not os.path.exists(download_path) or os.path.getsize(download_path) == 0:
                flag = download_video(itm, download_path, download_folder)
            if flag:
                with open(os.path.join(storage_folder, "links_processed.txt"), "a") as f:
                    f.write(itm)
                    f.write("\n")
                with open(os.path.join(storage_folder, "links_titles.txt"), "a", encoding="UTF-8") as f:
                    f.write(itm + "|||" + itms_titles[itm])
                    f.write("\n")
        else:
            print("Video exists")
            sg.Print("Video exists")
            flag= True

    completed_flag = flag
    return flag

def main():
    while True:
        window = my_gui()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Quit'):
            window.close()
            break
        foldername = values.get("foldername")
        url = values.get("url")
        
        if not foldername or not url:
            sg.Print("No folder or link provided")
        elif not is_valid_url(url):
            sg.Print("Invalid URL provided")

        else:
            try:
                sg.Print('Collecting from ', url)
                get_tiktok_videos(url, foldername)
                sg.Print("Done.")
            except Exception as e:
                sg.Print(f"An error occurred: {e}")
        window.close()

if __name__ == '__main__':
    main()
