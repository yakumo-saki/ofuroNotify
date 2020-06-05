import slackweb
from mastodon import Mastodon

def slack_post(message, webhook):
    print(f'slack post msg {message} webhook url {webhook}')
    slack = slackweb.Slack(url=webhook)
    slack.notify(text=message)
    print('slack done')


def twitter_post(message, webhook):
    print(f'This is not working: twitter post msg {message} webhook url {webhook}')


def mastodon_post(message, url, token):
    print(f'mastodon post msg {message} webhook url {url} token {token}')
    mastodon = Mastodon(access_token = token, api_base_url = url)
    mastodon.toot(message + " 👁️")
    print('mastodon done')
