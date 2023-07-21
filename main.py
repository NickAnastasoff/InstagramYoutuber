from scrape_videos import scrapeVideos
from make_compilation import makeCompilation
from youtube import upload
import time
import datetime
import os
import shutil
import googleapiclient.errors
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from constants import IG_USERNAME, IG_PASSWORD

print("user and pass:")
print(IG_USERNAME)
print(IG_PASSWORD)
title = "TRY NOT TO LAUGH"
now = datetime.datetime.now()
videoDirectory = "Memes"
outputFile = "./" + str(now.month) + "_" + str(now.year) + "_v" + str(now.day) + ".mp4"

INTRO_VID = '' # SET AS '' IF YOU DONT HAVE ONE
OUTRO_VID = ''
TOTAL_VID_LENGTH = 13*60
MAX_CLIP_LENGTH = 19
MIN_CLIP_LENGTH = 5
DAILY_SCHEDULED_TIME = "20:00"
TOKEN_NAME = "token.json" # Don't change

def routine():

    description = ""
    print(outputFile)

    if not os.path.exists(videoDirectory):
        os.makedirs(videoDirectory)
    
    # Step 1: Scrape Videos
    print("Scraping Videos...")
    scrapeVideos(username = IG_USERNAME,
                 password = IG_PASSWORD,
                 output_folder = videoDirectory,
                  days=1)
    print("Scraped Videos!")
    
    description = "Enjoy the memes! :) \n\n" \
    f"like and subscribe to @{IG_USERNAME} for more \n\n" \

    # Step 2: Make Compilation
    print("Making Compilation...")
    makeCompilation(path = videoDirectory,
                    introName = INTRO_VID,
                    outroName = OUTRO_VID,
                    totalVidLength = TOTAL_VID_LENGTH,
                    maxClipLength = MAX_CLIP_LENGTH,
                    minClipLength = MIN_CLIP_LENGTH,
                    outputFile = outputFile)
    print("Made Compilation!")
    
    description += "\n\nCopyright Disclaimer, Under Section 107 of the Copyright Act 1976, allowance is made for 'fair use' for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.\n\n"
    description += "#memes #dankmemes #compilation #funny #funnyvideos \n\n"

    # Step 3: Upload to Youtube
    print("Uploading to Youtube...")
    upload(outputFile,
                title,
                description)
    print("Uploaded To Youtube!")
    
    # Step 4: Cleanup
    print("Removing temp files!")
    # Delete all files made:
    #   Folder videoDirectory
    shutil.rmtree(videoDirectory, ignore_errors=True)
    #   File outputFile
    try:
        os.remove(outputFile)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
    print("Removed temp files!")

def attemptRoutine():
    while(1):
        try:
            routine()
            break
        except OSError as err:
            print("Routine Failed on " + "OS error: {0}".format(err))
            time.sleep(60*60)

attemptRoutine()