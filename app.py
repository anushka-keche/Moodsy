from dotenv import load_dotenv
load_dotenv()
import os

import spotipy

from flask import Flask, render_template, redirect, request, session
from spotipy.oauth2 import SpotifyOAuth

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 🔐 Spotify Credentials (PUT YOURS HERE)
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-read-private user-read-email"

sp_oauth = SpotifyOAuth(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    scope=SCOPE,
    cache_path=None,
    show_dialog=True
)

# 🎧 Login Route
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")

        session["username"] = name
        session["email"] = email

        return redirect("/home")

    return render_template("login.html")


# 🏠 Home Page
@app.route("/home")
def home():

    name = session.get("username","User")

    # ✅ ADD THIS PART (GREETING LOGIC)
    import datetime
    hour = datetime.datetime.now().hour

    if hour < 12:
        greeting = "Good Morning ☀️"
    elif hour < 18:
        greeting = "Good Afternoon 🌤️"
    else:
        greeting = "Good Evening 🌙"

    # ✅ PASS greeting to HTML
    return render_template("index.html", username=name, greeting=greeting)

# 🎵 Mood → Spotify Playlist Redirect
@app.route("/create_playlist/<mood>")
def create_playlist(mood):

    mood_dict = {
        "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
        "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
        "chill": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
        "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYxwmBaMqxsl",
        "party": "https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif",
        "romantic": "https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn"
    }

    playlist_url = mood_dict.get(mood.lower())

    if not playlist_url:
        return redirect("/home")

    return redirect(playlist_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", msg="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", msg="Something went wrong"), 500

# 🚀 Run App
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)