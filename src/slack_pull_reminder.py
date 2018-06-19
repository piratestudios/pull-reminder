from github3 import login
import os
import requests
import sys

ignore = os.environ.get('GITHUB_IGNORE_WORDS')
GITHUB_IGNORE_WORDS = ignore.split(',') if ignore else []
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#general')

try:
    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']
    GITHUB_ORGANIZATION = os.environ['GITHUB_ORGANIZATION']
except KeyError as error:
    sys.stderr.write('Please set the environment variable {0}'.format(error))
    sys.exit(1)


def is_ignored(title):
    lowercase_title = title.lower()
    for ignored_word in GITHUB_IGNORE_WORDS:
        if ignored_word.lower() in lowercase_title:
            return True

    return False


def format_pull_request(pull_request, repository):
    assignees = []
    for assignee in pull_request.assignees:
        # For some reason access to 'login' fails for some assignees
        try:
            assignees.append(assignee['login'])
        except AttributeError as attribute_error:
            print(attribute_error)
            print(assignee)

    assignee_text = ', '.join(assignees) if assignees else "no one"
    creator = pull_request.user.login

    return f"<{pull_request.html_url}|{repository}/{pull_request.title}> - by {creator} - assigned to *{assignee_text}*"


def fetch_open_pull_requests(organization_name):
    client = login(token=GITHUB_API_TOKEN)
    organization = client.organization(organization_name)
    formatted_pull_requests = []

    for repository in organization.repositories():
        for pull_request in repository.pull_requests():
            if pull_request.state == 'open' and not is_ignored(pull_request.title):
                formatted_pull_requests.append(format_pull_request(pull_request, repository.name))

    return formatted_pull_requests


def send_to_slack(text):
    payload = {
        'token': SLACK_API_TOKEN,
        'channel': SLACK_CHANNEL,
        'username': 'Pull Request Reminder',
        'icon_emoji': ':bell:',
        'text': text
    }

    response = requests.post('https://slack.com/api/chat.postMessage', data=payload)
    answer = response.json()
    if not answer['ok']:
        raise Exception(answer['error'])


def cli():
    pull_requests = fetch_open_pull_requests(GITHUB_ORGANIZATION)
    text = "No open pull requests today :partyparrot:" if not pull_requests else "Hi! There's a few open pull requests you should take a look at:\n" + '\n'.join(pull_requests)
    send_to_slack(text)


if __name__ == '__main__':
    cli()
