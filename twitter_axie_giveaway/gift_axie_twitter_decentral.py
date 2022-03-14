import csv

from matplotlib.pyplot import text
import tweepy
import ssl
import config
import logging
import random
import gift_axie_lib as gift
import re
import gift_axie_ocv_lib as decocv
import json
import requests

ssl._create_default_https_context = ssl._create_unverified_context

# Oauth keys
consumer_key = "XXX"
consumer_secret = "XXX"
access_token = "XXX"
access_token_secret = "XXX"

logging.basicConfig(filename=config.GIFT_AXIE_LOGS, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# Authentication with Twitter
client = tweepy.Client(bearer_token = config.BEARER_TOKEN, 
consumer_key = config.API_KEY,
consumer_secret=config.API_KEY_SECRET,
access_token=config.ACCESS_TOKEN,
access_token_secret=config.ACCESS_TOKEN_SECRET)

query = 'from:decentralfarm #Axie #DecentFarmGuild #AxieGiveaway -is:retweet'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at', 'conversation_id', 'referenced_tweets', 'author_id'], max_results=100, expansions=["in_reply_to_user_id","referenced_tweets.id", 'author_id'])
date_giveaway = tweets.data[0].created_at
tweet = tweets.data[0]
print(f"Id is {tweet.id}")
print(tweet)
logging.info(tweet)

print(tweet.conversation_id)
print(tweet.referenced_tweets)
logging.info("replies:")
valid_replies =[]
visited_users = {}
media = {}
specific_conversation_query = f'conversation_id:{tweet.conversation_id} to:decentralfarm ronin'
# specific_conversation_query = f'from:decentraland Join the monthly Town Hall meetups'
for reply in tweepy.Paginator(client.search_recent_tweets, query=specific_conversation_query,
                            tweet_fields=['context_annotations', 'created_at', 'conversation_id', 'referenced_tweets', 'in_reply_to_user_id', 'id', 'author_id'], 
                            expansions=["in_reply_to_user_id","referenced_tweets.id", 'author_id', 'attachments.media_keys'],
                            media_fields =['url','preview_image_url'],
                            max_results=100):
    print(reply.includes)
    print('________________')
    for in_rep in reply.data:

        logging.info(in_rep)
        print(in_rep)
        if visited_users.get(in_rep.author_id, 0) == 0:
            valid_replies.append(in_rep)

    for inc_re in reply.includes['media']:

        logging.info(inc_re)
        print(inc_re.data)
        media[inc_re.media_key] = inc_re.data

print(media)


followers=set()
for user in tweepy.Paginator(client.get_users_followers, id=tweet.author_id, max_results=1000).flatten(limit=10000):
    # print(user.id)
    followers.add(user.id)

likers=set()
for user in tweepy.Paginator(client.get_liking_users, id=tweet.id, max_results=100).flatten(limit=10000):
    # print(user.id)
    likers.add(user.id)

retweeters=set()
for user in tweepy.Paginator(client.get_retweeters, id=tweet.id, max_results=100).flatten(limit=10000):
    # print(user.id)
    retweeters.add(user.id)

def isValid(author_id):
    # print(f"The id is {author_id}")
    return author_id in list(followers & likers & retweeters)

def challenge2(potential_winner):
    if potential_winner.attachments is None:
        return False
    if not 'media_keys' in potential_winner.attachments:
        return False
    for media_key in potential_winner.attachments['media_keys']:
        photo_url = media[media_key]['url']
        print(f'*************{photo_url}*******************')
        reply_img = config.TWEET_IMGS_DIR+media_key
        with open(reply_img, 'wb') as f:
            f.write(requests.get(photo_url).content)
            f.close()
        
        min_distance , max_distance = decocv.compareImages(reply_img, config.DEC_IMGS_DIR)
        logging.info(f"The similarity of the images for {potential_winner.author_id} is between {min_distance} and {max_distance}")
        if min_distance < 0.8:
            return True
    return False

dest_address = ''
desired_axie = None
selected_winner = None
while len(valid_replies)>0:
    selected_winner = random.choice(valid_replies)
    print(f"selected: {json.dumps(selected_winner.data)}")
    
    lst_addr=re.findall(r"\bronin:\w+", selected_winner.text)
    if len(lst_addr) > 0:
        dest_address = lst_addr[0]
    lst_axies=re.findall(r"\baxie\s*=\s*([0-9]+)", selected_winner.text)
    if len(lst_axies) > 0:
        desired_axie = lst_axies[0]

    if gift.validAddr(dest_address) and isValid(selected_winner.author_id) and challenge2(selected_winner):
        print(f"The {dest_address} is valid")
        logging.info(f"The {dest_address} is valid")
        break
    else:
        logging.warning(f"The {dest_address} is NOT valid, removing from list")
        valid_replies.remove(selected_winner)

if len(valid_replies)>0:
    print(dest_address)
    gift_response = ''
    #gift_response = gift.gift(dest_address, desired_axie)
    username=client.get_users(ids=[selected_winner.author_id])
    print(f"username: {username}")
    logging.info(f"Send gift to {selected_winner.author_id}, tweet: {selected_winner.id}  address: {dest_address} check: {gift_response}")
    logging.info(f"The winner is {username.data[0].name}, @{username.data[0].username}, address: {dest_address} check: {gift_response}. Congratulations!!")
else:
    logging.info(f"No winner!!")

# Next giveway
if gift.balance()>0:
    
    # If today is Monday (aka 0 of 6), then run the report
    day = 'Monday'
    print(date_giveaway)
    if date_giveaway.weekday() <= 1:
       day = 'Wednesday' 
    print(f'''
    #DecentFarmGuild is doing an #AxieGiveaway every Monday and Wednesday.

    What? One Random #Axie from: https://marketplace.axieinfinity.com/profile/ronin:90611514365be717021bff8631abf2e4a7addd8e/axie/
    
    When? Next {day}.

    You need to:
    1. Retweet,
    2. Follow,
    3. Like,
    4. Reply with your ronin address.
    ''')
