import requests
import re

def clean_file_name(file_name):
    # Remove any characters that are not alphanumeric, hyphens, or underscores
    return re.sub(r'[^a-zA-Z0-9_-]', '', file_name)


def download_video_series(link, save_path='.'):
    try:
        file_name = clean_file_name(link.split('/')[-1]) + '.mp4'
        print ("Downloading file:%s"%file_name )
        r = requests.get(link, stream = True) 
        if not save_path.endswith('/'):
            save_path += '/'
        path = save_path + file_name
        with open(path, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 
        print ("Saved to %s!\n"%path )
    except Exception as e:
        print(f'Error downloading file {path}: {e}')  
