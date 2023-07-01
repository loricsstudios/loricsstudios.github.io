# thx to ChatGPT for the drudgery

# note: each search request for list of videos metadata that can contain at most 50 items incurs 100 units of quota, there is default daily limit of 10000 so for a massive channel with over 5000 videos you won't fit for a single search within the daily quota so do not spam usage of this script or you'll quickly run out

import csv
import logging

from googleapiclient.discovery import build
from os import getenv

log = logging.Logger('default')
log.setLevel(logging.WARN)

api_key = getenv('YOUTUBE_APIKEY')
channel_id = getenv('CHANNEL_ID')

youtube = build('youtube', 'v3', developerKey=api_key)



request = youtube.search().list( part='snippet', channelId=channel_id, maxResults=50 )
response = request.execute()

# cap here set at processing 500 = 10 * 50 videos, which consumes 1000 API quota usage
max_requests = 10 
request_number = 0 
response_items = []
while (response is not None and request_number<=max_requests): 
    request_number += 1
    response_items.append(response['items'])
    response = request.execute()

csv_file = '_data/data.csv'
log.info(f'writing to csv file: {csv_file}')

rows = []
for video in response_items:
    if video['id']['kind'] != 'youtube#video': continue
    title = video['snippet']['title'].replace(',',';')
    url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
    description = video['snippet']['description'].replace(',',';')
    id = video['id']['videoId']
    published_at = video['snippet']['publishedAt']
    default_thumbnail_url = video['snippet']['thumbnails']['default']['url']
    rows += [(id, title, description, published_at, default_thumbnail_url )]

with open(csv_file, 'w', newline='') as file_handle:
    output = csv.writer(file_handle)
    # default thumbnail is 120x90
    output.writerow(('id','title','description','published_at', 'd_thumbnail'))

    for row in rows:
        log.info(f'Writing row: {row} ..')
        output.writerow( row )
    

