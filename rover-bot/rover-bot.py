import requests
import random
import logging
import time
from datetime import datetime, date, timedelta
# from mock_response import response_json  # for testing only

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('rover-bot')


def get_photo(rover, date):
    api_key = 'DEMO_KEY'  # keep this a secret, shouldn't be in the public repository
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?&api_key={}&earth_date={}'.format(
        rover, api_key, date)

    # MAKE REQUEST
    logger.info('HTTP GET: {}'.format(url))

    response = requests.get(url)
    if response.status_code != 200:  # check that the API call worked and exit if it didn't
        logger.error(response.text())
        exit(1)
    response_json = response.json()

    return random.choice(response_json['photos'])


# SET VARIABLES
# keep this a secret, shouldn't be in the public repository
fb_access_token = '<paintmin bot access token here>'
rover_names = ['curiosity', 'opportunity', 'spirit']

# date info from https://en.wikipedia.org/wiki/Mars_rover
valid_dates = {
    'spirit': {
        'min': date(2004, 1, 4),
        'max': date(2010, 3, 22),
    },
    'opportunity': {
        'min': date(2004, 1, 25),
        'max': date(2018, 6, 10),
    },
    'curiosity': {
        'min': date(2012, 8, 6),
        # set to "now" as it's still
        'max': date(datetime.now().year, datetime.now().month, datetime.now().day)
    }
}

# BUILD REQUEST

photo = None
while photo is None:
    # choose a rover
    # rover = random.choice(rover_names)
    rover = 'curiosity'  # curiosity has the best images

    # choose a date
    start_date = valid_dates[rover]['min']
    end_date = valid_dates[rover]['max']
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    logger.debug('Searching for image from [{}] taken on [{}]'.format(
        rover, random_date))

    try:
        photo = get_photo(rover, random_date)
        camera_name = photo['camera']['full_name']
        photo_date = photo['earth_date']
        image_url = photo['img_src']
        logger.info('Image URL: {}'.format(image_url))
        img = requests.get(image_url).content
        img_size = len(img)
        if len(img) < 30000:
            logger.info(
                'Image was too small {} bytes, trying again in 10s...'.format(img_size))
            photo = None
            time.sleep(10)
    except IndexError:
        logger.info('No images for search criteria, trying again in 10s...')
        time.sleep(10)

# POST TO FB

message = '{} {}'.format(camera_name, photo_date)
logger.debug(message)

# image = requests.get(img_url).content  # fetch the source image
# NB: if we are using lambda we may need to write out the file
# with open("/tmp/image", 'wb') as f:
#     f.write(requests.get(img_url).content)
#     return True

logger.info('Posting to facebook!')
# post using the facebook graph API python module
# https://facebook-sdk.readthedocs.io/en/latest/api.html
# GraphAPI(access_token=fb_access_token).put_photo(image=image, message=message)  # make fb post
