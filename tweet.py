from cicero.twitter import Twitter


def tweet():
    twitter = Twitter()
    if not twitter.bill:
        print("Nothing to tweet")
        return

    post = twitter.publish()
    print(f"Tweeted: https://twitter.com/botcicero/{post.id}")


if __name__ == "__main__":
    tweet()
