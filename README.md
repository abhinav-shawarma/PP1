# PP1
Bot for BAS Hackathon

# NASA APIs

Quite a few open APIs available here, some of which include images https://api.nasa.gov/

Generating an API key is easy and instant and the rate limits are more than enough for posting to FB every 30 mins

# Mars Rover bot idea

We could build a bot or some other rover bot using the "Mars Rover Photos" API endpoint.

Example request:
https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY&date=2020-08-08

code will be straightforward, use python requests, pick a random rover and sol

parse the response, pick an image and share on fb with which camera it was taken with and which rover, the date and any other info
