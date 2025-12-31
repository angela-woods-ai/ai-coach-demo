import os
from dotenv import load_dotenv

# Load .env once, early
load_dotenv()

# Feature flags
USE_PINECONE = os.getenv("USE_PINECONE", "false").lower() == "true"
print("USE_PINECONE =", USE_PINECONE)
USE_CLAUDE = os.getenv("USE_CLAUDE", "false").lower() == "true"
print("USE_CLAUDE =", USE_CLAUDE)

# Size of the embedding to use for fixed length embeddings
EMBED_DIM = int(os.environ.get("EMBED_DIM", 256))
print("EMBED_DIM = ", EMBED_DIM)
RECREATE_PINECONE_INDEX = os.getenv("RECREATE_PINECONE_INDEX", "false").lower() == "true"

# KNN Similarity threshold for finding matches that are actually similar
SIMILARITY_THRESHOLD = float(os.environ.get("SIMILARITY_THRESHOLD", 0.25))

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Later could add more configs to remove hardcoded items
#AI_SERVICE_PORT = int(os.getenv("AI_SERVICE_PORT", "8000"))
