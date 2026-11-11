"""Search queries and filter keywords used to collect the misuse cases."""

# Queries sent to the GitHub Search API (commits, closed issues, closed pull requests).
SEARCH_QUERIES = {
    "fitbit": [
        "www.fitbit.com/oauth/authorize",
        "api.fitbit.com /oauth/request_token",
        "api.fitbit.com /oauth/access_token",
        "api.fitbit.com /sleep/startTime",
        "api.fitbit.com /sleep/timeInBed",
        "api.fitbit.com /sleep/awakeningsCount",
        "api.fitbit.com /sleep/minutesAwake",
        "api.fitbit.com /sleep/minutesToFallAsleep",
        "api.fitbit.com /sleep/minutesAfterWakeup",
        "api.fitbit.com /sleep/efficiency",
        "api.fitbit.com /sleep/minutesAsleep",
        "fitbit api update oauth",
        "fitbit api update sleep",
        "fitbit api update",
        "fitbit support oauth2",
        "fitbit support sleep",
        "api.fitbit.com/oauth2",
        "api.fitbit.com/1.2/user/-/sleep/date/",
    ],
    "switchbot": [
        "api.switch-bot.com /v1.0",
        "api.switch-bot.com /v1.1",
        "update: switchbotAPI version",
        "modularizing SwitchBot API",
        "SwitchBot API v1.1 update",
        "switchbot update commit",
        "switchbot API v1.1",
        "update switchbot API",
        "new switchbot API version",
        "switchbot support v1.1",
        "switchbotAPI update",
    ],
}

# A collected commit, issue or pull request is kept for manual inspection only when
# its diff or discussion contains one of these strings.
FILTER_KEYWORDS = {
    "fitbit": [
        "/oauth/authorize",
        "/oauth/request_token",
        "/oauth/access_token",
        "oauth/",
        "/oauth2/authorize",
        "/oauth2/token",
        "/oauth2",
        "oauth2/",
        "sleep/",
        "sleep/date",
    ],
    "switchbot": [
        "v1.0",
        "v1.1",
        "api.switch-bot.com",
        "headers",
        "header",
        "Authorization",
    ],
}
