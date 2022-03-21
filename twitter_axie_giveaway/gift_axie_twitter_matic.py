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
import gift_matic_lib as gift_mat

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
            visited_users[in_rep.author_id] = 1
            valid_replies.append(in_rep)
    if 'media' in reply.includes:
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

dest_address = ''
desired_axie = None
paid_replies =[]
dest_addr_dict = {}
desire_axie_dict = {}

for potential_winner  in valid_replies:
    
    print(f"selected: {json.dumps(potential_winner.data)}")
    
    lst_addr=re.findall(r"\bronin:\w+", potential_winner.text)
    if len(lst_addr) > 0:
        dest_address = lst_addr[0]
    lst_axies=re.findall(r"\baxie\s*=\s*([0-9]+)", potential_winner.text, re.IGNORECASE)
    if len(lst_axies) > 0:
        desired_axie = lst_axies[0]
    lst_polygon=re.findall(r"\bpolygon\s*=\s*(\w+)", potential_winner.text, re.IGNORECASE)
    polygon_address = None
    if len(lst_polygon) > 0:
        polygon_address = lst_polygon[0]

    if gift.validAddr(dest_address) and isValid(potential_winner.author_id) and gift_mat.validAddr(polygon_address):
        print(f"The {dest_address} is valid")
        logging.info(f"The {potential_winner.author_id} has {dest_address} and polygon={polygon_address} are valid")
        gift_mat_response = ''
        gift_mat_response = gift_mat.gift(polygon_address, 0.01)
        logging.info(f"Send MATIC to {potential_winner.author_id}, tweet: {potential_winner.id}  address: {polygon_address} check: {gift_mat_response}")
        paid_replies.append(potential_winner)
        desire_axie_dict[potential_winner.author_id] = dest_address
        desire_axie_dict[potential_winner.author_id] = desired_axie
    else:
        logging.warning(f"The {dest_address} is NOT valid, removing from list")

if len(paid_replies)>0:
    winner = random.choice(paid_replies)
    win_addr = dest_addr_dict.get(winner.author_id)
    print(win_addr)
    des_axie = desire_axie_dict.get(winner.author_id)
    gift_response = ''
    gift_response = gift.gift(win_addr, des_axie)
    username=client.get_users(ids=[winner.author_id])
    print(f"username: {username}")
    logging.info(f"Send gift to {winner.author_id}, tweet: {winner.id}  address: {win_addr} check: {gift_response}")
    logging.info(f"The winner is {username.data[0].name}, @{username.data[0].username}, address: {win_addr} check: {gift_response}. Congratulations!!")
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
