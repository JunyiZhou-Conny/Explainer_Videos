from google.colab import drive
drive.mount('/content/drive')
cache_dir = '/content/drive/MyDrive/LLM_cache'
os.makedirs(cache_dir, exist_ok=True)