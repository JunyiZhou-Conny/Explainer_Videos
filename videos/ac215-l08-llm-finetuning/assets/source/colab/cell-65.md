---

## <font color ='#16AD04'>**Step 4: Configure and Execute Fine-Tuning** </font>

Now we bring together the "LoRA" part of QLoRA! We'll configure LoRA adapters, set training parameters, and train.

### <font color ='#0376B9'>**4.1 Configure LoRA Parameters** </font>

LoRA (Low-Rank Adaptation) allows us to train only a small fraction of parameters by inserting trainable rank decomposition matrices into the model:

**Key LoRA parameters:**
- `r`: Rank of the LoRA matrices (lower = fewer parameters)
- `lora_alpha`: Scaling factor for LoRA updates  
- `lora_dropout`: Dropout applied to LoRA layers for regularization