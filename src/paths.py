from pathlib import Path
import os

# Parent Directory
PARENT_DIR = Path(__name__).parent.resolve().parent

# Data Directory
DATA_DIR = PARENT_DIR.joinpath('data')
print(DATA_DIR)

# Weather Raw Data Directory
RAW_DATA_DIR = PARENT_DIR / 'data' / 'bronze'

# Weather Transformed Data Diectory
TRANSFORMED_DATA_DIR = PARENT_DIR / 'data' / 'gold'

# Model Directory
MODELS_DIR = PARENT_DIR / 'models'

if not Path(DATA_DIR).exists():
    os.mkdir(DATA_DIR)

if not Path(RAW_DATA_DIR).exists():
    os.mkdir(RAW_DATA_DIR)

if not Path(TRANSFORMED_DATA_DIR).exists():
    os.mkdir(TRANSFORMED_DATA_DIR)

if not Path(MODELS_DIR).exists():
    os.mkdir(MODELS_DIR)

