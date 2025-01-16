import yaml
import tweepy
import requests
from atproto import Client
from datetime import datetime, timedelta
from pytz import timezone
from dateutil import parser

# Load credentials from config.yaml
with open(r"testcrossposting\config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Twitter API credentials
twitter_config = config["twitter"]
consumer_key = twitter_config["consumer_key"]
consumer_secret = twitter_config["consumer_secret"]
access_token = twitter_config["access_token"]
access_token_secret = twitter_config["access_token_secret"]

# Threads credentials
threads_config = config["threads"]
access_token_ = threads_config["access_token"]
threads_user_id = threads_config["user_id"]

# Bluesky credentials
bluesky_config = config["bluesky"]
bluesky_username = bluesky_config["username"]
bluesky_password = bluesky_config["password"]

def compose_threads_post(post_text):
    """
    Compose a text post for Threads, using the two-step process to create and publish a post.
    """
    # Step 1: Create the Threads Media Container with text only
    url_create = f"https://graph.threads.net/v1.0/{threads_user_id}/threads"
    
    payload = {
        "media_type": "TEXT",
        "text": post_text,
        "access_token": access_token_
    }

    response_create = requests.post(url_create, data=payload)

    if response_create.status_code == 200:
        # Step 1 success, extract the container ID
        media_container_id = response_create.json()["id"]
        print(f"Media Container Created. ID: {media_container_id}")

        # Step 2: Publish the Threads Media Container
        url_publish = f"https://graph.threads.net/v1.0/{threads_user_id}/threads_publish"

        payload_publish = {
            "creation_id": media_container_id,
            "access_token": access_token_
        }

        response_publish = requests.post(url_publish, data=payload_publish)

        if response_publish.status_code == 200:
            print(f"Post Published Successfully: {response_publish.json()}")
        else:
            print("Failed to Publish Post. Error:", response_publish.json())
    else:
        print("Failed to Create Media Container. Error:", response_create.json())

def compose_tweet(tweet):
    # Authenticate
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Create a tweet
    text = tweet
    client.create_tweet(text=text)
    print(f"Tweet posted: {text}")

def main():
    # Login to Bluesky using the atproto client
    client = Client()
    client.login(bluesky_username, bluesky_password)  # Use Bluesky credentials from the YAML file
    profile_feed = client.get_author_feed(actor=bluesky_username, filter='posts_no_replies')

    # Set time zone to Eastern Standard Time
    est = timezone('US/Eastern')
    now = datetime.now(est)  # Current time in EST
    five_minutes_ago = now - timedelta(minutes=30)  # 5 minutes ago

    # Filter posts created within the last 30 minutes
    recent_posts = [
        post for post in profile_feed.feed
        if parser.isoparse(post.post.record.created_at).astimezone(est) >= five_minutes_ago
    ]

    if recent_posts:
        print("Posts in the last 30 minutes:")
        for post in recent_posts:
            post_text = post.post.record.text
            print('-', post_text)

            # Check if the post ends with `..`
            if post_text.strip().endswith('..'):
                print("Post ends with '..'. Skipping posting to other platforms.")
                continue  # Skip this post
            
            # Post the tweet with the text of the most recent post
            compose_tweet(post_text)
            compose_threads_post(post_text)

    else:
        print("No posts in the last 30 minutes.")

if __name__ == '__main__':
    main()
