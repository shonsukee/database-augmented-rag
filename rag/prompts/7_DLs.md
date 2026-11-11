## Instruction
You are a software engineer specializing in REST APIs.
Please follow the guidelines below to make the necessary modifications.

### Modification Procedure
1. Analyze the deprecated specifications based on `## Deprecated specification`.
2. Based on the analysis in step 1., identify code snippets that follow deprecated specifications within the source code in `## Input Code`.
3. Analyze the latest specifications based on `### Technical Specifications for latest natural language` and `### Technical Specifications for latest code`.
4. Modify the code snippets identified in step 2. to follow the latest specifications analyzed in step 3., while paying attention to the points listed in `### Attention` below.

### Attention
There may be multiple code snippets following deprecated specifications within `## Input Code`.
Only refer to the information in `## Latest specification` when making modifications.
Do not perform refactoring or add comments; only modify the parts of the code that follow deprecated specifications to conform to the latest specifications.
Copy the source code from `## Input Code` before making modifications.
Delete all parts only according to the deprecated specification and modify the code to conform to the latest specification.
Only modify the parts of the code that follow deprecated specifications.
If no deprecated specification is found in the source code of the `## Input Code`, compare the source code with the latest specification to identify any differences. If modifications are required, modify the source code according to the latest specification.
Make sure to modify all code that follows deprecated specifications.
After modifications, ensure that all code following deprecated specifications has been replaced with code that conforms to the latest specifications.
If multiple deprecated specifications are present within `## Input Code`, confirm that all are unified under the latest specifications.

## Deprecated specification
```
{deprecated}
```

## Input Code
```
{user_query}
```

## Technical Specifications for latest natural language
```
{latest_natural_language}
```

## Technical Specifications for latest code
```
{latest_code}
```

## Output Indicator
Ensure that, except for the parts modified to follow the latest specifications, the structure and format of the code remain identical to the original code. Here, "identical" means that there should be no differences (diff) whatsoever, including in indentation, spaces, line breaks, and code structure, which should all be exactly the same as the original.
If there are any changes beyond the modified sections, this is considered incorrect.
Also, verify that the modified code conforms to the latest specifications.