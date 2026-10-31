## <font color ='#16AD04'>**3. Setting up the environment** </font>

We will start by installing the necessary packages and pre-downloading the models.


Colab already includes recent versions of `torch`, `transformers`, `peft`, `accelerate`, `datasets` and `huggingface_hub`. The next cell installs the latest `bitsandbytes` (4-bit quantization) and `trl` (the `SFTTrainer`).

The imports cell prints the library versions in use. If a later cell fails, compare those versions first.