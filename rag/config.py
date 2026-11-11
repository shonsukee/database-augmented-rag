"""Experimental settings shared by the store and repair steps."""

# Generation
GENERATION_MODEL = "gpt-4o"
# Sent as the system message of every generation request. {service} is the API name
# ("switchbot" or "fitbit").
SYSTEM_PROMPT = (
    "You are a chatbot that modifies an old version of the {service} API to a new one. "
    "Relevant information must be followed."
)
# Each input program is repaired this many times with the same prompt.
TRIALS = 5

# Indexing
EMBEDDING_MODEL = "text-embedding-3-large"
EMBED_BATCH_SIZE = 100
CHUNK_SIZE = 2048
CHUNK_OVERLAP = 200

# Retrieval (applied to every database of a configuration)
SIMILARITY_TOP_K = 60
SIMILARITY_CUTOFF = 0.0

SERVICES = ("switchbot", "fitbit")

# Configuration name -> databases it searches. A database name is also the name of the
# placeholder in the prompt template that receives the retrieved chunks.
CONFIGURATIONS = {
    "1_D": ("deprecated",),
    "2_L": ("latest",),
    "3_DLm": ("context",),
    "4_DL": ("deprecated", "latest"),
    "5_Ds": ("deprecated_natural_language", "deprecated_code"),
    "6_Ls": ("latest_natural_language", "latest_code"),
    "7_DLs": ("deprecated", "latest_natural_language", "latest_code"),
    "8_DsL": ("deprecated_natural_language", "deprecated_code", "latest"),
    "9_DsLs": (
        "deprecated_natural_language",
        "deprecated_code",
        "latest_natural_language",
        "latest_code",
    ),
    "10_DcLc": ("deprecated_code", "latest_code"),
    "11_DtLt": ("deprecated_natural_language", "latest_natural_language"),
}
