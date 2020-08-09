#!/usr/bin/env python3

import json
import requests
import logging
from datetime import date
import facebook

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pic-of-the-day')

key = 'DEMO_KEY' ####PRIVATE KEY
####REMOVE BEFORE COMMITING

access_token = '<thank-you-paintmin>'

def post_to_facebook(image, message):
    graph = facebook.GraphAPI(access_token)
    logger.debug("Posting to facebook.")
    post_id = graph.put_photo(image, message)["post_id"]


def main():
    #Today's date
    day = date.today().strftime('%Y-%m-%d')
    # day = '2020-02-02' #example

    url = f'https://api.nasa.gov/planetary/apod?api_key={key}&hd=True&date={day}'

    logger.debug(f'Getting json response from {url}')

    response = requests.get(url)

    result = response.json()
    # print(result.keys())
    try:
        caption = result['title']
        image_url = result['hdurl']
        description = result['explanation']
    except KeyError:
        logger.error("Invalid parameter.")
        exit(1)
    
    filename = caption.replace(' ', '_') + '.jpg'

    logger.debug('Writing image to local.')

    with open(filename, 'wb') as f:
        f.write(requests.get(image_url).content)
    #Caption including the image description.
    caption = caption + '\n' + description
    
    post_to_facebook(filename, caption)

if __name__ == "__main__":
    main()
