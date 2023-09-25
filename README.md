# Spotify-to-mp3
### About: 
It downloads all your songs from your playlist into MP3 format in a folder, using the Spotify API.
<br/>
### Requirements: 
- **Python**  (latest version)
- **Browser** 
- **Spotify Developer Account** 
### Steps:
- Create a Spotify developer account.
- Create an **App**. (For now write any **random** link for **URI**)
- After that Download the GitHub Repo.
- Locate it in **Vscode**.
- Open 3 terminals/cmd (recommended to do in VS Code, you won't be actively using 2 of them)
- On the First one Type:
    - `python server.py`
    - You can change the port to anything you want in the **server.py** file
- On the second Terminal/cmd Type:
    - `./ngrok http 8888`
    - 8888 is the default, **change it if you have changed it in the file**
- After that take the link given by **ngrok** and **replace** that random URI that you wrote in the developer App with that link **+ /callback** at the end of the link.
    - E.g ngroklink.com/callback
- After saving take note of:
    - **Client ID**
    - **Client Secret ID**
    - **The ngrok link +/callback**
    - You need this info because when you start **main.py** it will ask for this info.
- After taking note of all the info, in the third terminal/cmd Type:
    - `python main.py`
- The program will ask for all the info and save it, and then it will ask which link were you directed to. That link is the one you would be at **after** authenticating with Spotify, it will contain your token. **Copy THE LINK!** (not the token or anything on the page) and paste it onto the terminal/cmd and press enter. After that, it will show you your playlists, and continue as you wish!
- Do note that when running again, you can use your previous credentials, but just to be sure make sure in the credentials text file, you should **add /callback** into the ngrok link if not already there.
### Issues:
- If the developer dashboard doesn't work on your PC, **Try a different device!** For me, I had to use my mobile.
