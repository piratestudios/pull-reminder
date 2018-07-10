from datetime import datetime
from github import Github
import os
import requests
import schedule
import sys
import time

ignore_labels = os.environ.get('GITHUB_IGNORE_LABELS')
GITHUB_IGNORE_LABELS = ignore_labels.split(',') if ignore_labels else []

ignore_title_words = os.environ.get('GITHUB_IGNORE_TITLE_WORDS')
GITHUB_IGNORE_TITLE_WORDS = ignore_title_words.split(',') if ignore_title_words else []

SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#general')

try:
    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']
    GITHUB_ORGANIZATION = os.environ['GITHUB_ORGANIZATION']
except KeyError as error:
    sys.stderr.write('Please set the environment variable {0}'.format(error))
    sys.exit(1)

client = Github(GITHUB_API_TOKEN)

def is_ignored(pull_request):
    lowercase_title = pull_request.title.lower()
    ignored_title = False
    for ignored_word in GITHUB_IGNORE_TITLE_WORDS:
        if ignored_word.lower() in lowercase_title:
            ignored_title = True

    ignored_label = False
    # TODO the python library doesn't fetch the labels, even though Githubs Api returns them
    # https://github.com/PyGithub/PyGithub/blob/v1.39/github/PullRequest.py
    # for label in (pull_request.labels if pull_request.labels else []):
    #     if label in GITHUB_IGNORE_LABELS:
    #         ignored_label = True

    return ignored_title or ignored_label


def format_pull_request(pull_request, repository):
    assignees = []
    for assignee in pull_request.assignees:
        assignees.append(assignee.login)

    # TODO the python library doesn't fetch the reviewers, even though GitHub's Api returns them
    # https://github.com/PyGithub/PyGithub/blob/v1.39/github/PullRequest.py
    # for reviewer in pull_request.reviewers:
    #     assignees.append(reviewer.login)

    assignee_text = ', '.join(assignees) if assignees else "no one"
    creator = pull_request.user.login
    created_days_ago = (datetime.now() - pull_request.created_at).days

    return f"<{pull_request.html_url}|{repository}/{pull_request.title}> - by {creator} - assigned to *{assignee_text}* - created {created_days_ago} days ago"


def fetch_open_pull_requests(organization_name):
    formatted_pull_requests = []

    for repository in client.get_organization(organization_name).get_repos('all'):
        pull_requests = [pull_request for pull_request in repository.get_pulls(state='open')]
        pull_requests.sort(key=lambda pr: pr.created_at)
        for pull_request in pull_requests:
            if not is_ignored(pull_request):
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


def update_slack():
    print('Checking for pull requests')
    pull_requests = fetch_open_pull_requests(GITHUB_ORGANIZATION)
    text = "No open pull requests today :partyparrot:" if not pull_requests else "Hi! There's a few open pull requests you should take a look at:\n" + '\n'.join(pull_requests)
    print(text)
    send_to_slack(text)


if __name__ == '__main__':
    print('beep boop')
    schedule.every().day.at("09:30").do(update_slack)
    while True:
        schedule.run_pending()
        time.sleep(1)
