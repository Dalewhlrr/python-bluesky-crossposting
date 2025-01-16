This script automates the process of crossposting from Bluesky to other platforms such as Threads and Twitter. It runs as a cron job every 30 minutes, ensuring your text-based posts on Bluesky are shared seamlessly.

Prerequisites
API Keys
Threads: Obtain an API key from Threads.
Twitter: Obtain an API key, along with access tokens and secrets from Twitter Developer Platform.
Bluesky
No API key is required for Bluesky.
Features
Automatically crossposts from Bluesky to Threads and Twitter.
Runs as a cron job every 30 minutes.
Currently supports text-only posts (media is not yet supported).
Installation
Clone this repository:


git clone <repository_url>
cd <repository_folder>
Install the required dependencies:


pip install -r requirements.txt
Set up your configuration file:

Create a config.yaml file with your API keys and credentials. Follow the structure in the script comments for guidance.
How It Works
The script checks Bluesky for new posts.
Posts created within the last 30 minutes are identified.
Text-based posts are crossposted to:
Threads: Using Threads' API.
Twitter: Using the Twitter API.
Limitations
Media support: Currently, the script does not handle images, videos, or other media types. Only text posts are supported.
Scheduling
To run this script automatically, set up a cron job:

Open the crontab editor:

crontab -e
Add the following line to schedule the script every 30 minutes:


*/30 * * * * python3 /path/to/script.py
Save and exit the editor.
