import sys
from video import get_video_link
from download import download_video_series

def main():
    if len(sys.argv) > 1:
        tweet_url = sys.argv[1]
    else:
        tweet_url = input("Please enter the tweet URL: ")

    if len(sys.argv) > 2:
        save_path = sys.argv[2]
    else:
        save_path = '.'

    video_link = get_video_link(tweet_url)
    print(video_link)
    download_video_series(video_link, save_path)
    

if __name__ == "__main__":
    main()
