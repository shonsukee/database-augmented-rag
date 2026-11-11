# Prompt templates

One template per configuration. The file name is the configuration name used in the
paper (Table 2) with a running number.

| File | Databases searched (placeholders) |
| --- | --- |
| `0_BL.md` | none — `{link}` receives the specification URLs |
| `1_D.md` | `{deprecated}` |
| `2_L.md` | `{latest}` |
| `3_DLm.md` | `{context}` (deprecated and latest specifications in one database) |
| `4_DL.md` | `{deprecated}`, `{latest}` |
| `5_Ds.md` | `{deprecated_natural_language}`, `{deprecated_code}` |
| `6_Ls.md` | `{latest_natural_language}`, `{latest_code}` |
| `7_DLs.md` | `{deprecated}`, `{latest_natural_language}`, `{latest_code}` |
| `8_DsL.md` | `{deprecated_natural_language}`, `{deprecated_code}`, `{latest}` |
| `9_DsLs.md` | `{deprecated_natural_language}`, `{deprecated_code}`, `{latest_natural_language}`, `{latest_code}` |
| `10_DcLc.md` | `{deprecated_code}`, `{latest_code}` |
| `11_DtLt.md` | `{deprecated_natural_language}`, `{latest_natural_language}` |

`{user_query}` receives the input program in every template.

Each placeholder other than `{user_query}` and `{link}` is filled with the chunks
retrieved from the database of the same name (Pinecone index name: underscores replaced
by hyphens), formatted as

```text
【Context No.1】
[similarity: 0.59]
<chunk text>

【Context No.2】
...
```

`0_BL.md` is the prompt of the baseline. The baseline was entered into ChatGPT by hand,
so `rag.repair` does not run it; the template is kept here because the stored baseline
outputs under `results/0_BL/` were produced with it.

`tests/test_results.py` checks that every stored output under `results/` was produced
from the template of its configuration.
