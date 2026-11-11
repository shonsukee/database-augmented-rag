# Database-Augmented RAG for Automated Repair of REST API Misuses

Artifact of the study on repairing client programs that follow deprecated REST API
specifications, using an LLM with retrieval-augmented generation (RAG). The study
compares database configurations that differ in which specification version is stored
(deprecated, latest) and how it is stored (whole pages, or code snippets and
natural-language text in separate databases).

This repository contains

- the dataset: 21 misuse cases in 16 input programs, and the lists of specification
  pages (`dataset/`),
- the scripts used to collect candidate programs from GitHub (`collect/`),
- the RAG pipeline: specification storage and repair generation (`rag/`), and
- the stored outputs of every configuration (`results/`).

## Layout

```text
.
├── dataset/     21 misuse cases in 16 input programs, and specification URLs
├── collect/     GitHub search, de-duplication and keyword filter
├── rag/
│   ├── config.py   Models, chunking, top-k, number of runs, system prompt
│   ├── store/      Fetch specification pages and store them in Pinecone
│   ├── repair/     Retrieve, build the prompt, generate, save
│   └── prompts/    Prompt template of each configuration
├── results/     Stored outputs of the 12 configurations
├── docs/        Design intent of each configuration
└── tests/       Consistency checks (no API access needed)
```

`dataset/`, `collect/`, `rag/prompts/` and `results/` have their own README.

## Dataset

| Misuse type | SwitchBot | Fitbit | Total |
| --- | ---: | ---: | ---: |
| RH & EP (request header and endpoint) | 8 | 1 | 9 |
| EP (endpoint only) | 0 | 12 | 12 |
| Total | 8 | 13 | 21 |

The 21 cases are contained in 16 input programs (SwitchBot 8, Fitbit 8). A SwitchBot
program and a Fitbit Sleep API program count as one case each. A Fitbit OAuth program
counts as two cases, the authorization endpoint and the token endpoint.
`dataset/README.md` gives the count for every input program.

## Configurations

| Name | Databases | Stored content |
| --- | ---: | --- |
| `0_BL` | 0 | Baseline without RAG; the prompt lists the specification URLs |
| `1_D` | 1 | Deprecated specification |
| `2_L` | 1 | Latest specification |
| `3_DLm` | 1 | Deprecated and latest specifications mixed in one database |
| `4_DL` | 2 | Deprecated and latest specifications in separate databases |
| `5_Ds` | 2 | Deprecated specification, split into code snippets and text |
| `6_Ls` | 2 | Latest specification, split into code snippets and text |
| `7_DLs` | 3 | Deprecated specification; latest specification split |
| `8_DsL` | 3 | Deprecated specification split; latest specification |
| `9_DsLs` | 4 | Deprecated and latest specifications, each split |
| `10_DcLc` | 2 | Code snippets only, deprecated and latest |
| `11_DtLt` | 2 | Natural-language text only, deprecated and latest |

The design intent of each configuration is described in `docs/appendix.md`.

## Experimental settings

All values are defined in `rag/config.py`.

| Item | Setting |
| --- | --- |
| Generation model (`1_D` – `11_DtLt`) | GPT-4o (`gpt-4o`) through the OpenAI Chat Completions API, default sampling parameters |
| System message | `You are a chatbot that modifies an old version of the {service} API to a new one. Relevant information must be followed.` |
| Runs | 5 per input program, with the same prompt |
| Embedding model | `text-embedding-3-large` |
| Chunking | LlamaIndex default splitter, chunk size 2048 tokens, overlap 200 tokens |
| Retrieval | Top 60 chunks per database, query = the input program |
| Vector database | Pinecone; one index per database, one namespace per service |
| Baseline (`0_BL`) | GPT-4o in ChatGPT; the prompt `rag/prompts/0_BL.md` was entered by hand |

The retrieved chunks are inserted into the prompt in the order returned by the vector
search. No reranking is applied.

The baseline is not part of the pipeline code because it was run in the ChatGPT web
interface. Its prompt template and its outputs are included.

## Requirements

- Python 3.12, or Docker
- `OPENAI_API_KEY` and `PINECONE_API_KEY` (copy `.env.example` to `.env`)
- `GITHUB_TOKEN` only for `collect/`

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

or

```bash
docker build -t database-augmented-rag .
docker run --rm -it -v "$(pwd):/app" database-augmented-rag
```

## Store the specifications

Create the Pinecone indexes first (dimension 3072, the size of
`text-embedding-3-large` vectors):

`deprecated`, `latest`, `context`, `deprecated-natural-language`, `deprecated-code`,
`latest-natural-language`, `latest-code`

```bash
# Whole pages: databases of D, L, DL
make store name=switchbot version=deprecated method=all
make store name=switchbot version=latest     method=all

# Both versions in one database: DLm
make store name=switchbot version=deprecated method=all index-name=context
make store name=switchbot version=latest     method=all index-name=context

# Code snippets and natural-language text apart: Ds, Ls, DLs, DsL, DsLs, DcLc, DtLt
make store name=switchbot version=deprecated method=separate
make store name=switchbot version=latest     method=separate
```

Repeat with `name=fitbit`. Code snippets are the `<pre>` blocks of a specification
page; the natural-language text is the rest of the page.

## Run the repair

```bash
make repair name=switchbot types="commits pull-requests"        config=9_DsLs out=./output
make repair name=fitbit    types="commits issues pull-requests" config=9_DsLs out=./output
```

`config` is one of `1_D` … `11_DtLt`. Outputs are written to
`{out}/{config}/{service}/{type}/{input id}/{1..5}.md` in the format described in
`results/README.md`. The default output directory is `./output`, so a new run does not
overwrite `results/`.

The specification pages and the model behind `gpt-4o` change over time, so a new run
does not reproduce the stored outputs exactly.

## Tests

```bash
make test
```

The tests need neither API keys nor the packages in `requirements.txt`. They check
that the stored outputs in `results/` are consistent with the prompt templates and the
input programs in this repository, and they cover prompt construction and the helper
functions of `collect/`.

## Earlier repository

The development history up to 2026 is kept in
[`shonsukee/database-augmented-rag-legacy`](https://github.com/shonsukee/database-augmented-rag-legacy).
This repository is a cleaned-up version of that code for the stored outputs:

- The LLM reranking step and the support for local models, both added after the
  outputs were generated, are removed.
- The generation model is set to `gpt-4o`, the model used for the stored outputs. The
  code committed to the earlier repository named a different model.
- The unused answer-synthesis call during retrieval is removed; the retrieved chunks
  are the same.
- `rag/prompts/3_DLm.md` is the version of the template that the stored `3_DLm`
  outputs were generated with.
- The specification URL lists are the ones used for the stored outputs.

## License

See `LICENSE`.
