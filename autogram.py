import praw
import os
import requests
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from datetime import date
import subprocess
import sys

def main(subreddit_name):
    top_posts = redditAPI(subreddit_name)
    for post in top_posts:
        if post.url.endswith('.jpg'):
            extension = '.jpg'
            isDownloaded, image_path = download_image(post.url, extension)
            if isDownloaded:
                upload_to_instagram(image_path)
                break

def redditAPI(subreddit_name):
    reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                         client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                         user_agent='topAPI')
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.top(time_filter='day', limit=20)

def download_image(url, extension):
    response = requests.get(url)
    if response.status_code == 200:
        image_name = get_image_name()
        image_path = f'./images/{image_name}{extension}'
        with open(image_path, 'wb') as file:
            file.write(response.content)
        increment_image_name()
        return True, image_path
    return False, None

def upload_to_instagram(image_path):
    insta = Client()
    insta.login(os.environ.get('INSTA_USERNAME'), os.environ.get('INSTA_PASSWORD'))

    print("Handling challenge..")
    if insta.last_json.get('challenge'):
        insta.challenge_resolve_auto()
    print("Challenge handled.")
    caption = str(date.today())

    print("Uploading..")
    insta.photo_upload(image_path, caption)
    print("Good to go.")

def get_image_name():
    with open(f'./image_counter.txt', 'r') as file:
        number = int(file.read().strip())
    return f'image_{number}'

def increment_image_name():
    with open(f'./image_counter.txt', 'r') as file:
        number = int(file.read().strip())
    with open(f'./image_counter.txt', 'w') as file:
        file.write(str(number + 1))

def commit_and_push(filename):
    subprocess.run(['git', 'add', f'./images/{filename}'])
    subprocess.run(['git', 'commit', '-m', f'Add image {filename}'])
    subprocess.run(['git', 'push'])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please specify a subreddit name.")
        sys.exit(1)
    subreddit_name = sys.argv[1]
    main(subreddit_name)
