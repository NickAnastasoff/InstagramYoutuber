import datetime
import requests
from instagrapi import Client
from constants import memePages, IG_USERNAME, IG_PASSWORD

def get_following(username, password):
    cl = Client()
    cl.login(username, password)
    return cl.user_following()

def download_media(media_url, filename):
    response = requests.get(media_url)
    with open(filename, "wb") as file:
        file.write(response.content)

def scrapeVideos(username = "",
                 password = "",
                 output_folder = "",
                 days = 1,
                 accounts = []):
    cl = Client()
    cl.login(username, password)
    user_id = cl.user_id_from_username(IG_USERNAME)
    followers = cl.user_followers(user_id, 37)
    usernames = []
    for follower_id in followers.keys():
        follower_username = followers[follower_id].username
        usernames.append(follower_username)



    print(usernames)

    for account in usernames:
        user_id = cl.user_id_from_username(account)
        medias = cl.user_medias(user_id, 1)

        if medias:
            media = medias[0]
            if media.media_type == 2:  # Video media type
                # Download the video
                video_filename = f"{output_folder}/{account}_media.mp4"
                download_media(media.video_url, video_filename)

if __name__ == "__main__":
    scrapeVideos(username = IG_USERNAME,
                 password = IG_PASSWORD,
                 output_folder = "Memes",
                 accounts = memePages)