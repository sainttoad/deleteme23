import os
import sys
import time
import twitter
import datetime

consumer_key        = 'ueIHhQOMuYdQ2jgbWNJ0nllpQ'
access_token_key    = '85117657-Lpfqzxr0H6jyk83zm5S2ChfBcpwdmIPvqtOPP1bO0'
username            = os.environ['TWITTER_USERNAME']

with open("/secrets") as f:
    consumer_secret, access_token_secret = map(str.strip, f.read().split("\n"))

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

with open("./deleted.txt") as f:
    deleted_ids = [ int(line) for line in f.read().split("\n") if len(line) ]

def add_to_deleted(id):
    with open("./deleted.txt", "a") as f:
        f.write("{}\n".format(id))

def delete_via_archive():
    for root, dirs, files in os.walk('/tweets/data/js/tweets'):
        for file in files:
            with open(os.path.join(root, file)) as f:
                for line in f:
                    if line.startswith('  "id" :'):
                        the_id = int(line.split(':')[1].split(',')[0])
                        if not the_id in deleted_ids:
                            print(the_id)
                            try:
                                api.DestroyStatus(the_id)
                                add_to_deleted(the_id)
                                time.sleep(.025)
                            except twitter.error.TwitterError as e:
                                if e.message[0]['code'] == 144:
                                    add_to_deleted(the_id)
                                else:
                                    print("{} : {}".format(e.__class__, e))

def delete_recent():
    last_id = None

    while True:
        statuses = api.GetUserTimeline(screen_name=username, count=200, max_id=last_id)
        if statuses:
            last_id = statuses[-1].id - 1
        else:
            break

        for s in statuses:
            # Fri Feb 15 06:30:50 +0000 2019
            created_at = datetime.datetime.strptime(s.created_at, "%a %b %d %H:%M:%S %z %Y")
            diff = datetime.datetime.now(tz=datetime.timezone.utc) - created_at
            if diff.days > 0 or diff.seconds / 60 /60 > 23:
                print("{} : {} : {} : {}".format(s.id, s.created_at, s.retweeted, s.retweeted_status.user.screen_name if s.retweeted else ''))
                api.DestroyStatus(s.id)

        print("-------")

        time.sleep(1)

def delete_favorites():
    last_id = None

    while True:
        favorites = api.GetFavorites(screen_name=username, count=200, max_id=last_id)
        if favorites:
            last_id = favorites[-1].id - 1
        else:
            break

        for f in favorites:
            print("{} : {}".format(f.id, f.created_at))
            try:
                api.DestroyFavorite(status_id=f.id)
            except twitter.error.TwitterError as e:
                if e.message[0]['code'] == 144:
                    pass
                else:
                    print("{} : {}".format(e.__class__, e))




if __name__ == "__main__":
    delete_recent()
    # delete_favorites()
    # delete_via_archive()
