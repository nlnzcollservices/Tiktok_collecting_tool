import os
import re
import shutil
import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from fuzzywuzzy import fuzz
import PySimpleGUI as sg
import emoji



def is_valid_url(url):
    try:
        result = requests.get(url, verify=False)
        return result.status_code == 200
    except:
        return False

def my_gui():
    scheme = "LightGreen2"
    sg.theme(scheme)
    layout = [
        [sg.Text('Insert playlist TikTok link to filter results', font=('Helvetica', 13, 'bold italic'))],
        [sg.Text('Playlist link', size=(10, 1)), sg.InputText("", key='url', size=(100, 1))],
        [sg.Text('Input folder', size=(10, 1)), sg.InputText("", key='foldername', size=(100, 1)), sg.FolderBrowse('InputFolderBrowse')],
        [sg.Text('Output folder', size=(10, 1)), sg.InputText("", key='out_foldername', size=(100, 1)), sg.FolderBrowse('OutputFolderBrowse')],
        [sg.Button("Run!"), sg.Button("Quit")]
    ]
    window = sg.Window('TikTok downloader', layout, default_element_size=(35, 2))
    return window

def get_page_source(url):
    """Open the TikTok page and return the page source."""
    driver = webdriver.Firefox()
    driver.get(url)
    sleep(10)  # Increase sleep time if needed to allow the page to load completely
    soup = bs(driver.page_source, 'html.parser')
    driver.quit()
    return soup



def remove_emoji(string):
    """Remove all emojis from a string."""
    return emoji.replace_emoji(string, replace='')

def parse_soup(soup):
    """Extract and clean titles from the page source."""
    text = soup.get_text()


    my_titles = re.findall(r'\d{2}(.*?)(?=views)', text)
    print(my_titles)

    my_titles[0]= my_titles[0].split("01")[-1]
    my_titles[0] = " ".join(my_titles[0].split(" ")[:-2])
    # Split by "01", "02", ..., "10", "11", etc.
    # parts = re.split(r'(\d{2})', text)
    
    # # Filter out empty strings and numbers, keep the titles
    # titles = [parts[i].strip() for i in range(2, len(parts), 3)]

    # # Clean each title by splitting at '#' and removing emojis
    cleaned_titles = []
    for title in my_titles:
        # clean_title = title.split('#')[0].strip()  # Take part before #
        # clean_title = remove_emoji(clean_title)
        # clean_title = re.sub(r'@\S+', '', clean_title)
        clean_title = re.sub(r'\d+[\.\d+]*[KMB]*', '', title)   # Remove emojis
        cleaned_titles.append(clean_title)


    return cleaned_titles





def sanitize_folder_name(name):
    """Sanitize the folder name to remove or replace invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def fuzzy_match(description, titles):
    """Fuzzy match the description with the list of titles."""
    best_match = None
    highest_ratio = 0
    for title in titles:
        ratio = fuzz.ratio(description, title)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = title
    return best_match, highest_ratio

def organize_videos(foldername, playlist_foldername, titles):
    """Organize videos based on fuzzy matching of descriptions with titles."""
    print(foldername)

    if not os.path.exists(os.path.join(playlist_foldername,"playlist")):
        os.makedirs(os.path.join(playlist_foldername,"playlist"))

    for root, dirs, files in os.walk(foldername):
        for fl in files:
            if fl.endswith(".description"):
                description_path = os.path.join(root, fl)

                with open(description_path, "r", encoding="utf-8") as desc_file:
                    description = desc_file.read().strip()
                print(description)
                best_match, ratio = fuzzy_match(description, titles)
                if ratio > 80:  # Adjust the ratio threshold as needed

                    sanitized_folder_name = sanitize_folder_name(best_match.replace(" ", "_")).rstrip("_")
                    sanitized_folder_name = sanitized_folder_name.split('#')[0].strip()  # Take part before #
                    sanitized_folder_name = remove_emoji(sanitized_folder_name)
                    sanitized_folder_name = re.sub(r'@\S+', '', sanitized_folder_name)
                    sanitized_folder_name = sanitized_folder_name.rstrip("_.")
                    new_folder_name = os.path.join(playlist_foldername, "playlist", sanitized_folder_name)
                    if not os.path.exists(new_folder_name):
                        os.makedirs(new_folder_name)
                    shutil.copytree(root, new_folder_name, dirs_exist_ok=True)
                    break  # Stop after the first match to avoid multiple copies

def main():
    while True:
        window = my_gui()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Quit'):
            window.close()
            break
        foldername = values.get("foldername")
        playlist_foldername = values.get("out_foldername")
        url = values.get("url")

        if not foldername or not url or not playlist_foldername:
            sg.Print("No folder or link provided")
        elif not is_valid_url(url):
            sg.Print("Invalid URL provided")
        else:
            try:
                sg.Print('Collecting titles from ', url)
                soup = get_page_source(url)
                print(soup.text)
                titles = parse_soup(soup)
                sg.Print("Found titles:", titles)
                sg.Print("Organizing videos based on titles...")
                organize_videos(foldername, playlist_foldername, titles)
                sg.Print("Done.")
            except Exception as e:
                sg.Print(f"An error occurred: {e}")
        window.close()

if __name__ == '__main__':
    main()
