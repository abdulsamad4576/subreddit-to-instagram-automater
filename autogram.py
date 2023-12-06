import praw
import os
import requests
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from datetime import date
import subprocess

def main():
    top_posts = redditAPI()
    for post in top_posts:
        if post.url.endswith('.jpg') or post.url.endswith('.png'):
            extension = '.jpg' if post.url.endswith('.jpg') else '.png'
            isDownloaded, image_path = download_image(post.url, extension)
            if isDownloaded:
                upload_to_instagram(image_path)
                break

def redditAPI():
    reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                         client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                         user_agent='topAPI')
    subreddit = reddit.subreddit('memes')
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

    # Handle challenge if required
    if insta.last_json.get('challenge'):
        insta.challenge_resolve_auto()

    caption = str(date.today())
    insta.photo_upload(image_path, caption)

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
    main()
