# slack-pull-reminder

Posts a Slack reminder with a list of open pull requests for an
organization.

![slack-pull-reminder](http://i.imgur.com/3xsfTYV.png)

## Usage
-----

slack-pull-reminder is configured using environment variables:

### Required

-  `SLACK_API_TOKEN`: A [legacy](https://api.slack.com/custom-integrations/legacy-tokens) user token
-  `GITHUB_API_TOKEN`: These can be generated from your [personal settings]()
-  `ORGANIZATION`: The GitHub organization you want pull request reminders for.

### Optional

-  `IGNORE_WORDS`: A comma-separated list of words that will cause a pull request to be ignored.
-  `SLACK_CHANNEL`: The Slack channel you want the reminders to be posted in, defaults to #general.

## Example

```bash
$ ORGANIZATION="orgname" SLACK_API_TOKEN="token" GITHUB_API_TOKEN="token" slack-pull-reminder
```

## Cronjob

As slack-pull-reminder only runs once and exits, it's recommended to run
it regularly using for example a cronjob.

Example that runs slack-pull-reminder every day at 10:00:

```bash
0 10 * * * ORGANIZATION="orgname" SLACK_API_TOKEN="token" GITHUB_API_TOKEN="token" slack-pull-reminder
```
