# pull-reminder

Posts a Slack reminder with a list of open pull requests for an
organization.

![pull-reminder](http://i.imgur.com/3xsfTYV.png)

## Usage
-----

`pull-reminder` is configured using environment variables:

### Required

-  `SLACK_API_TOKEN`: A [legacy](https://api.slack.com/custom-integrations/legacy-tokens) user token
-  `GITHUB_API_TOKEN`: These can be generated from your [personal settings](https://github.com/settings/tokens)
-  `ORGANIZATION`: The GitHub organization you want pull request reminders for.

### Optional

-  `IGNORE_WORDS`: A comma-separated list of words that will cause a pull request to be ignored.
-  `SLACK_CHANNEL`: The Slack channel you want the reminders to be posted in, defaults to #general.

## Deployment

This is deployed via [Heroku](https://dashboard.heroku.com/apps/pull-reminder/) automatically from the master branch.
