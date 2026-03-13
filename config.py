import os

# Output
FULL_PATH = "/app/output/"
RELA_PATH = "output/"

# Models
MODELS = "/models"
INDEX = os.getenv("INDEX", "0,0")
MODEL_INDEX, MODEL_SUBINDEX = map(int, INDEX.split(","))

