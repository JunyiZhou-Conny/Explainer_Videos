## <font color ='#16AD04'>**6. Download models from Hugging Face Hub** </font>

### Pre-caching Models for Faster Loading and Persistence

To speed up our workflow, we will pre-download the models we need using the [`huggingface-hub` command-line interface (CLI)](https://huggingface.co/docs/huggingface_hub/guides/cli). This is a best practice that avoids long, in-line download waits when you first load a model in Python.

Crucially, we will direct the CLI to save the models directly to the **`LLM_cache`** directory on our Google Drive. This ensures that if your Colab session disconnects, you won't have to re-download these large files.

We are downloading two models:
*   `facebook/opt-350m`: A small model for our quantization demonstration.
*   `Qwen/Qwen3-0.6B`: The main model we will fine-tune.

**A quick look at the command:**
*   `!hf download`: Runs the Hugging Face CLI download command.
*   `--cache-dir {cache_dir}`: **This is the key part.** It tells the command to save the files in the specific folder we defined in our Python `cache_dir` variable (our Google Drive folder).
*   `--quiet`: Suppresses the download progress bars.
*   `--exclude "*.h5" --exclude "*.msgpack"`: Skips the TensorFlow and Flax copies of the `opt-350m` weights, which PyTorch does not use. This saves 1.3 GB in your Google Drive.
