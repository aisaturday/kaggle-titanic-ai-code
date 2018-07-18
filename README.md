# kaggle-titanic-ai-code
open sourced titanic ai code for kaggle competitions with google colab

# USAGE
## local
pip install -r requirements.txt --user
python kaggle-titanic-ai-code.py

## colab
import sys 
import os
sys.path.append(os.path.abspath("/path/to/requirements/on/google/drive/kt-ai-code"))

!pip install -r /path/to/requirements/on/google/drive/requirements.txt

import titanic_predict as tp # see https://github.com/aisaturday/kaggle-titanic-ai-code for more details