# Dataset Overview

This dataset contains API documentation references and code snippets related to Fitbit and SwitchBot.

The code snippets were collected from real GitHub repositories that use the Fitbit API or the SwitchBot API.

## Directory Structure

```text
dataset/
├── url/
├── commits/
├── pull-requests/
└── issues/
```

## API Documentation Resources

The `url/` directory contains API documentation URLs. These files are reference resources, not extracted source code snippets.

| Resource       | Description                       | URL                                             |
| -------------- | --------------------------------- | ----------------------------------------------- |
| Fitbit Web API | Official Fitbit Web API reference | https://dev.fitbit.com/build/reference/web-api/ |
| SwitchBot API  | SwitchBot API documentation       | https://github.com/OpenWonderLabs/SwitchBotAPI  |

## Source Repositories

The files under `commits/`, `pull-requests/`, and `issues/` are code snippets collected from the following GitHub repositories.

For each snippet I traced the exact GitHub commit (verified by matching the snippet's
distinctive lines against the file contents at each commit in history):

- **Introducing commit** — the commit where this code / API usage first entered the repository.
- **Snippet permalink** — a blob URL pinned to a commit whose file content matches the
  dataset snippet exactly. For deprecated snippets (OAuth1, etc.) this is the last commit
  before the code was rewritten.

### Fitbit

| Dataset File         | Source Repository / Original File | Introducing commit | Snippet permalink (matching version) |
| -------------------- | --------------------------------- | ------------------ | ------------------------------------ |
| `commits/1.go`       | [Thomas2500/go-fitbit](https://github.com/Thomas2500/go-fitbit) — `sleep.go` | [`18bc4fa`](https://github.com/Thomas2500/go-fitbit/commit/18bc4fa) (2020-08-16) | [blob@117c6c9](https://github.com/Thomas2500/go-fitbit/blob/117c6c9b379d/sleep.go) |
| `commits/2.java`     | [denzilferreira/com.aware.plugin.fitbit](https://github.com/denzilferreira/com.aware.plugin.fitbit) — `Plugin.java` | [`4b6f5bb`](https://github.com/denzilferreira/com.aware.plugin.fitbit/commit/4b6f5bb) (2017-01-12) | [blob@944f41f](https://github.com/denzilferreira/com.aware.plugin.fitbit/blob/944f41f/com.aware.plugin.fitbit/src/main/java/com/aware/plugin/fitbit/Plugin.java) |
| `commits/3.json`     | [simov/grant](https://github.com/simov/grant) — `config/oauth.json` (OAuth1 era) | [`613a4ac`](https://github.com/simov/grant/commit/613a4ac) (2014-12-28, "Add fitbit") | [blob@d3e261e](https://github.com/simov/grant/blob/d3e261e/config/oauth.json) (last OAuth1 version) |
| `commits/4.pm`       | [MrStrategy/FHEM-fitbit](https://github.com/MrStrategy/FHEM-fitbit) — `32_fitbit.pm` | [`e7a2465`](https://github.com/MrStrategy/FHEM-fitbit/commit/e7a2465) (2019-03-10, first commit) | [blob@a402441](https://github.com/MrStrategy/FHEM-fitbit/blob/a402441/32_fitbit.pm) |
| `commits/5.rb`       | [whazzmaster/fitgem](https://github.com/whazzmaster/fitgem) — `lib/fitgem/client.rb` (OAuth1) | [`b0ad12b`](https://github.com/whazzmaster/fitgem/commit/b0ad12b) (2011-11-28) | [blob@9d50f5c](https://github.com/whazzmaster/fitgem/blob/9d50f5c/lib/fitgem/client.rb) (last OAuth1 version, before OAuth2 migration) |
| `issues/5.js`        | Posted in GitHub **issue** [googleworkspace/apps-script-oauth1 #8](https://github.com/googleworkspace/apps-script-oauth1/issues/8) (the `getFitbitService()` code is in the issue body). Same code also lives in [simonbromberg/googlefitbit](https://github.com/simonbromberg/googlefitbit). | —  | https://github.com/googleworkspace/apps-script-oauth1/issues/8 |
| `issues/6.py`        | [omab/python-social-auth](https://github.com/omab/python-social-auth) — `social/backends/fitbit.py` (OAuth1 backend) | [`3e5d77f`](https://github.com/omab/python-social-auth/commit/3e5d77f38d1105da8a62451290a89a957a5bb981) | Related issues/PRs: [issue #733](https://github.com/omab/python-social-auth/issues/733), [PR #625](https://github.com/omab/python-social-auth/pull/625). Exact originating issue/comment not pinned. |
| `pull-requests/1.py` | [orcasgit/python-fitbit](https://github.com/orcasgit/python-fitbit) — `fitbit/api.py` (OAuth1 `FitbitOauthClient`) | [`eb0a61e`](https://github.com/orcasgit/python-fitbit/commit/eb0a61e) (2014-01-23) → [PR #10](https://github.com/orcasgit/python-fitbit/pull/10) | [blob@7e7dd9d](https://github.com/orcasgit/python-fitbit/blob/7e7dd9d/fitbit/api.py) → [PR #84](https://github.com/orcasgit/python-fitbit/pull/84) |

### SwitchBot

| Dataset File         | Source Repository / Original File | Introducing commit | Snippet permalink (matching version) |
| -------------------- | --------------------------------- | ------------------ | ------------------------------------ |
| `commits/1.scala`    | [y-yu/kindle-clock](https://github.com/y-yu/kindle-clock) — `…/switchbot/SwitchBotApiClientImpl.scala` | [`0cc4bad`](https://github.com/y-yu/kindle-clock/commit/0cc4bad) (2022-04-26, "Add switchbot") | [blob@5ba2739](https://github.com/y-yu/kindle-clock/blob/5ba2739/module/infra/src/main/scala/kindleclock/infra/api/switchbot/SwitchBotApiClientImpl.scala) |
| `commits/2.py`       | [jcostom/sbtemp](https://github.com/jcostom/sbtemp) — `sbtemp.py` (temperature / night-schedule version) | [`95f079e`](https://github.com/jcostom/sbtemp/commit/95f079e) (2022-04-16) | [blob@8e3615c](https://github.com/jcostom/sbtemp/blob/8e3615c/sbtemp.py) |
| `commits/3.py`       | [jcostom/sbhum](https://github.com/jcostom/sbhum) — `sbhum.py` (humidity version; **not** sbtemp) | [`9516e60`](https://github.com/jcostom/sbhum/commit/9516e60) (2022-04-16) | [blob@bfcb234](https://github.com/jcostom/sbhum/blob/bfcb234/sbhum.py) |
| `commits/4.py`       | [masayoshikuroda/switch-bot](https://github.com/masayoshikuroda/switch-bot) | — | Migration commit recorded during collection: [`19dd704`](https://github.com/masayoshikuroda/switch-bot/commit/19dd704649ee2dab86aa1ba9c1a29565ef8b52a6) |
| `commits/5.py`       | [snoozers/lazy-home](https://github.com/snoozers/lazy-home) — `layer/switchbot.py` | [`f5d600d`](https://github.com/snoozers/lazy-home/commit/f5d600d) (2022-10-07) | [blob@bb9a929](https://github.com/snoozers/lazy-home/blob/bb9a929/layer/switchbot.py) |
| `pull-requests/1.py` | [jsk-ros-pkg/jsk_3rdparty](https://github.com/jsk-ros-pkg/jsk_3rdparty) — `switchbot_ros/src/switchbot_ros/switchbot.py` | [`16a5cd7`](https://github.com/jsk-ros-pkg/jsk_3rdparty/commit/16a5cd7) (2021-08-11) → [PR #278](https://github.com/jsk-ros-pkg/jsk_3rdparty/pull/278) | [blob@429cd88](https://github.com/jsk-ros-pkg/jsk_3rdparty/blob/429cd88/switchbot_ros/src/switchbot_ros/switchbot.py) |
| `pull-requests/2.py` | [jonghwanhyeon/python-switchbot](https://github.com/jonghwanhyeon/python-switchbot) — `switchbot/client.py` | [`04d6588`](https://github.com/jonghwanhyeon/python-switchbot/commit/04d6588) (2021-08-20, "Use SwitchBot Official API"; pushed directly, no PR) | [blob@8d9dde0](https://github.com/jonghwanhyeon/python-switchbot/blob/8d9dde0/switchbot/client.py) |
| `pull-requests/3.rb` | [ytkg/switchbot](https://github.com/ytkg/switchbot) — `lib/switchbot/client.rb` | [`b627418`](https://github.com/ytkg/switchbot/commit/b627418) (2021-03-02, "Support devices endpoint"; pushed directly, no PR) | [blob@57717be](https://github.com/ytkg/switchbot/blob/57717be/lib/switchbot/client.rb) |
