# autogram
Automates uploading top post of a subreddit to an instagram page.

## Overview
This Python script automates the process of fetching top posts from a specific subreddit (in this case, 'memes') and posting them to Instagram. The script is designed to run once a day, downloading a top post and uploading it to an Instagram account.

## Features
- **Automated Scheduling:** Runs daily at a specified time using GitHub Actions.
- **Image Handling:** Downloads images from Reddit and handles image storage temporarily in the GitHub repository.
- **Instagram Integration:** Automatically uploads the image to a specified Instagram account.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- A GitHub account.
- A Reddit account with API access.
- An Instagram account.
- Python installed on your machine (preferably Python 3.11).

## Installation and Setup
1. **Clone the Repository:**
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. **Configure Environment Variables:**
Set up the following environment variables in your GitHub repository settings under 'Secrets':
- `REDDIT_CLIENT_ID`: Your Reddit API client ID.
- `REDDIT_CLIENT_SECRET`: Your Reddit API client secret.
- `INSTA_USERNAME`: Your Instagram username.
- `INSTA_PASSWORD`: Your Instagram password.

3. **GitHub Actions Workflow:**
Edit the `.github/workflows/main.yml` file to customize the schedule or Python version.

## Usage
The script is executed automatically according to the schedule set in the GitHub Actions workflow. You can modify the script or the workflow file for different subreddits, schedules, or Instagram accounts.

## Local Development
To run the script locally for development or testing:
1. Create a `.env` file in the root directory and add the necessary environment variables.
2. Install dependencies:
pip install praw requests instagrapi
3. Run the script:
python your_script.py

## Contributing
Contributions to this project are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your_feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your_feature`).
6. Open a pull request.
