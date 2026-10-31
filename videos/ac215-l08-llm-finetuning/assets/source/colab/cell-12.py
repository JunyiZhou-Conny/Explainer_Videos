# This will import the libraries for the entire notebook.

from datasets import Dataset
import locale
locale.getpreferredencoding = lambda *args, **kwargs: "UTF-8"

# Libraries to load models in 4-bit
import os


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import transformers

# Libraries for LoRa
from peft import LoraConfig, PeftModel
from peft import prepare_model_for_kbit_training
from trl import SFTTrainer
from trl import SFTConfig

import pandas as pd
import math
from tqdm import tqdm
import matplotlib.pyplot as plt

from IPython.display import display, HTML

import bitsandbytes, peft, trl
print(f"torch {torch.__version__} | transformers {transformers.__version__} | peft {peft.__version__} | "
      f"trl {trl.__version__} | bitsandbytes {bitsandbytes.__version__}")