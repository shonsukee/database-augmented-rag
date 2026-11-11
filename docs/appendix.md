# Appendix

## Storing Deprecated Specifications

**D** stores only deprecated specifications in the database.
The LLM uses these specifications to compare the target function with deprecated API usage and identify misuse instances.
The latest specifications are intentionally omitted from the prompt to examine whether the LLM can repair deprecated code snippets using its internal knowledge.

The prompt includes background information, a work policy, and modification procedures.
First, the LLM analyzes the deprecated specifications retrieved by RAG to detect misuse.
It then corrects the code using its internal knowledge.
If the misuse is unclear, the model outputs the original code.
Thus, this setup uses external knowledge for detection and internal knowledge for correction.

## Storing Latest Specifications

**L** stores only the latest specifications in the database.
Because LLMs may lack knowledge about rare or frequently updated APIs, RAG provides the latest specifications as reliable external knowledge.

This setup tests whether the latest specifications help the LLM detect and repair REST API misuse.
The retrieved specifications serve as ground truth and help the model compare the current implementation with the correct API rules.

## Storing Deprecated and Latest Specifications Separately

**DL** stores the latest and deprecated specifications in separate databases.
Unlike **DLm**, which stores both types in a single database, **DL** retrieves each specification type independently.

This separation clarifies the role of each context.
Deprecated specifications are used to detect misuse, whereas latest specifications are used to repair the code.
This design helps the model distinguish outdated usage from correct usage.

## Splitting Deprecated Specifications into Code and Natural Language

**Ds** splits deprecated specifications into code snippets and natural-language text and stores them separately.

We use the deprecated code snippets as direct search targets because they can reveal structurally similar misuse patterns.
Natural-language text provides additional context for understanding deprecated rules.
This configuration aims to improve misuse detection based on deprecated specifications.

## Splitting Latest Specifications into Code and Natural Language

**Ls** splits latest specifications into code snippets and natural-language text and stores them separately.

The purpose of this split is to retrieve clean and up-to-date correction information with less noise.
Code snippets provide concrete implementation examples, while natural-language text provides rule-level explanations.
This setup aims to improve correction accuracy.

## Splitting Only Latest Specifications

**DLs** stores deprecated specifications together but splits the latest specifications into code snippets and natural-language text.

The split of the latest specifications helps isolate reliable correction information.
Meanwhile, the integrated deprecated specifications are used to detect misuse with a lower processing cost.
This setup targets cases where misuse detection is relatively accurate, but correction requires more precise latest specifications.

## Splitting Only Deprecated Specifications

**DsL** splits deprecated specifications into code snippets and natural-language text but stores latest specifications together.

The split of deprecated specifications helps extract clearer misuse indicators.
Deprecated code snippets can reveal outdated implementation patterns, while deprecated natural-language text explains outdated rules.
This setup is intended for cases where correction accuracy is sufficient, but misuse detection requires more support.

## Storing Only Code Snippets

**DcLc** stores only code snippets from the specifications.
REST API specifications contain both code snippets and natural-language text.
Since this study aims to repair source code, this setup focuses on implementation examples.

Code snippets are directly related to implementation and can show concrete correction patterns.
Natural-language text is excluded to reduce input tokens and retrieval noise.
This setup tests whether a code-only database improves correction accuracy.

## Storing Only Natural-Language Text

**DtLt** stores only natural-language text from the specifications.

Natural-language text can describe API constraints, background information, and detailed rules that may not appear in code snippets.
This setup tests whether text-only retrieval provides enough context for detecting and correcting REST API misuse.
