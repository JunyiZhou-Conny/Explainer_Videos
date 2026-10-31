from google.colab import userdata
import os

# Get the Hugging Face token from Colab secrets
hf_token = userdata.get('HF_TOKEN')

# You can now use this token, for example, to log in to Hugging Face
from huggingface_hub import login
login(token=hf_token)

print("Hugging Face token successfully loaded.")