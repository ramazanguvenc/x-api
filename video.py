import requests
import re
import json

def get_x_auth_token(bearer):

    # URL for getting the guest token
    url = "https://api.twitter.com/1.1/guest/activate.json"

    # Headers for the request
    headers = {
        "Authorization": bearer
    }

    # Make the POST request
    response = requests.post(url, headers=headers)

    # Parse the JSON response and extract the guest token
    guest_token = response.json().get('guest_token')
    return guest_token



def get_max_bitrate_video_url(json_data):
    # Extract the media section from the JSON data
    try:
        media_items = json_data['data']['tweetResult']['result']['legacy']['extended_entities']['media']
    except KeyError:
        raise ValueError("Unexpected JSON structure: 'media' key not found")

    max_bitrate = 0
    best_video_url = None

    # Loop through all media items to find the one with the highest bit rate
    for media in media_items:
        if media.get('type') == 'video':
            video_variants = media.get('video_info', {}).get('variants', [])
            for variant in video_variants:
                bitrate = variant.get('bitrate', 0)
                if bitrate > max_bitrate:
                    max_bitrate = bitrate
                    best_video_url = variant.get('url')

    if best_video_url:
        return best_video_url
    else:
        raise ValueError("No video with bitrate found")


def read_json_from_file(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


# Function to extract tweetId from URL
def extract_tweet_id(url):
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid URL format. Unable to extract tweetId.")

def get_video_link(url_input):
    url = 'https://api.x.com/graphql/sCU6ckfHY0CyJ4HFjPhjtg/TweetResultByRestId'

    tweetId = extract_tweet_id(url_input)

    with open('jsons/params.json', 'r') as file:
        params = json.load(file)

    params['variables'] = params['variables'].replace("TWEET_ID", tweetId)

    with open('jsons/headers.json', 'r') as file:
        headers = json.load(file)



    # Send the request
    response = requests.get(url, params=params, headers=headers)

    # Print the response
    if response.status_code == 403:
        guest_token = get_x_auth_token(headers['authorization'])
        headers['x-guest-token'] = guest_token
        with open('jsons/headers.json', 'w') as file:
            json.dump(headers, file, indent=4)
        response = requests.get(url, params=params, headers=headers)
        

    if response.status_code == 200:
        return get_max_bitrate_video_url(json.loads(response.text))
    else:
        response.raise_for_status()