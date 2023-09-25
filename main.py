import os
import spotipy
import pytube
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pytube import YouTube
from pathlib import Path


# Function to save or load Spotify credentials from a file
def save_or_load_spotify_credentials():
    file_path = "spotify_credentials.txt"

    if os.path.exists(file_path):
        use_saved = input("Do you want to use saved Spotify credentials? (yes/no): ").lower()
        if use_saved == "yes":
            with open(file_path, 'r') as file:
                lines = file.readlines()
                return lines[0].strip(), lines[1].strip(), lines[2].strip()
    
    client_id = input("What is your client ID: ")
    client_secret = input("What is your client Secret ID: ")
    redirect_uri = input("Write your Ngrok link: ") + "/callback"
    
    with open(file_path, 'w') as file:
        file.write(f"{client_id}\n{client_secret}\n{redirect_uri}")

    return client_id, client_secret, redirect_uri

# Initialize Spotipy client
SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI = save_or_load_spotify_credentials()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read"))

# Function to search for a YouTube link for a given song title
def search_youtube_link(song_title):
    query = song_title
    url = f"https://www.youtube.com/results?search_query={'+'.join(query.split())}"

    # Set up Chrome options to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode, no browser UI

    driver = webdriver.Chrome(options=chrome_options)  # Initialize headless WebDriver
    driver.implicitly_wait(5)  # Implicit wait for 5 seconds
    driver.get(url)  # Navigate to YouTube search results

    # Retrieve the YouTube Link
    link = []
    select = driver.find_element(By.CSS_SELECTOR, 'div#contents ytd-item-section-renderer>div#contents a#thumbnail')
    link += [select.get_attribute('href')]

    # Close the WebDriver
    driver.quit()

    if link:
        return link[0]
    else:
        return None

# Function to convert a YouTube video to mp3
def youtube2mp3(url, outdir):
    try:
        # url input from user
        yt = YouTube(url)

        # Extract audio with 160kbps quality from video
        video = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        # Download the file
        out_file = video.download(output_path=outdir)
        base, ext = os.path.splitext(out_file)
        new_file = Path(f'{base}.mp3')
        os.rename(out_file, new_file)

        # Check success of download
        if new_file.exists():
            print(f'{yt.title} has been successfully downloaded.')
        else:
            print(f'ERROR: {yt.title} could not be downloaded!')
    except pytube.exceptions.VideoUnavailable:
        print("The video is unavailable for download.")

# Function to get user playlists and download their songs
def get_my_playlists():
    playlists = sp.current_user_playlists()
    if 'items' not in playlists:
        print("Error: Unable to retrieve playlists.")
        return []

    print("\nThese are your Playlists:")
    for idx, playlist in enumerate(playlists['items'], start=1):
        print(f"{idx}. {playlist['name']}")

    show_urls = input("Do you want to see all the URLs for the songs which are going to be downloaded? (yes/no): ").strip().lower()
    show_urls = show_urls == "yes"

    selected_playlist_idx = -1
    while selected_playlist_idx < 0 or selected_playlist_idx >= len(playlists['items']):
        selected_playlist_idx_str = input("\nEnter the number of the playlist you want to download: ")
        if not selected_playlist_idx_str.isdigit():
            print("Please enter a valid number.")
            continue
        selected_playlist_idx = int(selected_playlist_idx_str) - 1

    selected_playlist_id = playlists['items'][selected_playlist_idx]['id']
    playlist_name = playlists['items'][selected_playlist_idx]['name']
    print(f"\nYou selected playlist: {playlist_name}\n")

    # Get the maximum number of songs to search for
    max_songs_to_search = playlists['items'][selected_playlist_idx].get('tracks', {}).get('total', 0)
    print(f"The maximum number of songs you can choose is: {max_songs_to_search}\n")

    num_songs_to_search = -1
    while num_songs_to_search < 0 or num_songs_to_search > max_songs_to_search:
        num_songs_to_search_str = input("Enter the number of songs you want to download: ")
        if not num_songs_to_search_str.isdigit():
            print("Please enter a valid number.")
            continue
        num_songs_to_search = int(num_songs_to_search_str)
        if num_songs_to_search < 0 or num_songs_to_search > max_songs_to_search:
            print(f"Please enter a number between 1 and {max_songs_to_search}.")

    # Retrieve and store all the songs in the selected playlist
    playlist_tracks = sp.playlist_tracks(selected_playlist_id)
    song_list = []

    for idx, track in enumerate(playlist_tracks['items'][:num_songs_to_search], start=1):
        song_info = f"{idx}. {track['track']['name']} by {', '.join([artist['name'] for artist in track['track']['artists']])}"
        youtube_link = search_youtube_link(track['track']['name'])
        if youtube_link:
            song_info += f"\nYouTube Link: {youtube_link}"
            if show_urls:
                print(f"Song {idx} URL: {youtube_link}")

            # Create a folder using the playlist name
            playlist_folder = os.path.join(os.getcwd(), playlist_name)
            if not os.path.exists(playlist_folder):
                os.makedirs(playlist_folder)

            # Download the YouTube video as MP3 to the playlist folder
            youtube2mp3(youtube_link, playlist_folder)

        song_list.append(song_info)

    return song_list

if __name__ == "__main__":
    songs = get_my_playlists()
    for song in songs:
        print(song)
