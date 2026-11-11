# Dataset

21 misuse cases of two REST API services, contained in 16 input programs.

| Misuse type | SwitchBot | Fitbit | Total |
| --- | ---: | ---: | ---: |
| RH & EP (request header and endpoint) | 8 | 1 | 9 |
| EP (endpoint only) | 0 | 12 | 12 |
| Total | 8 | 13 | 21 |

## How cases are counted

An input program is a fragment of a client program that follows a deprecated
specification. One input program can contain more than one case.

- **SwitchBot (API v1.0 → v1.1)**: one case per input program. The endpoints and the
  request headers of a program change together with the API version.
- **Fitbit Sleep API (v1 → v1.2)**: one case per input program, also when the program
  calls several Sleep endpoints (`commits/2.java` calls six).
- **Fitbit OAuth (1.0 → 2.0)**: two cases per input program, the authorization endpoint
  and the token endpoint. The request-token endpoint is not counted; OAuth 2.0 has no
  such endpoint.

`cases.csv` lists the number of cases and the lines of the deprecated usage for every
input program.

| Service | Input program | Cases | Type | Counted as |
| --- | --- | ---: | --- | --- |
| SwitchBot | `commits/1.scala` | 1 | RH & EP | v1.0 endpoints and request headers |
| SwitchBot | `commits/2.py` | 1 | RH & EP | v1.0 endpoint and request headers |
| SwitchBot | `commits/3.py` | 1 | RH & EP | v1.0 endpoint and request headers |
| SwitchBot | `commits/4.py` | 1 | RH & EP | v1.0 endpoint and request headers |
| SwitchBot | `commits/5.py` | 1 | RH & EP | v1.0 endpoint and request headers |
| SwitchBot | `pull-requests/1.py` | 1 | RH & EP | v1.0 endpoint and request headers |
| SwitchBot | `pull-requests/2.py` | 1 | RH & EP | v1.0 endpoint and request headers |
| SwitchBot | `pull-requests/3.rb` | 1 | RH & EP | v1.0 endpoints and request headers |
| Fitbit | `commits/1.go` | 1 | EP | Sleep v1 endpoint |
| Fitbit | `commits/2.java` | 1 | EP | Sleep v1 endpoints (six calls) |
| Fitbit | `commits/3.json` | 2 | EP, EP | Authorization endpoint; token endpoint |
| Fitbit | `commits/4.pm` | 1 | EP | Sleep v1 endpoint |
| Fitbit | `commits/5.rb` | 2 | EP, EP | Authorization endpoint; token endpoint |
| Fitbit | `issues/5.js` | 2 | EP, EP | Authorization endpoint; token endpoint |
| Fitbit | `issues/6.py` | 2 | EP, EP | Authorization endpoint; token endpoint |
| Fitbit | `pull-requests/1.py` | 2 | RH & EP, EP | Authorization endpoint; token endpoint. The program also puts the OAuth 1.0 signature in the request header |

Each input program is repaired as a whole. The cases of one program are therefore
judged on the same output.

## Files

```text
dataset/
├── cases.csv             Number of cases per input program
├── resources.md          Source repository of every input program
├── switchbot/
│   ├── commits/          5 input programs
│   ├── pull-requests/    3 input programs
│   └── url/              Specification pages (deprecated.txt, latest.txt)
└── fitbit/
    ├── commits/          5 input programs
    ├── issues/           2 input programs
    ├── pull-requests/    1 input program
    └── url/              Specification pages (deprecated.txt, latest.txt)
```

The directory name (`commits`, `issues`, `pull-requests`) is the kind of GitHub record
through which the program was found. File numbers are identifiers and are not
consecutive.

## Specification pages

| File | Pages | Content |
| --- | ---: | --- |
| `switchbot/url/deprecated.txt` | 1 | SwitchBot API v1.0 |
| `switchbot/url/latest.txt` | 1 | SwitchBot API v1.1 |
| `fitbit/url/deprecated.txt` | 1 | Fitbit Sleep API v1 |
| `fitbit/url/latest.txt` | 126 | Fitbit Web API reference |

## Collection

The candidate programs were collected with the scripts in `collect/` and then selected
and extracted by hand; see `collect/README.md`. The source repositories are listed in
`resources.md`.
