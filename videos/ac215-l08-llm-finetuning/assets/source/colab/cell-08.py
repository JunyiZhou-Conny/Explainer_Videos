# Colab ships recent torch, transformers, peft, accelerate, datasets and huggingface_hub. (installing these is optional for now)
# Colab doesn't ship trl and bitsandbytes - so we do need install them
!uv pip install transformers==5.16.1 tokenizers==0.23.1 huggingface-hub==1.29.0 bitsandbytes==0.50.2
!uv pip install trl==1.14.0

# Colab ships torchao 0.10; peft refuses to add LoRA layers to a full-precision model while it is installed.
!uv pip uninstall torchao