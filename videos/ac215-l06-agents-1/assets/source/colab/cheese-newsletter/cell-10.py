# @title Setup OpenAI Key
# Using Google Colab's Secrets feature 🔑
from google.colab import userdata
api_key = userdata.get('OPENAI_API_KEY')
import os
os.environ['OPENAI_API_KEY'] = api_key
