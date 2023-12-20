import praw
import os
import requests
from instagrapi import Client
from datetime import date
import subprocess
import sys
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(subreddit_name):
    logging.info(f"Starting script for subreddit: {subreddit_name}")
    top_posts = redditAPI(subreddit_name)
    if(top_posts == None):
        logging.info("No posts returned.")
    else:
        logging.info(top_posts)
    for post in top_posts:
        if post.url.endswith('.jpg'):
            extension = '.jpg'
            isDownloaded, image_path = download_image(post.url, extension)
            if isDownloaded:
                upload_to_instagram(image_path)
                logging.info("Script completed successfully.")
                break

def redditAPI(subreddit_name):
    logging.info(f"Accessing Reddit API for subreddit: {subreddit_name}")
    try:
        reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                             client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                             user_agent='topAPI')
        subreddit = reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(time_filter='day', limit=20)
        logging.info("Reddit API accessed successfully.")
        return top_posts
    except Exception as e:
        logging.error(f"Error accessing Reddit API: {e}")
        return []

def download_image(url, extension):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = get_image_name()
            image_path = f'./images/{image_name}{extension}'
            with open(image_path, 'wb') as file:
                file.write(response.content)
            increment_image_name()
            logging.info(f"Image downloaded successfully: {image_path}")
            return True, image_path
        else:
            logging.error(f"Failed to download image. Status code: {response.status_code}")
            return False, None
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return False, None

def upload_to_instagram(image_path):
    try:
        insta = Client()
        insta.login(os.environ.get('INSTA_USERNAME'), os.environ.get('INSTA_PASSWORD'))

        # Handle challenge if required
        if insta.last_json.get('challenge'):
            insta.challenge_resolve_auto()

        caption = str(date.today())
        insta.photo_upload(image_path, caption)
        logging.info(f"Image uploaded to Instagram successfully: {image_path}")
    except Exception as e:
        logging.error(f"Error uploading to Instagram: {e}")

def get_image_name():
    try:
        with open(f'./image_counter.txt', 'r') as file:
            number = int(file.read().strip())
        return f'image_{number}'
    except Exception as e:
        logging.error(f"Error getting image name: {e}")
        return "default_image"

def increment_image_name():
    try:
        with open(f'./image_counter.txt', 'r') as file:
            number = int(file.read().strip())
        with open(f'./image_counter.txt', 'w') as file:
            file.write(str(number + 1))
        logging.info("Image name incremented successfully.")
    except Exception as e:
        logging.error(f"Error incrementing image name: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Please specify a subreddit name.")
        sys.exit(1)
    subreddit_name = sys.argv[1]
    main(subreddit_name)
