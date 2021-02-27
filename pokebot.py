# API keys not added. @PokemonRaidBot on Twitter

import praw, tweepy, datetime, math, logging, time, pandas, os
from os import environ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, since_id, all_names):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    Flag = True
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        for poke in all_names:
            for value in poke:
                if value.lower() in tweet.text.lower():
                    logger.info("Valid Pokemon found - sending")
                    user = api.get_user(tweet.user.id)
                    api.update_status(
                        status=most_recent(value.lower(), user.screen_name),
                        in_reply_to_status_id=tweet.id,
                        exclude_reply_user_ids=1357865981155098624
                    )
                    Flag = False
                    break
            if Flag is False:
                break
        break

    if Flag is True:
        logger.info("Invalid entry")
        return since_id
    else:
        return new_since_id


def most_recent(name, user):
    reddit = praw.Reddit(
        client_id=environ["API_ID"],
        client_secret=environ["API_SECRET"],
        user_agent="<twitter>:<pokeraidapp>:<1.01> (by u/<ming0_>)"
    )

    Flag = True
    subreddit = reddit.subreddit("pokemongoraids")
    for submission in subreddit.new(limit=10):
        return_string = "%s\n" % submission.url
        if name in submission.title.lower():
            difference = datetime.datetime.now().timestamp() - submission.created_utc
            if difference > 216000:
                return_string += "@%s Most recent %s raid found over 1 hour ago." % (user, name.upper())
            elif difference > 60:
                return_string += "@%s Most recent %s raid found %d minutes ago." % (user, name.upper(), math.floor(difference / 60))
            else:
                return_string += "@%s Most recent %s raid found %d seconds ago." % (user, name.upper(), math.floor(difference / 60))
            Flag = True
            break
        else:
            Flag = False
    if Flag is False:
        return_string = ""
        return_string = "@%s New raid not found for %s. :( Try again later." % (user, name.upper())
        
    return return_string


def main():
    auth = tweepy.OAuthHandler(environ["API_KEY"],
                               environ["API_KEY_SECRET"])
    auth.set_access_token(environ["ACCESS_TOKEN"],
                          environ["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    df = pandas.read_csv('pokemon.csv')
    all_pokemon = df.values.tolist()

    since_id = 1
    while True:
        try:
            api.verify_credentials()

            since_id = check_mentions(api, since_id, all_pokemon)

            logger.info("Waiting...")
            time.sleep(10)
        except tweepy.TweepError as e:
            if "Status is a duplicate" in str(e):
                pass
            else:
                print("ERROR CODE: ", str(e))
            time.sleep(10)


if __name__ == "__main__":
    main()
