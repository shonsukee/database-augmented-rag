# Results

Stored outputs of the 12 configurations, five runs per input program:
12 configurations × 16 input programs × 5 runs = 960 files.

The 16 input programs contain 21 misuse cases (see `dataset/README.md`). There is one
output file per input program and run, so the cases of one program are judged on the
same output file.

```text
results/{configuration}/{service}/{commits|issues|pull-requests}/{input id}/{1..5}.md
```

`{input id}` is the file name of the input program without its extension, so
`results/9_DsLs/switchbot/commits/5/3.md` is the third run of `9_DsLs` on
`dataset/switchbot/commits/5.py`.

## File format

```text
# LLM Response
<output of the model>

# User Query
<the full prompt that was sent>
```

The five runs of one input under one configuration share the same prompt. A response
that came back without a code fence was wrapped in one, tagged with the extension of
the input file.

## How the outputs were produced

| Configuration | Produced by |
| --- | --- |
| `1_D` – `11_DtLt` | The pipeline in `rag/` (retrieval from Pinecone, generation with GPT-4o through the OpenAI API) |
| `0_BL` | The prompt was entered into ChatGPT (GPT-4o) by hand and the response was copied into the same file format |

The outputs were first committed on 2025-07-22 and 2025-08-19.

## Retrieved chunks per prompt

Number of specification chunks in the prompt (`【Context No.N】` entries), over the
inputs of each service. Each database returns at most 60 chunks; a database that holds
fewer chunks for a service returns all of them.

| Configuration | Databases | SwitchBot | Fitbit |
| --- | ---: | ---: | ---: |
| `0_BL` | 0 | 0 | 0 |
| `1_D` | 1 | 6 | 2 |
| `2_L` | 1 | 27 | 54–58 |
| `3_DLm` | 1 | 33 | 54–58 |
| `4_DL` | 2 | 33 | 56–60 |
| `5_Ds` | 2 | 51 | 13 |
| `6_Ls` | 2 | 77–80 | 98–107 |
| `7_DLs` | 3 | 83–86 | 100–109 |
| `8_DsL` | 3 | 78 | 67–71 |
| `9_DsLs` | 4 | 128–131 | 111–120 |
| `10_DcLc` | 2 | 102–105 | 56–61 |
| `11_DtLt` | 2 | 26 | 55–59 |

The chunks of each database can be read back from a stored prompt with
`rag.repair.prompt.split_prompt`.

## Evaluation

Whether an output is a successful repair was judged by hand by the first author, by
comparing the output with the fix in the source repository and with the latest
specification. The judgments are not included in this repository.

## Consistency checks

`make test` verifies, without any API access, that

- every configuration has five outputs for each input program,
- every stored prompt is the prompt template of its configuration filled with the
  corresponding input program, and
- the baseline prompts list exactly the URLs in `dataset/{service}/url/`.
